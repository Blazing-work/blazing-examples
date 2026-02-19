# Podcast Transcription Example

This example demonstrates automatic audio transcription using OpenAI's Whisper API with automatic chunking for large files and parallel processing for speed.

## What It Does

Creates an audio transcription service with automatic file handling:

1. **Audio Loading**: Supports any format (MP3, MP4, M4A, WAV, FLAC) via pydub/ffmpeg
2. **Automatic Chunking**: Splits audio into 10-minute chunks (well under 25MB Whisper limit)
3. **Parallel Transcription**: Processes up to 3 chunks concurrently using `asyncio.Semaphore(3)`
4. **Timestamp Merging**: Adjusts segment timestamps when merging chunk transcripts
5. **Format Flexibility**: Auto-detects audio format, no manual conversion needed

## Prerequisites

**CRITICAL: Python 3.12 or earlier required**

pydub depends on `audioop` module, which was removed in Python 3.13. Check your version:

```bash
python3 --version  # Must be 3.12.x or earlier
```

**SYSTEM DEPENDENCY: ffmpeg required**

pydub uses ffmpeg for audio format conversion and decoding.

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Verify ffmpeg:**
```bash
ffmpeg -version
```

**Python dependencies:**
```bash
# If using uv (recommended)
uv sync

# Or with pip
pip install pydub openai
```

## How It Works

### Architecture

```
Audio Upload → pydub.AudioSegment.from_file()
                      ↓
        Split into 10-minute chunks
                      ↓
        Export chunks to temp MP3 files
                      ↓
    Parallel Whisper API calls (max 3 concurrent)
                      ↓
        Merge transcripts in order
                      ↓
    Adjust segment timestamps → Full transcript
```

### Whisper API File Size Limit

**CRITICAL: Whisper API has 25MB file size limit**

This example handles it automatically:

- **Chunk duration:** 10 minutes (600 seconds)
- **Typical MP3 bitrate:** 128kbps
- **10-minute chunk size:** ~9.4MB (well under 25MB)
- **Safety margin:** 2.65x headroom for higher bitrate audio

**Higher bitrate audio** (256kbps, 320kbps):
- 10-minute at 256kbps ≈ 18.8MB (still safe)
- 10-minute at 320kbps ≈ 23.4MB (still under limit)

### Parallel Processing Strategy

Uses `asyncio.Semaphore(3)` to limit concurrent API calls:

**Why 3 concurrent calls?**
- **API rate limits:** OpenAI Whisper typically allows ~50 req/min (varies by tier)
- **Cost control:** Limits parallel spending (each call costs money)
- **Optimal speed:** 3x speedup vs sequential, without overwhelming API

**Example:** 30-minute podcast:
- Sequential: ~15 minutes (Whisper real-time factor ≈ 0.5x)
- Parallel (3 concurrent): ~5 minutes (3x speedup)

### Response Format: verbose_json

Uses `response_format="verbose_json"` with `timestamp_granularities=["segment"]`:

**Returns:**
- `text`: Full transcript
- `duration`: Audio duration in seconds
- `segments`: Array of timestamped segments with `start`, `end`, `text`

**Why verbose_json?**
- Timestamps enable features like:
  - Jump to specific moments in audio
  - Generate subtitles (SRT, VTT)
  - Search transcript with time references
  - Highlight important segments

## Egress Rules

```python
@app.service(egress=["api.openai.com"])
```

Required for:
- OpenAI Whisper API transcription

## Secrets

Requires `OPENAI_API_KEY` from SecretsConnector:

```bash
# Set via environment variable
export OPENAI_API_KEY="sk-..."

# Or via Blazing secrets management
curl -X POST http://localhost:8000/secrets/set \
  -H "Content-Type: application/json" \
  -d '{"key": "OPENAI_API_KEY", "value": "sk-..."}'
```

Get API key from: https://platform.openai.com/api-keys

## Usage

### Quick Test (Standalone)

Run the example directly to test with generated audio:

```bash
cd examples/07-podcast-transcription
python3 flow.py
```

This will:
1. Generate 30 seconds of silent/tone audio
2. Transcribe it using Whisper API
3. Print transcript and metadata

