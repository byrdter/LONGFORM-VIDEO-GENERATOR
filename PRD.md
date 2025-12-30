# Product Requirements Document (PRD)
# Long-Form Video Generator

## 1. Executive Summary

### 1.1 Product Vision
A command-line tool system for creating professional-quality, long-form (30+ minute) documentary-style videos using AI-generated content. The system combines AI-written scripts, AI-generated images, AI voice synthesis, and automated video assembly to produce videos at near-zero marginal cost.

### 1.2 Target User
Content creators who want to produce educational, historical, or speculative documentary videos without:
- Professional video editing skills
- Expensive software subscriptions
- Stock footage libraries
- Voice actors

### 1.3 Key Value Proposition
- **Cost**: ~$0 per video using free API tiers
- **Speed**: Generate a 30-minute video in hours, not days
- **Quality**: Professional narration, consistent visual style, proper pacing
- **Automation**: Batch processing of all assets

---

## 2. Product Requirements

### 2.1 Functional Requirements

#### FR-1: Script Generation Support
- **FR-1.1**: Provide prompt templates for AI script generation
- **FR-1.2**: Support chapter-based organization
- **FR-1.3**: Output format compatible with segment planning

#### FR-2: Segment Planning
- **FR-2.1**: Break scripts into 20-60 second segments
- **FR-2.2**: Each segment defines: narration text, image prompt, Ken Burns effects
- **FR-2.3**: Support chapter-level configuration (music track, volume)
- **FR-2.4**: Output as structured JSON for automation

#### FR-3: Image Generation
- **FR-3.1**: Generate images via Gemini API (Imagen 3)
- **FR-3.2**: Support single image and batch generation modes
- **FR-3.3**: Enforce 16:9 aspect ratio for video compatibility
- **FR-3.4**: Skip existing images in batch mode (idempotent)

#### FR-4: Voice Generation
- **FR-4.1**: Generate narration via Edge TTS (free)
- **FR-4.2**: Support multiple voice options (British, American, male, female)
- **FR-4.3**: Support speech rate adjustment
- **FR-4.4**: Batch generation from segments.json

#### FR-5: Segment Video Creation
- **FR-5.1**: Apply Ken Burns effects (zoom, pan) to still images
- **FR-5.2**: Support multiple effects per segment (e.g., zoom_in then pan_left)
- **FR-5.3**: Sync narration audio with configurable padding
- **FR-5.4**: Layer background music at configurable volume
- **FR-5.5**: Output 1920x1080 @ 30fps H.264 video

#### FR-6: Final Assembly
- **FR-6.1**: Concatenate all segment clips in order
- **FR-6.2**: Generate YouTube chapter markers file
- **FR-6.3**: Support optional crossfade transitions
- **FR-6.4**: Output final video in YouTube-ready format

### 2.2 Non-Functional Requirements

#### NFR-1: Performance
- Image generation: <30 seconds per image
- Voice generation: <5 seconds per segment
- Segment video creation: <30 seconds per segment
- Full 30-minute video: <2 hours total processing

#### NFR-2: Reliability
- All batch operations must be idempotent (skip existing files)
- Graceful error handling with informative messages
- Resume capability after interruption

#### NFR-3: Usability
- CLI interface with clear help text
- Progress output during batch operations
- Sensible defaults for all optional parameters

#### NFR-4: Maintainability
- Modular script architecture (one script = one function)
- Type hints throughout Python code
- Comprehensive CLAUDE.md for AI-assisted development

---

## 3. Technical Specifications

### 3.1 System Requirements

| Requirement | Specification |
|-------------|---------------|
| Python | 3.10 or higher |
| FFmpeg | Latest stable |
| OS | macOS, Linux, Windows |
| RAM | 4GB minimum |
| Storage | ~500MB per 30-min project |

### 3.2 Dependencies

```toml
[project]
dependencies = [
    "google-generativeai>=0.3.0",
    "edge-tts>=6.1.0",
    "python-dotenv>=1.0.0",
]
```

### 3.3 API Requirements

| API | Purpose | Auth | Cost |
|-----|---------|------|------|
| Gemini API | Image generation | API key | Free tier |
| Edge TTS | Voice synthesis | None | Free |

### 3.4 File Format Specifications

#### Input: segments.json
```json
{
  "project_name": "The Fall of Rome",
  "voice": "en-GB-RyanNeural",
  "chapters": [
    {
      "chapter_id": 1,
      "title": "The Golden Age",
      "music_track": "epic_orchestral.mp3",
      "music_volume": 0.15,
      "segments": [
        {
          "segment_id": "001",
          "narration": "At its height, the Roman Empire...",
          "image_prompt": "Panoramic view of ancient Rome...",
          "ken_burns_sequence": ["zoom_out", "pan_right"],
          "transition": "fade"
        }
      ]
    }
  ]
}
```

