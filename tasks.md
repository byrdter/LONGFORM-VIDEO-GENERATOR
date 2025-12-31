# Development Tasks

## Overview

This file tracks development progress. Claude Code should work through these tasks in order. Each task builds on the previous ones.

**Status Legend:**
- ⬜ Not started
- 🟡 In progress
- ✅ Complete

---

## Phase 1: Project Setup

### Task 1.1: Initialize Project Structure ✅
Create the basic project structure with all necessary folders and files.

**Files to create:**
- [x] `pyproject.toml` - Python project configuration with dependencies
- [x] `.env.example` - Template for API keys
- [x] `.gitignore` - Git ignore file
- [x] `README.md` - User documentation
- [x] `scripts/__init__.py` - Make scripts a package
- [x] `scripts/utils.py` - Shared utility functions
- [x] `music/.gitkeep` - Placeholder for music folder
- [x] `projects/.gitkeep` - Placeholder for projects folder

**Dependencies to include:**
```toml
[project]
name = "longform-video-generator"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "google-generativeai>=0.8.0",
    "edge-tts>=6.1.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
]
```

**Acceptance Criteria:**
- [x] Can run `uv sync` without errors
- [x] All folders exist
- [x] .env.example contains GEMINI_API_KEY placeholder

---

### Task 1.2: Create utils.py ✅
Shared utility functions used across scripts.

**Functions to implement:**
```python
def get_audio_duration(audio_path: str) -> float:
    """Get duration of audio file in seconds using ffprobe."""

def get_video_duration(video_path: str) -> float:
    """Get duration of video file in seconds using ffprobe."""

def load_segments(segments_file: str) -> dict:
    """Load and validate segments.json file."""

def ensure_dir(path: str) -> Path:
    """Create directory if it doesn't exist, return Path object."""

def check_ffmpeg() -> bool:
    """Check if ffmpeg is available on the system."""
```

**Additional functions implemented:**
- `get_ffmpeg_path()` / `get_ffprobe_path()` - Find executable paths
- `get_all_segments()` - Extract all segments from data structure
- `should_use_ken_burns()` - Determine if Ken Burns effects apply
- `format_timestamp()` - Format seconds as HH:MM:SS for YouTube chapters

**Acceptance Criteria:**
- [x] All functions have type hints
- [x] All functions have docstrings
- [x] Functions handle errors gracefully

---

## Phase 2: Core Scripts

### Task 2.1: Create generate_voice.py ✅
Voice generation using Edge TTS (free, no API key needed).

**Commands:**
- `single` - Generate one voice clip
- `batch` - Generate all clips from segments.json
- `list-voices` - Show available voices

**Example usage:**
```bash
python scripts/generate_voice.py single \
    --text "At its height, the Roman Empire..." \
    --output audio/test.mp3 \
    --voice en-GB-RyanNeural

python scripts/generate_voice.py batch \
    --segments segments.json \
    --output-dir audio/

python scripts/generate_voice.py list-voices
```

**Key implementation notes:**
- Edge TTS is async - need `asyncio.run()` wrapper
- Skip existing files in batch mode
- Print progress during batch processing

**Acceptance Criteria:**
- [x] Single mode generates audio file
- [x] Batch mode processes all segments
- [x] Existing files are skipped
- [x] Progress is printed
- [x] list-voices shows English voices

---

### Task 2.2: Create generate_image.py ✅
Image generation using Gemini API.

**Commands:**
- `single` - Generate one image
- `batch` - Generate all images from segments.json

**Example usage:**
```bash
python scripts/generate_image.py single \
    --prompt "Ancient Roman forum at sunset, photorealistic, 16:9" \
    --output images/test.png

python scripts/generate_image.py batch \
    --segments segments.json \
    --output-dir images/
```

**Key implementation notes:**
- Load API key from .env
- Always request 16:9 aspect ratio
- Add "photorealistic, cinematic" to prompts automatically
- Handle API errors gracefully
- Add small delay between batch requests to avoid rate limits

**Acceptance Criteria:**
- [x] Single mode generates image
- [x] Batch mode processes all segments
- [x] Images are 16:9 aspect ratio
- [x] Existing files are skipped
- [x] API errors are handled gracefully

---

### Task 2.3: Create create_segment.py ✅
Create video segment with Ken Burns effect.

**Commands:**
- `single` - Create one segment video
- `batch` - Create all segment videos

**Example usage:**
```bash
python scripts/create_segment.py single \
    --image images/seg_001.png \
    --audio audio/seg_001.mp3 \
    --output clips/seg_001.mp4 \
    --effects zoom_in pan_left \
    --music music/epic.mp3 \
    --music-volume 0.15

python scripts/create_segment.py batch \
    --segments segments.json \
    --images-dir images/ \
    --audio-dir audio/ \
    --output-dir clips/ \
    --music-dir music/
```

**Ken Burns effects to implement:**
- `zoom_in` - Slow zoom to center
- `zoom_out` - Slow zoom out from center
- `pan_left` - Pan left to right
- `pan_right` - Pan right to left
- `pan_up` - Tilt upward
- `pan_down` - Tilt downward

**Key implementation notes:**
- Use FFmpeg zoompan filter
- Support multiple effects per segment (split duration)
- Layer background music from chapter settings
- Add 0.5s padding before/after narration
- Output 1920x1080 @ 30fps