**Note:** Whisper may return minimal transcript for silent audio (this is expected behavior).

### Via Blazing Service

Start the service:

```bash
python3 examples/07-podcast-transcription/flow.py &
```

**Transcribe an audio file:**

```bash
curl -X POST http://localhost:8000/transcribe \
  -F "file=@path/to/podcast.mp3"
```

Response:
```json
{
  "transcript": "Welcome to the podcast. Today we're discussing...",
  "duration_seconds": 1847.5,
  "chunks": 4,
  "segments": [
    {
      "start": 0.0,
      "end": 3.2,
      "text": "Welcome to the podcast."
    },
    {
      "start": 3.2,
      "end": 7.8,
      "text": "Today we're discussing..."
    }
  ],
  "metadata": {
    "audio_duration": 1847.5,
    "chunks_processed": 4,
    "segments_count": 142,
    "channels": 2,
    "frame_rate": 44100
  }
}
```

## Supported Audio Formats

pydub (via ffmpeg) supports all common audio formats:

| Format | Extension | Notes |
|--------|-----------|-------|
| MP3 | .mp3 | Most common podcast format |
| MP4 | .mp4, .m4a | AAC audio in MP4 container |
| WAV | .wav | Uncompressed, large files |
| FLAC | .flac | Lossless compression |
| OGG | .ogg | Vorbis codec |
| WebM | .webm | Opus codec |

**Auto-detection:** pydub automatically detects format from file header (not extension).

## Cost Estimates

Based on OpenAI Whisper pricing: **$0.006 per minute** of audio

| Audio Length | Chunks | API Calls | Cost |
|--------------|--------|-----------|------|
| 5 min | 1 | 1 | $0.03 |
| 30 min | 3 | 3 | $0.18 |
| 1 hour | 6 | 6 | $0.36 |
| 2 hours | 12 | 12 | $0.72 |

**Cost vs human transcription:**
- Human transcription: ~$1-2 per minute = $60-120 per hour
- Whisper API: $0.36 per hour
- **Savings: 99% cheaper than human transcription**

## Testing

Verify the example works:

```bash
# Check syntax
python3 -m py_compile examples/07-podcast-transcription/flow.py

# Verify critical patterns
grep -q "AudioSegment.from_file" examples/07-podcast-transcription/flow.py
grep -q "Semaphore(3)" examples/07-podcast-transcription/flow.py
grep -q "verbose_json" examples/07-podcast-transcription/flow.py

# Check ffmpeg dependency
ffmpeg -version

# Run integration test
python3 examples/07-podcast-transcription/flow.py
```

## Common Issues

### Issue: No audio file for testing

**Don't include large audio files in repo.** Instead:

**Option 1: Generate silent audio**
```python
from pydub import AudioSegment
AudioSegment.silent(duration=30*60*1000).export("test.mp3")
```

**Option 2: Download sample podcast**
```bash
# Public domain podcast from archive.org
curl -o test_podcast.mp3 "https://archive.org/download/sample_podcast/sample.mp3"
```

**Option 3: Use YouTube audio**
```bash
# Requires yt-dlp
yt-dlp -x --audio-format mp3 "https://youtube.com/watch?v=VIDEO_ID"
```

### Issue: ModuleNotFoundError: No module named 'audioop'

**Symptom:** Import error on Python 3.13+

**Cause:** `audioop` module was removed in Python 3.13, but pydub depends on it

**Fix:** Downgrade to Python 3.12:
```bash
pyenv install 3.12.0
pyenv local 3.12.0
```

### Issue: FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'

**Symptom:** pydub can't find ffmpeg

**Cause:** ffmpeg not installed or not in PATH

**Fix:** Install ffmpeg (see Prerequisites section)

**Verify fix:**
```bash
which ffmpeg
ffmpeg -version
```

### Issue: RuntimeWarning: Couldn't find ffprobe or avprobe

**Symptom:** pydub works but shows warning

**Cause:** ffprobe (part of ffmpeg) not in PATH

**Fix:** Same as ffmpeg issue - ensure full ffmpeg installation, not just binary

