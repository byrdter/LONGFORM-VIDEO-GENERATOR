"""
create_segment.py - Create video segments from images and audio.

Combines a still image with audio narration, optionally applying Ken Burns effects.
Uses FFmpeg for video processing.
"""

import argparse
import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv

from utils import (
    load_segments,
    ensure_dir,
    get_all_segments,
    get_audio_duration,
    should_use_ken_burns,
    check_ffmpeg,
    get_ffmpeg_path,
)


# Ken Burns effect parameters
# Each effect defines: start_zoom, end_zoom, start_x, end_x, start_y, end_y
# Coordinates are relative (0-1) where 0.5 is center
KEN_BURNS_EFFECTS = {
    "zoom_in": {
        "start_zoom": 1.0,
        "end_zoom": 1.3,
        "start_x": 0.5,
        "end_x": 0.5,
        "start_y": 0.5,
        "end_y": 0.5,
    },
    "zoom_out": {
        "start_zoom": 1.3,
        "end_zoom": 1.0,
        "start_x": 0.5,
        "end_x": 0.5,
        "start_y": 0.5,
        "end_y": 0.5,
    },
    "pan_left": {
        "start_zoom": 1.2,
        "end_zoom": 1.2,
        "start_x": 0.7,
        "end_x": 0.3,
        "start_y": 0.5,
        "end_y": 0.5,
    },
    "pan_right": {
        "start_zoom": 1.2,
        "end_zoom": 1.2,
        "start_x": 0.3,
        "end_x": 0.7,
        "start_y": 0.5,
        "end_y": 0.5,
    },
    "pan_up": {
        "start_zoom": 1.2,
        "end_zoom": 1.2,
        "start_x": 0.5,
        "end_x": 0.5,
        "start_y": 0.7,
        "end_y": 0.3,
    },
    "pan_down": {
        "start_zoom": 1.2,
        "end_zoom": 1.2,
        "start_x": 0.5,
        "end_x": 0.5,
        "start_y": 0.3,
        "end_y": 0.7,
    },
}


def build_zoompan_filter(effect_name: str, duration: float, fps: int = 30) -> str:
    """
    Build FFmpeg zoompan filter string for a Ken Burns effect.

    Args:
        effect_name: Name of the effect (zoom_in, pan_left, etc.)
        duration: Duration in seconds
        fps: Frames per second

    Returns:
        FFmpeg filter string
    """
    effect = KEN_BURNS_EFFECTS.get(effect_name)
    if not effect:
        # Default to static if unknown effect
        return f"zoompan=z=1:d={int(duration * fps)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={fps}"

    total_frames = int(duration * fps)

    # Calculate zoom interpolation
    sz = effect["start_zoom"]
    ez = effect["end_zoom"]

    # Calculate position interpolation (in pixels, relative to zoomed frame)
    # x and y represent the top-left corner of the output frame
    sx = effect["start_x"]
    ex = effect["end_x"]
    sy = effect["start_y"]
    ey = effect["end_y"]

    # Build the zoompan filter with linear interpolation
    # zoom goes from sz to ez
    # x/y position is calculated to keep the focal point centered
    zoom_expr = f"{sz}+({ez}-{sz})*on/{total_frames}"
    x_expr = f"iw*({sx}+({ex}-{sx})*on/{total_frames})-iw/zoom/2"
    y_expr = f"ih*({sy}+({ey}-{sy})*on/{total_frames})-ih/zoom/2"

    return f"zoompan=z='{zoom_expr}':x='{x_expr}':y='{y_expr}':d={total_frames}:s=1920x1080:fps={fps}"


def create_segment(
    image_path: str,
    audio_path: str,
    output_path: str,
    effects: list = None,
    music_path: str = None,
    music_volume: float = 0.15,
    padding_start: float = 0.5,
    padding_end: float = 0.5,
) -> bool:
    """
    Create a video segment from an image and audio file.

    Args:
        image_path: Path to the image file
        audio_path: Path to the audio file
        output_path: Path for the output video
        effects: List of Ken Burns effects to apply (empty = static image)
        music_path: Optional path to background music
        music_volume: Volume of background music (0.0-1.0)
        padding_start: Seconds of padding before narration
        padding_end: Seconds of padding after narration

    Returns:
        True if successful, False otherwise
    """
    ffmpeg = get_ffmpeg_path()
    if not ffmpeg:
        print("Error: FFmpeg not found. Please install FFmpeg.")
        return False

    # Get audio duration
    audio_duration = get_audio_duration(audio_path)
    total_duration = audio_duration + padding_start + padding_end

    fps = 30
    effects = effects or []

    # Build video filter
    if effects:
        # Split duration among effects
        effect_duration = total_duration / len(effects)
        filters = []
        for effect in effects:
            filters.append(build_zoompan_filter(effect, effect_duration, fps))

        # For multiple effects, we'd need to concat them, but for simplicity
        # we'll just use the first effect for the full duration
        if len(effects) == 1:
            video_filter = filters[0]
        else:
            # Use first effect - TODO: implement effect chaining
            video_filter = build_zoompan_filter(effects[0], total_duration, fps)
    else:
        # Static image - just scale to 1920x1080
        total_frames = int(total_duration * fps)
        video_filter = f"zoompan=z=1:d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={fps}"

    try:
        if music_path and Path(music_path).exists():
            # With background music
            # Create audio mix: narration (delayed by padding_start) + music
            cmd = [
                ffmpeg, "-y",
                "-loop", "1",
                "-i", image_path,
                "-i", audio_path,
                "-i", music_path,
                "-filter_complex",
                f"[0:v]{video_filter},format=yuv420p[v];"
                f"[1:a]adelay={int(padding_start * 1000)}|{int(padding_start * 1000)}[narration];"
                f"[2:a]volume={music_volume},aloop=loop=-1:size=2e+09[music];"
                f"[narration][music]amix=inputs=2:duration=first:dropout_transition=2[a]",
                "-map", "[v]",
                "-map", "[a]",
                "-t", str(total_duration),
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                output_path
            ]
        else:
            # Without background music
            cmd = [
                ffmpeg, "-y",
                "-loop", "1",
                "-i", image_path,
                "-i", audio_path,
                "-filter_complex",
                f"[0:v]{video_filter},format=yuv420p[v];"
                f"[1:a]adelay={int(padding_start * 1000)}|{int(padding_start * 1000)},apad=pad_dur={padding_end}[a]",
                "-map", "[v]",
                "-map", "[a]",
                "-t", str(total_duration),
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "192k",
                output_path
            ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"  FFmpeg error: {result.stderr}")
            return False

        return True

    except Exception as e:
        print(f"  Error creating segment: {e}")
        return False


