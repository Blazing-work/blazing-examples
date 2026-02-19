"""
Podcast Transcription Example for Blazing

Demonstrates parallel audio transcription using:
- FFmpeg for audio processing (Python 3.13+ compatible)
- OpenAI Whisper API for transcription
- Asyncio Semaphore for parallel processing with throttling
- Automatic chunking to handle 25MB Whisper API file size limit

SYSTEM DEPENDENCY: Requires ffmpeg and ffprobe
  - macOS: brew install ffmpeg
  - Ubuntu: apt-get install ffmpeg
  - Windows: https://ffmpeg.org/download.html
"""

import os
import logging
import asyncio
from typing import Dict, Any, List
from pathlib import Path
import tempfile

from audio_ffmpeg import audio_duration_seconds, split_audio
from blazing import Blazing, BaseService
from blazing_service.connectors.openai import OpenAIConnector
from blazing_service.connectors.secrets import SecretsConnector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blazing app
app = Blazing(
    api_url=os.getenv("BLAZING_API_URL", "http://localhost:8000"),
    api_token=os.getenv("BLAZING_API_TOKEN", "demo-token-placeholder")
)


@app.service(egress=["api.openai.com"])
class TranscriptionService(BaseService):
    """
    Audio transcription service using OpenAI Whisper API.

    Workflow:
    1. Load audio file (any format supported by ffmpeg)
    2. Split into 10-minute chunks (well under 25MB Whisper limit)
    3. Transcribe chunks in parallel with Semaphore(3) throttling
    4. Merge transcripts in order

    Uses FFmpeg for audio processing (Python 3.13+ compatible).
    """

    def __init__(self, connector_instances=None):
        """Initialize transcription service with OpenAI."""
        super().__init__(connector_instances)

        # Initialize connectors
        self.secrets = connector_instances.get('secrets') if connector_instances else SecretsConnector()
        self.openai = connector_instances.get('openai') if connector_instances else None

        # Semaphore to limit concurrent Whisper API calls (prevents overwhelming API)
        self.transcription_semaphore = asyncio.Semaphore(3)

        # Temporary directory for audio chunks
        self.temp_dir = Path(tempfile.mkdtemp(prefix="transcription_"))

        logger.info("TranscriptionService initialized")

    async def _ensure_openai_connected(self):
        """Ensure OpenAI connector is initialized and connected."""
        if self.openai is None:
            api_key = await self.secrets.get("OPENAI_API_KEY")
            self.openai = OpenAIConnector(api_key=api_key)

        if not self.openai.is_connected:
            await self.openai.connect()

    async def _split_audio(self, audio_path: str, chunk_duration_seconds: float = 10 * 60) -> List[Path]:
        """
        Split audio into chunks of specified duration using FFmpeg.

        Args:
            audio_path: Path to audio file
            chunk_duration_seconds: Duration of each chunk in seconds (default: 10 minutes)

        Returns:
            List of paths to audio chunk files
        """
        chunks = split_audio(
            in_path=audio_path,
            out_dir=self.temp_dir,
            chunk_seconds=chunk_duration_seconds,
            out_ext="mp3",
            bitrate="128k",
            sample_rate=16000,
            mono=True
        )

        logger.info(f"Split audio into {len(chunks)} chunks ({chunk_duration_seconds/60:.1f} min each)")
        return chunks

    async def _transcribe_chunk(self, chunk_path: Path, chunk_index: int) -> Dict[str, Any]:
        """
        Transcribe a single audio chunk using Whisper API.

        Args:
            chunk_path: Path to audio chunk file
            chunk_index: Index of this chunk (for ordering)

        Returns:
            Dictionary with transcript and metadata
        """
        async with self.transcription_semaphore:
            # Get chunk duration using FFmpeg
            chunk_duration = audio_duration_seconds(chunk_path)

            logger.info(f"Transcribing chunk {chunk_index} ({chunk_duration:.1f}s)")

            # Transcribe using Whisper API with verbose_json for timestamps
            with open(chunk_path, 'rb') as audio_file:
                result = await self.openai.transcribe(
                    audio_file=audio_file,
                    model="whisper-1",
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )

            logger.info(f"Chunk {chunk_index} transcribed ({len(result.get('text', ''))} chars)")

            return {
                "index": chunk_index,
                "text": result.get("text", ""),
                "duration": result.get("duration", 0),
                "segments": result.get("segments", [])
            }

    async def transcribe(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribe audio file with automatic chunking and parallel processing.

        Args:
            audio_path: Path to audio file (any format supported by ffmpeg)

        Returns:
            Dictionary with full transcript and metadata
        """
        await self._ensure_openai_connected()

        logger.info(f"Loading audio file: {audio_path}")

        # Get audio metadata using FFmpeg
        from audio_ffmpeg import get_audio_info
        audio_info = get_audio_info(audio_path)
        duration_seconds = audio_info["duration"]

        logger.info(f"Loaded audio: {duration_seconds:.1f}s, {audio_info['channels']} channels, {audio_info['sample_rate']}Hz")

        # Split into 10-minute chunks (600 seconds)
        # At typical MP3 bitrate (128kbps), 10 minutes ≈ 9.4MB (well under 25MB limit)
        chunk_duration_seconds = 10 * 60
        chunk_paths = await self._split_audio(audio_path, chunk_duration_seconds)

        logger.info(f"Transcribing {len(chunk_paths)} chunks in parallel (max 3 concurrent)")

        # Transcribe all chunks in parallel with semaphore throttling
        transcription_tasks = [
            self._transcribe_chunk(chunk_path, i)
            for i, chunk_path in enumerate(chunk_paths)
        ]

        chunk_results = await asyncio.gather(*transcription_tasks)

        # Sort by chunk index (should already be sorted, but ensure correctness)
        chunk_results.sort(key=lambda x: x["index"])

        # Merge transcripts
        full_transcript = " ".join(result["text"].strip() for result in chunk_results)
        total_duration = sum(result["duration"] for result in chunk_results)

        # Merge segments with adjusted timestamps
        all_segments = []
        time_offset = 0.0
        for result in chunk_results:
            for segment in result.get("segments", []):
                adjusted_segment = segment.copy()
                adjusted_segment["start"] += time_offset
                adjusted_segment["end"] += time_offset
                all_segments.append(adjusted_segment)
            time_offset += result["duration"]

        # Clean up temporary chunk files
        for chunk_path in chunk_paths:
            chunk_path.unlink(missing_ok=True)

        logger.info(f"Transcription complete: {len(full_transcript)} chars, {len(all_segments)} segments")

        return {
            "transcript": full_transcript,
            "duration_seconds": duration_seconds,
            "chunks": len(chunk_paths),
            "segments": all_segments,
            "metadata": {
                "audio_duration": duration_seconds,
                "chunks_processed": len(chunk_paths),
                "segments_count": len(all_segments),
                "channels": audio_info["channels"],
                "frame_rate": audio_info["sample_rate"]
            }
        }


# Create service instance
transcription_service = TranscriptionService()


@app.endpoint.post("/transcribe")
async def transcribe_endpoint(request):
    """
    Transcribe uploaded audio file.

    Expects multipart form data with 'file' field containing audio file.

    Returns:
        JSON with full transcript and metadata
    """
    form = await request.form()

    if 'file' not in form:
        return {"error": "No file provided"}, 400

    file = form['file']

    # Save uploaded file temporarily
    temp_path = Path("/tmp") / file.filename
    with open(temp_path, 'wb') as f:
        f.write(await file.read())

    try:
        result = await transcription_service.transcribe(str(temp_path))
        return result
    finally:
        # Clean up temp file
        temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    # For testing: generate silent audio and transcribe
    import asyncio

    async def test_transcription():
        """Test transcription with generated silent audio."""
        print("Generating 30-second silent audio for testing...")

        # Generate 30 seconds of silent audio using FFmpeg
        from audio_ffmpeg import create_silent_audio
        test_path = "/tmp/test_audio.mp3"
        create_silent_audio(test_path, duration_seconds=30)

        print(f"Generated test audio: {test_path}")
        print("Note: Whisper may return empty or minimal transcript for silent audio")

        print("\nTranscribing...")
        result = await transcription_service.transcribe(test_path)

        print("\nResults:")
        print(f"Transcript: {result['transcript'][:200]}..." if len(result['transcript']) > 200 else f"Transcript: {result['transcript']}")
        print(f"Duration: {result['duration_seconds']:.1f}s")
        print(f"Chunks: {result['chunks']}")
        print(f"Segments: {result['metadata']['segments_count']}")

        # Clean up test file
        Path(test_path).unlink(missing_ok=True)

    asyncio.run(test_transcription())