### Issue: Audio file too large (>25MB single chunk)

**Symptom:** `openai.error.InvalidRequestError: Audio file is too large`

**Cause:** High bitrate audio exceeds 25MB even for 10-minute chunks

**Fix:** Reduce chunk duration:
```python
# In flow.py, change chunk_duration_ms
chunk_duration_ms = 5 * 60 * 1000  # 5 minutes instead of 10
```

Or reduce audio bitrate before transcription:
```python
audio = AudioSegment.from_file(audio_path)
audio = audio.set_frame_rate(16000).set_channels(1)  # Mono, 16kHz (Whisper optimal)
```

### Issue: Rate limiting errors

**Symptom:** `openai.error.RateLimitError: Rate limit exceeded`

**Cause:** Too many parallel requests for your OpenAI tier

**Fix:** Reduce semaphore limit:
```python
self.transcription_semaphore = asyncio.Semaphore(1)  # Sequential instead of 3 concurrent
```

Or upgrade OpenAI account tier for higher rate limits.

## Advanced: Production Improvements

This example prioritizes clarity over production features. For production systems:

### 1. Progress Tracking

Add webhook or SSE for long transcription progress:

```python
async def transcribe_with_progress(audio_path: str, progress_callback):
    chunks = self._split_audio(audio)

    for i, chunk in enumerate(chunks):
        result = await self._transcribe_chunk(chunk, i)
        await progress_callback(i + 1, len(chunks), result)
```

### 2. Speaker Diarization

Whisper doesn't identify speakers. Integrate with speaker diarization services:

- **pyannote.audio** (open source)
- **AssemblyAI** (commercial, includes diarization)
- **Deepgram** (commercial, real-time diarization)

### 3. Subtitle Generation

Convert segments to SRT/VTT format:

```python
def segments_to_srt(segments):
    srt_lines = []
    for i, segment in enumerate(segments, start=1):
        start = format_timestamp(segment['start'])
        end = format_timestamp(segment['end'])
        srt_lines.append(f"{i}\n{start} --> {end}\n{segment['text']}\n")
    return "\n".join(srt_lines)
```

### 4. Audio Preprocessing

Optimize audio for Whisper before transcription:

```python
# Whisper optimal settings: mono, 16kHz
audio = AudioSegment.from_file(audio_path)
audio = audio.set_frame_rate(16000)  # Whisper's sample rate
audio = audio.set_channels(1)  # Mono (reduces file size, Whisper trained on mono)
```

**Benefits:**
- Smaller file size (faster upload)
- Better Whisper accuracy (matches training data)
- Lower costs (smaller files, fewer chunks)

### 5. Language Detection

Auto-detect audio language before transcription:

```python
# First pass: detect language with small sample
sample = audio[:30000]  # First 30 seconds
sample_path = "/tmp/sample.mp3"
sample.export(sample_path, format="mp3")

with open(sample_path, 'rb') as f:
    result = await self.openai.transcribe(f, model="whisper-1")

language = result.get('language', 'en')
logger.info(f"Detected language: {language}")

# Second pass: transcribe with detected language
result = await self.openai.transcribe(
    audio_file=audio_file,
    model="whisper-1",
    language=language  # Improves accuracy
)
```

### 6. Caching

Cache transcripts to avoid re-transcribing:

```python
import hashlib

# Generate audio file hash
with open(audio_path, 'rb') as f:
    audio_hash = hashlib.sha256(f.read()).hexdigest()

# Check cache
cached = await redis.get(f"transcript:{audio_hash}")
if cached:
    return json.loads(cached)

# Transcribe and cache
result = await self.transcribe(audio_path)
await redis.set(f"transcript:{audio_hash}", json.dumps(result), ex=86400*7)  # Cache 7 days
```

## References

- [OpenAI Whisper API Documentation](https://platform.openai.com/docs/guides/speech-to-text)
- [pydub Documentation](https://github.com/jiaaro/pydub)
- [ffmpeg Download](https://ffmpeg.org/download.html)
- [Whisper Model Card](https://github.com/openai/whisper/blob/main/model-card.md)
