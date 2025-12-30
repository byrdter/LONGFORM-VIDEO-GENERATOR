"""
utils.py - Shared utilities for the longform video generator.

Provides common functions for file operations, duration detection, and validation.
"""

import json
import subprocess
import shutil
from pathlib import Path
from typing import Optional


def get_ffmpeg_path() -> Optional[str]:
    """Find FFmpeg executable path."""
    # Check PATH first
    path = shutil.which("ffmpeg")
    if path:
        return path

    # Check common locations on macOS
    common_paths = [
        "/opt/homebrew/bin/ffmpeg",
        "/usr/local/bin/ffmpeg",
        "/usr/bin/ffmpeg",
    ]
    for p in common_paths:
        if Path(p).exists():
            return p

    return None


def get_ffprobe_path() -> Optional[str]:
    """Find ffprobe executable path."""
    # Check PATH first
    path = shutil.which("ffprobe")
    if path:
        return path

    # Check common locations on macOS
    common_paths = [
        "/opt/homebrew/bin/ffprobe",
        "/usr/local/bin/ffprobe",
        "/usr/bin/ffprobe",
    ]
    for p in common_paths:
        if Path(p).exists():
            return p

    return None


def check_ffmpeg() -> bool:
    """Check if FFmpeg is available on the system."""
    return get_ffmpeg_path() is not None


def check_ffprobe() -> bool:
    """Check if ffprobe is available on the system."""
    return get_ffprobe_path() is not None


def get_audio_duration(audio_path: str) -> float:
    """
    Get the duration of an audio file in seconds using ffprobe.

    Args:
        audio_path: Path to the audio file

    Returns:
        Duration in seconds as a float
    """
    ffprobe = get_ffprobe_path()
    if not ffprobe:
        raise RuntimeError("ffprobe not found")

    cmd = [
        ffprobe,
        "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())


def get_video_duration(video_path: str) -> float:
    """
    Get the duration of a video file in seconds using ffprobe.

    Args:
        video_path: Path to the video file

    Returns:
        Duration in seconds as a float
    """
    ffprobe = get_ffprobe_path()
    if not ffprobe:
        raise RuntimeError("ffprobe not found")

    cmd = [
        ffprobe,
        "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())


def load_segments(segments_file: str) -> dict:
    """
    Load and parse a segments.json file.

    Args:
        segments_file: Path to the segments.json file

    Returns:
        Parsed JSON as a dictionary
    """
    with open(segments_file, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dir(path: Path) -> Path:
    """
    Create a directory if it doesn't exist.

    Args:
        path: Path to the directory

    Returns:
        The path object
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_all_segments(data: dict) -> list:
    """
    Extract all segments from a segments.json structure.

    Args:
        data: Parsed segments.json dictionary

    Returns:
        List of tuples: (segment, chapter) for each segment
    """
    segments = []
    for chapter in data.get("chapters", []):
        for segment in chapter.get("segments", []):
            segments.append((segment, chapter))
    return segments


def should_use_ken_burns(segment: dict, chapter: dict) -> bool:
    """
    Determine if Ken Burns effects should be applied to a segment.

    Args:
        segment: The segment dictionary
        chapter: The parent chapter dictionary

    Returns:
        True if Ken Burns effects should be applied
    """
    # Check chapter-level setting first
    if not chapter.get("ken_burns_enabled", True):
        return False

    # Check segment-level setting
    ken_burns_sequence = segment.get("ken_burns_sequence", [])
    if not ken_burns_sequence:
        return False

    return True


def format_timestamp(seconds: float) -> str:
    """
    Format seconds as HH:MM:SS for YouTube chapters.

    Args:
        seconds: Time in seconds

    Returns:
        Formatted timestamp string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"
