# CLAUDE.md - Project Instructions for Claude Code

## Project Overview

This is a **Long-Form Video Generator** for creating 30+ minute documentary-style videos using AI-generated content. The system produces still-image-based videos with Ken Burns effects, AI voiceover, and background music.

**Target Use Cases:**
- Historical documentaries (e.g., "The Fall of Rome", "The Space Race")
- Futuristic/speculative narratives (e.g., "Mars Colony 2150", "The AI Revolution")
- Educational content (e.g., "How the Internet Works", "The History of Mathematics")

## Architecture Philosophy

Following the "Smart Agents + Dumb Code" pattern from the pokemon-ai-video-generator repo:

- **Smart Agents**: AI prompts that read files, make decisions, extract information
- **Dumb Code**: Simple Python scripts that take complete inputs and call one API

Each script should do ONE thing well:
- `generate_image.py` → Takes prompt, outputs image
- `generate_voice.py` → Takes text, outputs audio
- `create_segment.py` → Takes image + audio, outputs video clip
- `assemble_video.py` → Takes clips, outputs final video

## Tech Stack

| Component | Technology | Notes |
|-----------|------------|-------|
| Language | Python 3.10+ | Use type hints throughout |
| Package Manager | uv | Fast, reliable Python package management |
| Image Generation | Gemini API (Imagen 3) | Free tier, use `google-generativeai` |
| Voice Generation | Edge TTS | Completely free, use `edge-tts` |
| Video Processing | FFmpeg | Must be installed on system |
| Configuration | python-dotenv | For API keys |

## Project Structure

```
longform-video-generator/
├── CLAUDE.md                 # This file - project instructions
├── README.md                 # User-facing documentation
├── PRD.md                    # Product requirements document
├── pyproject.toml            # Python dependencies (uv)
├── .env.example              # Template for API keys
│
├── scripts/                  # Core Python tools
│   ├── __init__.py
│   ├── generate_image.py     # Gemini API wrapper
│   ├── generate_voice.py     # Edge TTS wrapper
│   ├── create_segment.py     # Ken Burns + audio merge
│   ├── assemble_video.py     # Final concatenation
│   └── utils.py              # Shared utilities
│
├── prompts/                  # AI prompts for content generation
│   ├── 1_script_generator.md
│   ├── 2_segment_planner.md
│   └── 3_image_prompt_generator.md
│
├── music/                    # Royalty-free background tracks
│   └── .gitkeep
│
└── projects/                 # Generated project folders
    └── example_project/
        ├── script.md
        ├── segments.json
        ├── images/
        ├── audio/
        ├── clips/
        └── final_video.mp4
```

## Key Data Structures

### segments.json Schema

```json
{
  "project_name": "string",
  "voice": "string (edge-tts voice name)",
  "chapters": [
    {
      "chapter_id": "number",
      "title": "string",
      "music_track": "string (filename in music/)",
      "music_volume": "number (0.0-1.0, recommend 0.10-0.20)",
      "ken_burns_enabled": "boolean (optional, default true - set false for static images)",
      "segments": [
        {
          "segment_id": "string (e.g., '001')",
          "narration": "string (text to speak)",
          "image_prompt": "string (Gemini image prompt)",
          "ken_burns_sequence": ["array of effect names, or empty [] for static image"],
          "transition": "string: 'cut' | 'fade' | 'crossfade'"
        }
      ]
    }
  ]
}
```

**Static Images:** To use static images without Ken Burns effects:
- Per-segment: Use `"ken_burns_sequence": []` or omit the field
- Per-chapter: Set `"ken_burns_enabled": false` (applies to all segments in chapter)

### Ken Burns Effects Available

- `zoom_in` - Slow zoom into center (reveals, emphasis)
- `zoom_out` - Slow zoom out (establishing shots, endings)
- `pan_left` - Pan left to right (landscapes, movement)
- `pan_right` - Pan right to left
- `pan_up` - Tilt upward (tall structures, sky)
- `pan_down` - Tilt downward (reveals from above)

## Development Guidelines

### When Writing Scripts

1. **Always include CLI interface** using `argparse`
2. **Support both single-item and batch modes**
3. **Skip existing files** in batch mode (idempotent)
4. **Print progress** to stdout
5. **Use pathlib.Path** for all file operations
6. **Handle errors gracefully** with informative messages

### Script Template

```python
"""
script_name.py - Brief description

Longer description of what this script does.
"""

import argparse
from pathlib import Path

def main_function(input_path: str, output_path: str, **kwargs):
    """Main logic here."""
    pass

def batch_process(config_file: str, output_dir: str, **kwargs):
    """Process multiple items from a config file."""
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brief description")
    subparsers = parser.add_subparsers(dest="command")
    
    # Single item
    single = subparsers.add_parser("single", help="Process single item")
    single.add_argument("--input", required=True)
    single.add_argument("--output", required=True)
    
    # Batch mode
    batch = subparsers.add_parser("batch", help="Batch process from config")
    batch.add_argument("--config", required=True)
    batch.add_argument("--output-dir", required=True)
    
    args = parser.parse_args()
    
    if args.command == "single":
        main_function(args.input, args.output)
    elif args.command == "batch":
        batch_process(args.config, args.output_dir)
    else:
        parser.print_help()
```

### FFmpeg Notes

- Always use `-y` flag to overwrite without prompting
- Output format: 1920x1080 (16:9), 30fps, H.264, AAC audio
- Use `ffprobe` to get audio/video duration
- Ken Burns uses the `zoompan` filter

### Edge TTS Notes

- Async library - use `asyncio.run()` for sync wrapper
- Recommended voices:
  - `en-GB-RyanNeural` - British male (historical)
  - `en-US-GuyNeural` - American male (general)
  - `en-US-AriaNeural` - American female (expressive)
- Rate adjustment: `"-10%"` slower, `"+10%"` faster

### Gemini API Notes

- Use `google-generativeai` package
- Model for images: `imagen-3.0-generate-001`
- Always specify `aspect_ratio="16:9"` for video
- Include style keywords: "photorealistic", "cinematic lighting"

## Testing Commands

```bash
# Test image generation
python scripts/generate_image.py single \
    --prompt "Ancient Roman forum at sunset, photorealistic, 16:9" \
    --output test_image.png

# Test voice generation
python scripts/generate_voice.py single \
    --text "At its height, the Roman Empire stretched across three continents." \
    --output test_voice.mp3 \
    --voice en-GB-RyanNeural

# Test segment creation
python scripts/create_segment.py single \
    --image test_image.png \
    --audio test_voice.mp3 \
    --output test_segment.mp4 \
    --effects zoom_in pan_left

# Test full assembly
python scripts/assemble_video.py \
    --clips-dir projects/test/clips \
    --output projects/test/final.mp4
```

## Current Development Status

See `tasks.md` for current progress and next steps.

## Common Issues & Solutions

### FFmpeg not found
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Edge TTS timeout
- Large text blocks may timeout
- Split into smaller chunks (<500 words per call)

### Gemini API rate limits
- Free tier has limits
- Add delays between batch requests if hitting limits

## Reference Materials

- Original pokemon-ai-video-generator: https://github.com/bhancockio/pokemon-ai-video-generator
- Edge TTS voices list: Run `edge-tts --list-voices`
- FFmpeg zoompan filter docs: https://ffmpeg.org/ffmpeg-filters.html#zoompan
- Gemini API docs: https://ai.google.dev/docs