#### Output: Video
- Container: MP4
- Video codec: H.264 (libx264)
- Video resolution: 1920x1080
- Video framerate: 30 fps
- Audio codec: AAC
- Audio bitrate: 192 kbps
- Audio channels: Stereo

#### Output: Chapter Markers
```text
YouTube Chapters:
----------------------------------------
0:00 The Golden Age
5:32 The Crisis of the Third Century
12:45 The Fall of the West
```

---

## 4. User Stories

### US-1: Create a New Project
**As a** content creator
**I want to** initialize a new video project
**So that** I have an organized folder structure to work with

**Acceptance Criteria:**
- Running `python scripts/init_project.py "The Fall of Rome"` creates the project folder structure
- Creates empty segments.json template
- Creates placeholder folders for images, audio, clips

### US-2: Generate Script with AI
**As a** content creator  
**I want to** use AI to generate my documentary script
**So that** I don't have to write 30 minutes of content from scratch

**Acceptance Criteria:**
- Clear prompt template in `prompts/1_script_generator.md`
- Instructions for using with Claude, GPT, or other AI
- Output format ready for segment planning

### US-3: Plan Segments
**As a** content creator
**I want to** break my script into video segments
**So that** I can generate assets for each segment

**Acceptance Criteria:**
- AI prompt template for segment planning
- Outputs valid segments.json
- Each segment has all required fields

### US-4: Generate All Images
**As a** content creator
**I want to** batch generate all images for my project
**So that** I don't have to generate them one by one

**Acceptance Criteria:**
- `python scripts/generate_image.py batch --segments segments.json --output-dir images/`
- Skips images that already exist
- Shows progress (e.g., "Generating image 5/60...")

### US-5: Generate All Voice Narration
**As a** content creator
**I want to** batch generate all voice clips
**So that** I have narration for every segment

**Acceptance Criteria:**
- `python scripts/generate_voice.py batch --segments segments.json --output-dir audio/`
- Uses voice specified in segments.json
- Skips existing audio files

### US-6: Create All Segment Videos
**As a** content creator
**I want to** combine images and audio into video segments
**So that** I have individual clips ready for assembly

**Acceptance Criteria:**
- Ken Burns effects applied correctly
- Background music layered at correct volume
- Audio/video properly synced

### US-7: Assemble Final Video
**As a** content creator
**I want to** combine all segments into one video
**So that** I have a complete documentary to upload

**Acceptance Criteria:**
- All clips concatenated in order
- YouTube chapter markers file generated
- Final video plays correctly

### US-8: Iterate on Specific Segments
**As a** content creator
**I want to** regenerate specific segments without redoing everything
**So that** I can fix issues efficiently

**Acceptance Criteria:**
- Can regenerate single image: `--segment 015`
- Can regenerate single audio: `--segment 015`
- Can regenerate single video clip: `--segment 015`

---

## 5. User Interface

### 5.1 Command Line Interface

All interaction is via CLI scripts. Each script follows this pattern:

```bash
python scripts/<script_name>.py <command> [options]
```

### 5.2 Commands Overview

| Script | Commands | Purpose |
|--------|----------|---------|
| `init_project.py` | (default) | Create new project folder |
| `generate_image.py` | single, batch | Generate images |
| `generate_voice.py` | single, batch, list-voices | Generate narration |
| `create_segment.py` | single, batch | Create video segments |
| `assemble_video.py` | (default) | Assemble final video |

### 5.3 Example Complete Workflow

```bash
# 1. Initialize project
python scripts/init_project.py "The Fall of Rome"

# 2. Generate script (manual - use AI assistant)
# Edit: projects/the_fall_of_rome/script.md

# 3. Plan segments (manual - use AI assistant)
# Edit: projects/the_fall_of_rome/segments.json

# 4. Generate all images
python scripts/generate_image.py batch \
    --segments projects/the_fall_of_rome/segments.json \
    --output-dir projects/the_fall_of_rome/images

# 5. Generate all voice narration
python scripts/generate_voice.py batch \
    --segments projects/the_fall_of_rome/segments.json \
    --output-dir projects/the_fall_of_rome/audio

# 6. Create all segment videos
python scripts/create_segment.py batch \
    --segments projects/the_fall_of_rome/segments.json \
    --images-dir projects/the_fall_of_rome/images \
    --audio-dir projects/the_fall_of_rome/audio \
    --output-dir projects/the_fall_of_rome/clips \
    --music-dir music/

# 7. Assemble final video
python scripts/assemble_video.py \
    --clips-dir projects/the_fall_of_rome/clips \
    --segments projects/the_fall_of_rome/segments.json \
    --output projects/the_fall_of_rome/final_video.mp4
```