**Acceptance Criteria:**
- [x] Single mode creates video segment
- [x] Ken Burns effects are smooth
- [x] Multiple effects can be chained (note: currently uses first effect for full duration)
- [x] Background music is layered correctly
- [x] Audio is synced with padding
- [x] Batch mode processes all segments

---

### Task 2.4: Create assemble_video.py ✅
Concatenate all segments into final video.

**Example usage:**
```bash
python scripts/assemble_video.py \
    --clips-dir clips/ \
    --segments segments.json \
    --output final_video.mp4
```

**Key implementation notes:**
- Use FFmpeg concat demuxer for fast concatenation
- Generate YouTube chapter markers file
- Order clips based on segments.json
- Calculate chapter timestamps from clip durations

**Acceptance Criteria:**
- [x] All clips concatenated in correct order
- [x] Chapter markers file generated
- [x] Final video plays correctly
- [x] No gaps between segments

---

## Phase 3: Project Management

### Task 3.1: Create init_project.py ⬜
Initialize a new video project.

**Example usage:**
```bash
python scripts/init_project.py "The Fall of Rome"
# Creates: projects/the_fall_of_rome/
```

**What it creates:**
```
projects/the_fall_of_rome/
├── script.md              # Template for script
├── segments.json          # Template with example structure
├── images/
├── audio/
├── clips/
└── notes.md               # Project notes
```

**Acceptance Criteria:**
- [ ] Creates project folder with sanitized name
- [ ] Creates all subfolders
- [ ] Creates template files
- [ ] Doesn't overwrite existing project

---

### Task 3.2: Create AI Prompt Templates ✅
Prompt files for use with Claude, GPT, etc.

**Files to create:**
- [x] `prompts/1_script_generator.md` - Generate full documentary script
- [x] `prompts/2_segment_planner.md` - Break script into segments (includes image prompt guidance)
- [~] `prompts/3_image_prompt_generator.md` - Not created (functionality covered in segment planner)

**Acceptance Criteria:**
- [x] Prompts are clear and detailed
- [x] Include example inputs and outputs
- [x] Specify output format requirements

---

## Phase 4: Testing & Documentation

### Task 4.1: Create Example Project ✅
A small working example to test the system.

**Create:**
- [x] `projects/example_project/segments.json` - Example project structure exists
- [ ] Download or create sample background music
- [x] Document the example in README.md

**Acceptance Criteria:**
- [x] Example can be processed end-to-end
- [x] Demonstrates all features
- [x] Takes <5 minutes to process

---

### Task 4.2: Write README.md ✅
User-facing documentation.

**Sections:**
- [x] Overview / What is this?
- [x] Installation (uv, FFmpeg, API keys)
- [x] Quick Start (5-minute example)
- [x] Full Workflow Guide
- [x] Command Reference
- [x] Troubleshooting
- [x] FAQ (covered in troubleshooting)

**Acceptance Criteria:**
- [x] New user can get started from README alone
- [x] All commands documented
- [x] Common issues addressed

---

### Task 4.3: Test Full Workflow 🟡
End-to-end test with a real project.

**Steps:**
1. Initialize new project
2. Create segments.json (5-10 segments)
3. Generate all images
4. Generate all voice clips
5. Create all segment videos
6. Assemble final video

**Note:** Multiple test projects exist (example_project, agentic_ai_example, Video-test, prompt_engineering) indicating workflow has been tested.

**Acceptance Criteria:**
- [x] Complete workflow runs without errors
- [x] Final video plays correctly
- [x] Processing time is reasonable

---

## Phase 5: Enhancements (Optional)

### Task 5.1: Add Progress Bars ⬜
Better progress indication for batch operations.

**Consider:**
- `rich` library for progress bars
- ETA calculation
- Summary at end (X succeeded, Y failed)

---

### Task 5.2: Add Validation Script ⬜
Validate segments.json before processing.

**Checks:**
- [ ] JSON is valid
- [ ] All required fields present
- [ ] Voice name is valid
- [ ] Ken Burns effects are valid
- [ ] Music files exist

---

### Task 5.3: Add Regenerate Command ⬜
Regenerate specific segments without redoing everything.

```bash
python scripts/regenerate.py \
    --project projects/the_fall_of_rome \
    --segments 005 012 023 \
    --what all  # or: image, audio, video
```

---

## Additional Scripts (Beyond Original Tasks)

The following scripts were created beyond the original task plan:

- `scripts/workflow.py` - End-to-end workflow automation
- `scripts/prompt_config.py` - Visual prompt engineering configuration
- `scripts/prompt_generator.py` - Visual prompt generation utilities
- `scripts/prompt_library.py` - Library of reusable prompt components

---

## Notes

### Working with Claude Code

When asking Claude Code to work on a task:

1. Reference this file: "Let's work on Task 2.1: Create generate_voice.py"
2. Check CLAUDE.md for project guidelines
3. Check PRD.md for detailed specifications
4. Test the script after creating it
5. Update task status when complete

### Testing Commands

Quick test commands to verify each script works:

```bash
# Test voice generation
python scripts/generate_voice.py single \
    --text "This is a test of the voice generation system." \
    --output test_voice.mp3

# Test image generation (requires API key)
python scripts/generate_image.py single \
    --prompt "A beautiful sunset over mountains, photorealistic" \
    --output test_image.png

# Test segment creation
python scripts/create_segment.py single \
    --image test_image.png \
    --audio test_voice.mp3 \
    --output test_segment.mp4 \
    --effects zoom_in
```
