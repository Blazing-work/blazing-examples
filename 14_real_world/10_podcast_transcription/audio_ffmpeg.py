"""
FFmpeg-based audio utilities for Python 3.13+ compatibility.

Replaces pydub (which depends on audioop, removed in Python 3.13).
Uses ffmpeg/ffprobe subprocess calls for audio processing.
"""
from __future__ import annotations
import json
import math
import shutil
import subprocess
from pathlib import Path
from typing import List


def _require_bin(name: str) -> str:
    """Check if binary exists in PATH."""
    p = shutil.which(name)
    if not p:
        raise RuntimeError(
            f"Missing dependency: {name}. "
            f"Install ffmpeg: https://ffmpeg.org/download.html"
        )
    return p


def audio_duration_seconds(in_path: str | Path) -> float:
    """
    Get audio duration in seconds using ffprobe.

    Args:
        in_path: Path to audio file

    Returns:
        Duration in seconds

    Raises:
        RuntimeError: If ffprobe not found
        subprocess.CalledProcessError: If ffprobe fails
    """
    ffprobe = _require_bin("ffprobe")
    in_path = str(in_path)

    cmd = [
        ffprobe, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        in_path
    ]

    out = subprocess.check_output(cmd, text=True)
    data = json.loads(out)
    return float(data["format"]["duration"])


def split_audio(
    in_path: str | Path,
    out_dir: str | Path,
    chunk_seconds: float,
    out_ext: str = "mp3",
    bitrate: str = "128k",
    sample_rate: int = 16000,
    mono: bool = True,
) -> List[Path]:
    """
    Split audio file into chunks using ffmpeg.

    Args:
        in_path: Path to input audio file
        out_dir: Directory for output chunks
        chunk_seconds: Length of each chunk in seconds
        out_ext: Output format extension (default: mp3)
        bitrate: Audio bitrate (default: 128k for MP3)
        sample_rate: Sample rate in Hz (default: 16000 for Whisper)
        mono: Convert to mono (default: True)

    Returns:
        List of paths to output chunks

    Raises:
        RuntimeError: If ffmpeg not found
        subprocess.CalledProcessError: If ffmpeg fails
    """
    ffmpeg = _require_bin("ffmpeg")
    in_path = Path(in_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Get total duration
    dur = audio_duration_seconds(in_path)
    n_chunks = int(math.ceil(dur / chunk_seconds))
    outputs: List[Path] = []

    for i in range(n_chunks):
        start = i * chunk_seconds
        length = min(chunk_seconds, dur - start)
        out_path = out_dir / f"{in_path.stem}_part{i:04d}.{out_ext}"

        # Build ffmpeg command for chunk extraction
        cmd = [
            ffmpeg, "-v", "error",
            "-ss", f"{start:.3f}",  # Start time
            "-t", f"{length:.3f}",   # Duration
            "-i", str(in_path),
            "-vn",                   # No video
            "-ac", "1" if mono else "2",  # Audio channels
            "-ar", str(sample_rate),      # Sample rate
        ]

        # Add codec/bitrate based on format
        if out_ext == "mp3":
            cmd.extend(["-codec:a", "libmp3lame", "-b:a", bitrate])
        elif out_ext == "wav":
            cmd.extend(["-codec:a", "pcm_s16le"])

        cmd.append(str(out_path))

        subprocess.check_call(cmd)
        outputs.append(out_path)

    return outputs


def create_silent_audio(
    out_path: str | Path,
    duration_seconds: float,
    sample_rate: int = 16000,
    format: str = "mp3",
    bitrate: str = "128k"
) -> Path:
    """
    Create silent audio file using ffmpeg.

    Useful for testing without needing real audio files.

    Args:
        out_path: Path for output file
        duration_seconds: Duration in seconds
        sample_rate: Sample rate in Hz (default: 16000)
        format: Output format (default: mp3)
        bitrate: Bitrate for compressed formats (default: 128k)

    Returns:
        Path to created file

    Raises:
        RuntimeError: If ffmpeg not found
        subprocess.CalledProcessError: If ffmpeg fails
    """
    ffmpeg = _require_bin("ffmpeg")
    out_path = Path(out_path)

    cmd = [
        ffmpeg, "-v", "error",
        "-f", "lavfi",
        "-i", f"anullsrc=r={sample_rate}:cl=mono",
        "-t", str(duration_seconds),
    ]

    # Add codec/bitrate based on format
    if format == "mp3":
        cmd.extend(["-codec:a", "libmp3lame", "-b:a", bitrate])
    elif format == "wav":
        cmd.extend(["-codec:a", "pcm_s16le"])

    cmd.append(str(out_path))

    subprocess.check_call(cmd)
    return out_path


def get_audio_info(in_path: str | Path) -> dict:
    """
    Get comprehensive audio file information using ffprobe.

    Args:
        in_path: Path to audio file

    Returns:
        Dictionary with audio metadata (duration, sample_rate, channels, etc.)

    Raises:
        RuntimeError: If ffprobe not found
        subprocess.CalledProcessError: If ffprobe fails
    """
    ffprobe = _require_bin("ffprobe")
    in_path = str(in_path)

    cmd = [
        ffprobe, "-v", "error",
        "-show_entries", "format=duration:stream=sample_rate,channels,codec_name",
        "-of", "json",
        in_path
    ]

    out = subprocess.check_output(cmd, text=True)
    data = json.loads(out)

    # Extract relevant info
    format_info = data.get("format", {})
    stream_info = data.get("streams", [{}])[0]

    return {
        "duration": float(format_info.get("duration", 0)),
        "sample_rate": int(stream_info.get("sample_rate", 0)),
        "channels": int(stream_info.get("channels", 0)),
        "codec": stream_info.get("codec_name", "unknown")
    }