---

## 6. Ken Burns Effects Specification

### 6.1 Available Effects

| Effect | Description | Best For |
|--------|-------------|----------|
| `zoom_in` | 1.0x → 1.3x zoom to center | Reveals, emotional moments, emphasis |
| `zoom_out` | 1.3x → 1.0x zoom from center | Establishing shots, endings, scope |
| `pan_left` | Pan from left to right | Landscapes, following action |
| `pan_right` | Pan from right to left | Landscapes, following action |
| `pan_up` | Tilt from bottom to top | Tall structures, looking skyward |
| `pan_down` | Tilt from top to bottom | Reveals from above, looking down |

### 6.2 Effect Sequencing

Multiple effects can be chained for longer segments:

```json
"ken_burns_sequence": ["zoom_in", "pan_left"]
```

- Total segment duration is divided equally among effects
- Example: 40-second segment with 2 effects = 20 seconds each

### 6.3 Effect Selection Guidelines

| Narration Content | Recommended Effects |
|-------------------|---------------------|
| Introduction/overview | `zoom_out` |
| Specific detail/person | `zoom_in` |
| Geographic description | `pan_left` or `pan_right` |
| Architectural feature | `pan_up` or `zoom_in` |
| Dramatic moment | `zoom_in` (slow) |
| Chapter transition | `zoom_out` + `fade` |

### 6.4 Static Images (No Ken Burns)

For content like maps, documents, or diagrams where camera movement is distracting, static images can be used:

**Per-segment:** Use an empty array or omit the field:
```json
"ken_burns_sequence": []
```

**Per-chapter:** Disable for all segments in a chapter:
```json
{
  "chapter_id": 3,
  "title": "Maps and Documents",
  "ken_burns_enabled": false,
  "segments": [...]
}
```

Static images are scaled to fit 1920x1080 and displayed for the duration of the narration.

---

## 7. Audio Specifications

### 7.1 Voice Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| Sample rate | 24kHz | Edge TTS default |
| Format | MP3 | Compatible with FFmpeg |
| Rate | Configurable | Default: normal speed |

### 7.2 Recommended Voices

| Voice ID | Description | Best For |
|----------|-------------|----------|
| `en-GB-RyanNeural` | British male | Historical, formal |
| `en-GB-SoniaNeural` | British female | Historical, formal |
| `en-US-GuyNeural` | American male, deep | General, authoritative |
| `en-US-DavisNeural` | American male, warm | Storytelling |
| `en-US-AriaNeural` | American female | Expressive, engaging |
| `en-US-JennyNeural` | American female, clear | Educational |

### 7.3 Background Music

| Setting | Recommended Value |
|---------|-------------------|
| Volume | 0.10 - 0.20 (10-20% of narration) |
| Format | MP3 (any bitrate) |
| Loop | Auto-loop if shorter than chapter |

---

## 8. Success Metrics

### 8.1 Technical Metrics
- [ ] Generate 60+ images in batch without failure
- [ ] Generate 60+ voice clips in batch without failure
- [ ] Create 60+ video segments in batch without failure
- [ ] Assemble 30+ minute video without errors
- [ ] YouTube chapters file generated correctly

### 8.2 Quality Metrics
- [ ] All images render at 1920x1080
- [ ] Voice narration is clear and properly paced
- [ ] Ken Burns effects are smooth (no jitter)
- [ ] Audio levels are balanced (narration audible over music)
- [ ] No gaps or sync issues between segments

---

## 9. Future Enhancements (Out of Scope for V1)

- Web UI for project management
- Real-time preview of segments
- AI video generation integration (Kling, Sora) as upgrade path
- Automatic subtitle generation
- Multiple language support
- Custom voice training
- Template library for common video types

---

## 10. Appendix

### A. Glossary

| Term | Definition |
|------|------------|
| Segment | A single unit of video (20-60 seconds) with one image |
| Chapter | A group of related segments with shared music |
| Ken Burns effect | Camera movement (zoom/pan) applied to still image |
| Edge TTS | Microsoft's free text-to-speech service |
| Gemini API | Google's AI API including Imagen 3 for images |

### B. Reference Implementation

- Pokemon AI Video Generator: https://github.com/bhancockio/pokemon-ai-video-generator
- Edge TTS documentation: https://github.com/rany2/edge-tts
- Gemini API: https://ai.google.dev/

### C. Sample segments.json

See `projects/example_project/segments.json` for a complete working example.
