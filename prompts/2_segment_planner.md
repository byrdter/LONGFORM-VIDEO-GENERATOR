# Prompt 2: Segment Planner

Use this prompt to break your documentary script into segments suitable for video production.

---

## The Prompt

```
You are a video production planner. Your task is to break a documentary script into individual segments for automated video generation.

## Understanding the Video System

Each segment will become a video clip consisting of:
- ONE still image with a Ken Burns effect (slow zoom or pan)
- Narration audio (the text you extract)
- Background music (set per chapter)

The segments will be concatenated to form the final video.

## Segment Guidelines

**Duration:**
- Each segment should be 20-60 seconds of narration
- At ~2.5 words per second, that's roughly 50-150 words per segment
- Shorter segments (20-30s) create more dynamic pacing
- Longer segments (45-60s) work for contemplative moments

**Breaking Points:**
- Break at natural pauses in the narration
- End of a complete thought or idea
- Before a transition to a new scene/topic
- After a rhetorical question (gives it weight)

**One Image Per Segment:**
- Each segment needs ONE primary image
- The image should capture the essence of what's being discussed
- Think: "What single frame best represents these 30 seconds?"

## Ken Burns Effects

Choose effects based on the content:

| Effect | Best For |
|--------|----------|
| zoom_in | Revealing details, emotional moments, emphasis |
| zoom_out | Establishing shots, showing scale, endings |
| pan_left | Landscapes, movement from point A to B |
| pan_right | Landscapes, movement from point B to A |
| pan_up | Tall structures, looking to the sky, aspiration |
| pan_down | Reveals from above, looking down, contemplation |

**For longer segments (40-60s)**, use TWO effects in sequence:
- ["zoom_out", "pan_left"] - Establish then explore
- ["zoom_in", "zoom_out"] - Focus then release
- ["pan_left", "zoom_in"] - Survey then focus

## Output Format

Output valid JSON matching this structure:

```json
{
  "project_name": "Title of Project",
  "voice": "en-GB-RyanNeural",
  "chapters": [
    {
      "chapter_id": 1,
      "title": "Chapter Title",
      "music_track": "suggested_music_style.mp3",
      "music_volume": 0.15,
      "segments": [
        {
          "segment_id": "001",
          "narration": "The exact text to be spoken...",
          "image_description": "Brief description of ideal image",
          "image_prompt": "Detailed prompt for image generation...",
          "ken_burns_sequence": ["effect1", "effect2"],
          "transition": "fade"
        }
      ]
    }
  ]
}
```

## Transition Types

- `"cut"` - Hard cut (for dramatic moments, urgency)
- `"fade"` - Fade to black then in (for chapter endings, time passing)
- `"crossfade"` - Dissolve into next (for smooth flow, related content)

## Music Track Suggestions

Name tracks by mood (user will match to actual files):
- `epic_orchestral.mp3` - Grand, sweeping moments
- `tension_building.mp3` - Building suspense
- `melancholic_piano.mp3` - Sad, reflective sections
- `mysterious_ambient.mp3` - Unknown, discovery
- `triumphant_brass.mp3` - Victory, achievement
- `gentle_strings.mp3` - Peaceful, contemplative

## Voice Options

Common documentary voices:
- `en-GB-RyanNeural` - British male (authoritative, historical)
- `en-GB-SoniaNeural` - British female (elegant, thoughtful)
- `en-US-GuyNeural` - American male (deep, serious)
- `en-US-DavisNeural` - American male (warm, storytelling)
- `en-US-AriaNeural` - American female (engaging, dynamic)

## Image Prompt Guidelines

For each image_prompt, include:
1. Main subject and composition
2. Setting/environment details
3. Lighting description
4. Mood/atmosphere
5. "photorealistic, cinematic, 16:9 aspect ratio" (always include)

Example:
"Roman legionaries marching through a mountain pass at dawn, eagles and standards held high against a dramatic cloudy sky, dust rising from their sandaled feet, golden morning light breaking through clouds, sense of power and determination, photorealistic, cinematic composition, 16:9 aspect ratio"

## The Script to Process

[PASTE YOUR FULL SCRIPT HERE]

## Instructions

1. Read the entire script
2. Identify chapter boundaries
3. Break each chapter into segments of 50-150 words
4. For each segment, write a detailed image prompt
5. Choose appropriate Ken Burns effects
6. Select transitions
7. Output as valid JSON
```

---

## Tips for Best Results

1. **Paste the Complete Script**: The AI needs full context to make good breaking decisions
2. **Specify Your Preferences**: "I prefer shorter segments around 25-30 seconds" or "Make chapters visually distinct"
3. **Review the Image Prompts**: These are crucial - edit them if they don't capture what you envision
4. **Check Segment Count**: A 30-minute video needs roughly 60-90 segments at 20-30 seconds each

---

## Post-Processing Checklist

After getting the JSON output:

1. [ ] Validate JSON syntax (use a JSON validator)
2. [ ] Check segment count matches expected duration
3. [ ] Review image prompts for quality and consistency
4. [ ] Verify Ken Burns effects match content
5. [ ] Confirm music tracks make sense for mood
6. [ ] Save as `segments.json` in your project folder
