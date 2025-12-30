"""
assemble_video.py - Assemble video segments into final video.

Concatenates all video segments into a single final video using FFmpeg.
Also generates YouTube chapter markers file.
"""

import argparse
import subprocess
import tempfile
from pathlib import Path

from utils import (
    load_segments,
    ensure_dir,
    get_all_segments,
    get_video_duration,
    format_timestamp,
    check_ffmpeg,
    get_ffmpeg_path,
)


def assemble_video(clips_dir: str, output_path: str, segments_file: str = None) -> bool:
    """
    Assemble video segments into a final video.

    Args:
        clips_dir: Directory containing video segments
        output_path: Path for the final video
        segments_file: Optional segments.json for ordering and chapter markers

    Returns:
        True if successful, False otherwise
    """
    ffmpeg = get_ffmpeg_path()
    if not ffmpeg:
        print("Error: FFmpeg not found. Please install FFmpeg.")
        return False

    clips_path = Path(clips_dir)
    output = Path(output_path)
    ensure_dir(output.parent)

    # Get list of clips
    if segments_file:
        # Use segments.json for ordering
        data = load_segments(segments_file)
        segments = get_all_segments(data)
        clip_files = []
        for segment, chapter in segments:
            clip_file = clips_path / f"{segment['segment_id']}.mp4"
            if clip_file.exists():
                clip_files.append(clip_file)
            else:
                print(f"Warning: Missing clip {clip_file}")
    else:
        # Just sort by filename
        clip_files = sorted(clips_path.glob("*.mp4"))

    if not clip_files:
        print("Error: No video clips found")
        return False

    print(f"Assembling {len(clip_files)} clips...")

    # Create concat file for FFmpeg
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        for clip in clip_files:
            # FFmpeg concat requires escaped paths
            escaped_path = str(clip.absolute()).replace("'", "'\\''")
            f.write(f"file '{escaped_path}'\n")
        concat_file = f.name

    try:
        # Use FFmpeg concat demuxer
        cmd = [
            ffmpeg, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            str(output)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            return False

        # Generate chapter markers if segments.json provided
        if segments_file:
            generate_chapters(clips_dir, segments_file, str(output))

        return True

    except Exception as e:
        print(f"Error assembling video: {e}")
        return False

    finally:
        # Clean up temp file
        Path(concat_file).unlink(missing_ok=True)


def generate_chapters(clips_dir: str, segments_file: str, output_path: str) -> None:
    """
    Generate YouTube chapter markers file.

    Args:
        clips_dir: Directory containing video segments
        segments_file: Path to segments.json
        output_path: Path to the output video (chapters file will be alongside)
    """
    data = load_segments(segments_file)
    clips_path = Path(clips_dir)
    output = Path(output_path)

    chapters_file = output.with_suffix(".chapters.txt")

    chapters = []
    current_time = 0.0

    for chapter in data.get("chapters", []):
        chapter_title = chapter.get("title", f"Chapter {chapter.get('chapter_id', '?')}")
        chapter_start = current_time

        # Calculate chapter duration from its segments
        for segment in chapter.get("segments", []):
            clip_file = clips_path / f"{segment['segment_id']}.mp4"
            if clip_file.exists():
                duration = get_video_duration(str(clip_file))
                current_time += duration

        chapters.append((chapter_start, chapter_title))

    # Write chapters file
    with open(chapters_file, "w") as f:
        f.write("YouTube Chapters:\n\n")
        for timestamp, title in chapters:
            f.write(f"{format_timestamp(timestamp)} {title}\n")

    print(f"Chapter markers saved to {chapters_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Assemble video segments into final video"
    )

    parser.add_argument("--clips-dir", required=True, help="Directory with video clips")
    parser.add_argument("--output", required=True, help="Output video path")
    parser.add_argument("--segments", help="Path to segments.json (for ordering and chapters)")

    args = parser.parse_args()

    print("Assembling final video...")
    success = assemble_video(args.clips_dir, args.output, args.segments)

    if success:
        print(f"Final video saved to {args.output}")
    else:
        print("Failed to assemble video")


if __name__ == "__main__":
    main()
