# Development Tasks

## Overview

This file tracks development progress. Claude Code should work through these tasks in order. Each task builds on the previous ones.

**Status Legend:**
- ⬜ Not started
- 🟡 In progress
- ✅ Complete

---

## Phase 1: Project Setup

### Task 1.1: Initialize Project Structure ⬜
Create the basic project structure with all necessary folders and files.

**Files to create:**
- [ ] `pyproject.toml` - Python project configuration with dependencies
- [ ] `.env.example` - Template for API keys
- [ ] `.gitignore` - Git ignore file
- [ ] `README.md` - User documentation
- [ ] `scripts/__init__.py` - Make scripts a package
- [ ] `scripts/utils.py` - Shared utility functions
- [ ] `music/.gitkeep` - Placeholder for music folder
- [ ] `projects/.gitkeep` - Placeholder for projects folder

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
- [ ] Can run `uv sync` without errors
- [ ] All folders exist
- [ ] .env.example contains GEMINI_API_KEY placeholder

---

### Task 1.2: Create utils.py ⬜
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

**Acceptance Criteria:**
- [ ] All functions have type hints
- [ ] All functions have docstrings
- [ ] Functions handle errors gracefully

---

## Phase 2: Core Scripts

### Task 2.1: Create generate_voice.py ⬜
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
- [ ] Single mode generates audio file
- [ ] Batch mode processes all segments
- [ ] Existing files are skipped
- [ ] Progress is printed
- [ ] list-voices shows English voices

---

### Task 2.2: Create generate_image.py ⬜
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
- [ ] Single mode generates image
- [ ] Batch mode processes all segments
- [ ] Images are 16:9 aspect ratio
- [ ] Existing files are skipped
- [ ] API errors are handled gracefully

---

### Task 2.3: Create create_segment.py ⬜
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
- [ ] Single mode creates video segment
- [ ] Ken Burns effects are smooth
- [ ] Multiple effects can be chained
- [ ] Background music is layered correctly
- [ ] Audio is synced with padding
- [ ] Batch mode processes all segments

---

### Task 2.4: Create assemble_video.py ⬜
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
- [ ] All clips concatenated in correct order
- [ ] Chapter markers file generated
- [ ] Final video plays correctly
- [ ] No gaps between segments

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

### Task 3.2: Create AI Prompt Templates ⬜
Prompt files for use with Claude, GPT, etc.

**Files to create:**
- [ ] `prompts/1_script_generator.md` - Generate full documentary script
- [ ] `prompts/2_segment_planner.md` - Break script into segments
- [ ] `prompts/3_image_prompt_generator.md` - Create image prompts

**Acceptance Criteria:**
- [ ] Prompts are clear and detailed
- [ ] Include example inputs and outputs
- [ ] Specify output format requirements

---

## Phase 4: Testing & Documentation

### Task 4.1: Create Example Project ⬜
A small working example to test the system.

**Create:**
- [ ] `projects/example_project/segments.json` - 3-5 segments
- [ ] Download or create sample background music
- [ ] Document the example in README.md

**Acceptance Criteria:**
- [ ] Example can be processed end-to-end
- [ ] Demonstrates all features
- [ ] Takes <5 minutes to process

---

### Task 4.2: Write README.md ⬜
User-facing documentation.

**Sections:**
- [ ] Overview / What is this?
- [ ] Installation (uv, FFmpeg, API keys)
- [ ] Quick Start (5-minute example)
- [ ] Full Workflow Guide
- [ ] Command Reference
- [ ] Troubleshooting
- [ ] FAQ

**Acceptance Criteria:**
- [ ] New user can get started from README alone
- [ ] All commands documented
- [ ] Common issues addressed

---

### Task 4.3: Test Full Workflow ⬜
End-to-end test with a real project.

**Steps:**
1. Initialize new project
2. Create segments.json (5-10 segments)
3. Generate all images
4. Generate all voice clips
5. Create all segment videos
6. Assemble final video

**Acceptance Criteria:**
- [ ] Complete workflow runs without errors
- [ ] Final video plays correctly
- [ ] Processing time is reasonable

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