def batch_create(
    segments_file: str,
    images_dir: str,
    audio_dir: str,
    output_dir: str,
    music_dir: str = None,
) -> None:
    """
    Create video segments for all entries in segments.json.

    Args:
        segments_file: Path to segments.json
        images_dir: Directory containing images
        audio_dir: Directory containing audio files
        output_dir: Directory to save video segments
        music_dir: Directory containing music files
    """
    # Load environment defaults
    load_dotenv()
    padding_start = float(os.getenv("DEFAULT_PADDING_START", "0.5"))
    padding_end = float(os.getenv("DEFAULT_PADDING_END", "0.5"))
    default_music_volume = float(os.getenv("DEFAULT_MUSIC_VOLUME", "0.15"))

    data = load_segments(segments_file)
    output_path = ensure_dir(Path(output_dir))
    images_path = Path(images_dir)
    audio_path = Path(audio_dir)
    music_path = Path(music_dir) if music_dir else None

    segments = get_all_segments(data)
    total = len(segments)

    print(f"Creating {total} video segments...")

    for i, (segment, chapter) in enumerate(segments, 1):
        segment_id = segment["segment_id"]
        video_file = output_path / f"{segment_id}.mp4"

        # Skip if already exists
        if video_file.exists():
            print(f"[{i}/{total}] Skipping {segment_id} (already exists)")
            continue

        image_file = images_path / f"{segment_id}.png"
        audio_file = audio_path / f"{segment_id}.mp3"

        if not image_file.exists():
            print(f"[{i}/{total}] Skipping {segment_id} (image not found)")
            continue

        if not audio_file.exists():
            print(f"[{i}/{total}] Skipping {segment_id} (audio not found)")
            continue

        print(f"[{i}/{total}] Creating {segment_id}...")

        # Determine Ken Burns effects
        if should_use_ken_burns(segment, chapter):
            effects = segment.get("ken_burns_sequence", [])
        else:
            effects = []

        # Get music settings
        music_file = None
        music_volume = default_music_volume

        music_track = chapter.get("music_track")
        if music_track and music_path:
            potential_music = music_path / music_track
            if potential_music.exists():
                music_file = str(potential_music)
                music_volume = chapter.get("music_volume", default_music_volume)

        success = create_segment(
            str(image_file),
            str(audio_file),
            str(video_file),
            effects=effects,
            music_path=music_file,
            music_volume=music_volume,
            padding_start=padding_start,
            padding_end=padding_end,
        )

        if success:
            print(f"  Saved to {video_file}")
        else:
            print(f"  Failed to create {segment_id}")

    print("Done!")


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Create video segments from images and audio"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Single segment
    single = subparsers.add_parser("single", help="Create a single segment")
    single.add_argument("--image", required=True, help="Path to image file")
    single.add_argument("--audio", required=True, help="Path to audio file")
    single.add_argument("--output", required=True, help="Output video path")
    single.add_argument("--effects", nargs="*", default=[], help="Ken Burns effects")
    single.add_argument("--music", help="Path to background music")
    single.add_argument("--music-volume", type=float, default=0.15, help="Music volume")

    # Batch mode
    batch = subparsers.add_parser("batch", help="Batch create from segments.json")
    batch.add_argument("--segments", required=True, help="Path to segments.json")
    batch.add_argument("--images-dir", required=True, help="Directory with images")
    batch.add_argument("--audio-dir", required=True, help="Directory with audio")
    batch.add_argument("--output-dir", required=True, help="Output directory")
    batch.add_argument("--music-dir", help="Directory with music files")

    args = parser.parse_args()

    if args.command == "single":
        print("Creating segment...")
        success = create_segment(
            args.image,
            args.audio,
            args.output,
            effects=args.effects,
            music_path=args.music,
            music_volume=args.music_volume,
        )
        if success:
            print(f"Saved to {args.output}")
        else:
            print("Failed to create segment")

    elif args.command == "batch":
        batch_create(
            args.segments,
            args.images_dir,
            args.audio_dir,
            args.output_dir,
            args.music_dir,
        )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
