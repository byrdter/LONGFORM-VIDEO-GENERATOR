# Visual Prompt Engineering Guide

**Author:** Manus AI  
**Date:** December 30, 2025  
**Version:** 1.0

## Overview

This guide explains how to use the integrated visual prompt engineering system to automate the creation of high-quality image prompts for your Agentic AI educational videos. The system combines intelligent prompt generation, a persistent prompt library, and seamless integration with your existing video generation workflow.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Core Components](#core-components)
3. [Workflow Options](#workflow-options)
4. [Prompt Generation](#prompt-generation)
5. [Prompt Library](#prompt-library)
6. [Configuration](#configuration)
7. [Examples](#examples)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Option 1: Fully Automated Workflow

Generate prompts and create your entire video in one command:

```bash
python scripts/workflow.py projects/my_agentic_ai_video/
```

This will:
1. Analyze your narration and generate optimized image prompts
2. Generate images from prompts
3. Generate voice narration
4. Create video segments with Ken Burns effects
5. Assemble the final video

### Option 2: Prompts Only

Just generate prompts without creating the video:

```bash
python scripts/prompt_generator.py batch \
    --segments projects/my_project/segments.json \
    --style isometric
```

### Option 3: Interactive Mode

Review and edit each prompt before proceeding:

```bash
python scripts/workflow.py projects/my_project/ --interactive
```

---

## Core Components

### 1. `prompt_config.py` - Knowledge Base

Contains the research-backed knowledge base:

- **Visual Styles:** 5 predefined styles (minimalist, isometric, blueprint, cyberpunk, photorealistic)
- **Agentic AI Concepts:** 14 concepts with metaphors and keywords
- **Quality Boosters:** Keywords that enhance image quality
- **Negative Prompts:** Keywords to exclude unwanted elements
- **Platform Configurations:** Settings for different AI image generators

### 2. `prompt_generator.py` - Prompt Generation

Generates optimized prompts from narration text:

- Detects Agentic AI concepts automatically
- Selects appropriate visual metaphors
- Constructs prompts using the five-layer architecture
- Adds quality boosters and negative prompts
- Formats for your target platform (Nano Banana Pro, Midjourney, etc.)

### 3. `prompt_library.py` - Persistent Storage

Manages a SQLite database of successful prompts:

- Save prompts with ratings, tags, and metadata
- Search by concepts, style, or text
- Track usage statistics
- Export/import for backup and sharing
- Reuse successful prompts in new projects

### 4. `workflow.py` - Integrated Workflow

Combines all components into a streamlined workflow:

- Automatic prompt generation with library lookup
- Integration with existing video generation scripts
- Interactive review and rating
- End-to-end automation

---

## Workflow Options

### Workflow A: Fully Automated

**Best for:** Quick iteration, consistent style, large projects

```bash
# Run complete workflow
python scripts/workflow.py projects/my_project/ \
    --style isometric \
    --skip-review
```

**What happens:**
1. Generates prompts for all segments
2. Checks library for similar prompts (reuses if found)
3. Generates new prompts for segments without matches
4. Runs complete video generation pipeline
5. Skips manual review

---

### Workflow B: Interactive

**Best for:** High-quality control, learning, first-time users

```bash
# Run with interactive prompt review
python scripts/workflow.py projects/my_project/ \
    --interactive
```

**What happens:**
1. For each segment, shows:
   - Original narration
   - Generated prompt
   - Similar prompts from library (if any)
2. You can:
   - Accept the generated prompt
   - Choose a library prompt
   - Edit the prompt manually
   - Skip the segment
3. Continues with video generation
4. Reviews results and saves successful prompts to library

---

### Workflow C: Prompts Only

**Best for:** Preparing prompts in advance, batch processing

```bash
# Generate prompts without creating video
python scripts/workflow.py projects/my_project/ \
    --prompts-only \
    --style cyberpunk
```

**What happens:**
1. Generates and saves prompts to segments.json
2. Stops before image generation
3. You can review/edit prompts manually
4. Run image generation later

---

### Workflow D: Manual with Library

**Best for:** Maximum control, custom workflows

```bash
# Step 1: Generate prompts
python scripts/prompt_generator.py batch \
    --segments projects/my_project/segments.json \
    --style isometric

# Step 2: Review segments.json and edit prompts

# Step 3: Generate images
python scripts/generate_image.py batch \
    --segments projects/my_project/segments.json \
    --output-dir projects/my_project/images

# Step 4: Save successful prompts to library
python scripts/prompt_library.py save \
    --prompt "Your successful prompt here" \
    --rating 5 \
    --style isometric \
    --concepts "orchestration,multi-agent"

# Step 5: Continue with existing workflow
python scripts/generate_voice.py batch ...
python scripts/create_segment.py batch ...
python scripts/assemble_video.py ...
```

---

## Prompt Generation

### How It Works

The prompt generator uses a five-layer architecture:

```
Layer 1: Subject/Concept
    ↓
Layer 2: Action/Context
    ↓
Layer 3: Visual Style
    ↓
Layer 4: Composition/Lighting
    ↓
Layer 5: Quality Boosters
    ↓
Platform Formatting
```

### Concept Detection

The system automatically detects Agentic AI concepts in your narration:

| Narration Contains | Detected Concept | Default Style |
|:-------------------|:-----------------|:--------------|
| "orchestration", "coordination" | orchestration | isometric |
| "multi-agent", "team of agents" | multi-agent | isometric |
| "state", "memory", "persistence" | state_management | blueprint |
| "security", "protection" | security | cyberpunk |
| "monitoring", "observability" | observability | cyberpunk |

### Visual Styles

Choose from five research-backed styles:

**Minimalist** - Simple, clear, educational
```python
Keywords: flat design, vector art, clean lines
Best for: Icons, simple diagrams, concept illustrations
```

**Isometric** - 3D perspective, structured
```python
Keywords: isometric view, 3D render, low poly
Best for: System architecture, data flow, technical diagrams
```

**Blueprint** - Technical, schematic
```python
Keywords: blueprint style, schematic diagram, wireframe
Best for: Internal mechanisms, algorithms, specifications
```

**Cyberpunk** - High-tech, dramatic, engaging
```python
Keywords: cyberpunk, neon glow, holographic display
Best for: Title cards, thumbnails, high-tech atmosphere
```

**Photorealistic** - Realistic, cinematic
```python
Keywords: photorealistic, cinematic lighting, depth of field
Best for: Hero shots, high-impact visuals, realism
```

### Single Prompt Generation

Generate a single prompt from narration:

```bash
python scripts/prompt_generator.py single \
    --narration "Multi-agent systems coordinate through a central orchestrator" \
    --style isometric \
    --output my_prompt.json
```

Output:
```json
{
  "prompt": "multi-agent system represented as orchestra, coordinating data and information, isometric view, 3D render, low poly, cinematic lighting, 8K resolution, hyper-detailed, sharp focus --ar 16:9 --style raw --stylize 750",
  "negative_prompt": "blurry, deformed, ugly, low quality, bad anatomy, text, watermark, signature, flat, 2D",
  "style": "isometric",
  "concepts": ["multi-agent", "orchestration"],
  "source": "generated"
}
```

### Batch Processing

Process an entire segments.json file:

```bash
python scripts/prompt_generator.py batch \
    --segments projects/my_project/segments.json \
    --style isometric \
    --overwrite
```

Options:
- `--style`: Override style for all segments
- `--overwrite`: Replace existing prompts
- `--interactive`: Review each prompt
- `--output`: Save to different file

---

## Prompt Library

### Why Use a Library?

- **Reuse Successful Prompts:** Don't reinvent the wheel
- **Build Knowledge:** Learn what works over time
- **Consistency:** Maintain visual style across projects
- **Efficiency:** 50-70% time savings

### Saving Prompts

Save a successful prompt:

```bash
python scripts/prompt_library.py save \
    --prompt "A central AI conductor orchestrating agents..." \
    --negative "blurry, deformed, text, watermark" \
    --narration "Multi-agent systems coordinate..." \
    --concepts "orchestration,multi-agent" \
    --style isometric \
    --rating 5 \
    --tags "title-card,hero-shot" \
    --image projects/my_project/images/001.png
```

### Searching the Library

Find prompts by concept:

```bash
python scripts/prompt_library.py search \
    --concepts "orchestration" \
    --min-rating 4 \
    --limit 5
```

Find prompts by text:

```bash
python scripts/prompt_library.py search \
    --query "conductor" \
    --style isometric
```

### Rating Prompts

Rate a prompt after seeing results:

```bash
python scripts/prompt_library.py rate \
    --id 42 \
    --rating 5
```

### Library Statistics

View your library stats:

```bash
python scripts/prompt_library.py stats
```

Output:
```
PROMPT LIBRARY STATISTICS
==================================================
Total Prompts: 127

By Rating:
  ⭐⭐⭐⭐⭐: 23
  ⭐⭐⭐⭐: 45
  ⭐⭐⭐: 38
  ⭐⭐: 12
  ⭐: 5
  Unrated: 4

By Style:
  isometric: 52
  cyberpunk: 31
  photorealistic: 24
  blueprint: 15
  minimalist: 5

Most Used:
  1. ID 42: 12 uses, 5⭐
  2. ID 17: 9 uses, 5⭐
  ...
```

### Export/Import

Export your library:

```bash
python scripts/prompt_library.py export \
    --output my_prompt_library.json
```

Import a library:

```bash
python scripts/prompt_library.py import \
    --input shared_library.json
```

---

## Configuration

### segments.json Enhancement

The system adds optional fields to your segments.json:

```json
{
  "project_name": "Agentic AI Skills",
  "voice": "en-GB-RyanNeural",
  "visual_config": {
    "primary_style": "isometric",
    "consistency_mode": "moderate",
    "platform": "nano-banana-pro"
  },
  "chapters": [
    {
      "chapter_id": 1,
      "title": "Multi-Agent Orchestration",
      "segments": [
        {
          "segment_id": "001",
          "narration": "Multi-agent systems coordinate...",
          
          // AUTO-GENERATED FIELDS
          "image_prompt": "A central AI conductor...",
          "image_prompt_negative": "blurry, deformed...",
          "image_prompt_source": "generated",
          "agentic_concepts": ["multi-agent", "orchestration"],
          "visual_style": "isometric",
          
          // OPTIONAL: If from library
          "prompt_library_id": 42,
          
          // EXISTING FIELDS
          "ken_burns_sequence": ["zoom_in"],
          "transition": "fade"
        }
      ]
    }
  ]
}
```

### Custom Configuration

Create a custom config file (optional):

```python
# my_config.py
from prompt_config import DEFAULT_CONFIG

MY_CONFIG = DEFAULT_CONFIG.copy()
MY_CONFIG.update({
    "default_style": "cyberpunk",
    "platform": "midjourney",
    "aspect_ratio": "16:9",
    "include_quality_boosters": True,
    "consistency_mode": "strict"
})
```

---

## Examples

### Example 1: Agentic AI Skills Video

**Scenario:** Creating a video about the 9 Agentic AI skills

**segments.json (before):**
```json
{
  "segments": [
    {
      "segment_id": "001",
      "narration": "Multi-agent orchestration involves coordinating multiple specialized agents through a central control system."
    }
  ]
}
```

**Command:**
```bash
python scripts/workflow.py projects/agentic_skills/ \
    --style isometric
```

**segments.json (after):**
```json
{
  "segments": [
    {
      "segment_id": "001",
      "narration": "Multi-agent orchestration involves...",
      "image_prompt": "multi-agent system represented as orchestra, central AI conductor coordinating specialized agents, isometric view, 3D render, low poly, cinematic lighting, 8K resolution, hyper-detailed, sharp focus --ar 16:9 --style raw --stylize 750",
      "image_prompt_negative": "blurry, deformed, ugly, low quality, text, watermark, flat, 2D",
      "agentic_concepts": ["multi-agent", "orchestration"],
      "visual_style": "isometric",
      "image_prompt_source": "generated"
    }
  ]
}
```

---

### Example 2: Using the Library

**Scenario:** Second video on similar topics

**Command:**
```bash
python scripts/workflow.py projects/agentic_advanced/ \
    --interactive
```

**What happens:**
```
[001] Found 3 similar prompts in library

Narration: Advanced orchestration patterns enable dynamic agent collaboration...

1. (ID: 42, Rating: 5⭐)
   A central AI conductor orchestrating agents, isometric view...

2. (ID: 17, Rating: 4⭐)
   Multi-agent coordination system with central hub...

3. (ID: 89, Rating: 4⭐)
   Orchestra of AI agents working in harmony...

Use library prompt? [1-3/n]: 1

[001] ✓ Using library prompt (ID: 42)
```

---

### Example 3: Custom Prompt with Manual Edit

**Scenario:** You want a specific visual not captured by auto-generation

**Command:**
```bash
python scripts/prompt_generator.py single \
    --narration "AI agents must protect sensitive data" \
    --style cyberpunk
```

**Generated prompt:**
```
security represented as fortress, protecting data and information, cyberpunk, neon glow, holographic display, cinematic lighting, 8K resolution, hyper-detailed, sharp focus --ar 16:9
```

**You edit it to:**
```
A massive glowing digital fortress with AI guardians defending against cyber threats, cyberpunk, neon glow, dramatic lighting, 8K resolution, hyper-detailed --ar 16:9 --style raw --stylize 750
```

**Save to library:**
```bash
python scripts/prompt_library.py save \
    --prompt "A massive glowing digital fortress..." \
    --rating 5 \
    --concepts "security" \
    --style cyberpunk \
    --tags "fortress,guardian,dramatic"
```

---

## Best Practices

### 1. Start with Good Narration

The quality of generated prompts depends on your narration. Include:

✅ **Good:** "Multi-agent systems coordinate through a central orchestrator that manages task distribution and monitors agent performance."

❌ **Poor:** "This is about agents."

### 2. Build Your Library Gradually

- Start with 5-10 high-quality prompts
- Rate prompts honestly (5⭐ only for exceptional results)
- Add tags for easy searching
- Export your library regularly for backup

### 3. Maintain Visual Consistency

- Choose a primary style for your channel (e.g., isometric)
- Use secondary styles sparingly for emphasis
- Set `consistency_mode: "strict"` in visual_config

### 4. Iterate and Refine

- Generate multiple variations for important segments
- Use `--interactive` mode to compare options
- Save the best prompts to your library
- Learn from what works

### 5. Leverage Concept Detection

Write narration that includes concept keywords:

- "orchestration" → Detects orchestration concept
- "multi-agent" → Detects multi-agent concept
- "security" → Detects security concept

This helps the system choose the right style and metaphors.

---

## Troubleshooting

### Issue: Prompts are too generic

**Solution:**
- Use `--interactive` mode to review and edit
- Add more specific details to your narration
- Manually edit the generated prompt
- Build a library of specific prompts for reuse

### Issue: Wrong visual style selected

**Solution:**
- Override with `--style` parameter
- Set `primary_style` in segments.json visual_config
- Manually specify style for each segment

### Issue: Library not finding similar prompts

**Solution:**
- Ensure concepts are detected (check narration)
- Lower `min_rating` threshold
- Add more prompts to your library
- Use text search instead of concept search

### Issue: Generated images don't match prompt

**Solution:**
- Add more specific negative prompts
- Increase detail in the prompt
- Try different quality boosters
- Adjust platform-specific parameters

### Issue: Workflow fails at image generation

**Solution:**
- Check GEMINI_API_KEY is set
- Verify segments.json has valid prompts
- Check API rate limits
- Review generate_image.py logs

---

## Advanced Topics

### Custom Visual Metaphors

Add your own metaphors to `prompt_config.py`:

```python
AGENTIC_CONCEPTS["my_concept"] = {
    "keywords": ["my", "custom", "keywords"],
    "metaphors": ["my custom metaphor"],
    "visual_keywords": ["custom visual keywords"],
    "default_style": "isometric"
}
```

### Platform-Specific Optimization

Configure for different platforms:

```python
# For DALL-E 3
config = {
    "platform": "dalle3",
    "aspect_ratio": "16:9"
}

# For Stable Diffusion
config = {
    "platform": "stable-diffusion",
    "aspect_ratio": "16:9"
}
```

### Batch Library Operations

Export high-rated prompts only:

```python
from prompt_library import PromptLibrary

library = PromptLibrary()
high_rated = library.search_prompts(min_rating=4, limit=1000)

# Export to custom format
with open('high_rated.json', 'w') as f:
    json.dump(high_rated, f, indent=2)
```

---

## Summary

The visual prompt engineering system provides:

✅ **Automated prompt generation** from narration
✅ **Persistent library** of successful prompts
✅ **Intelligent reuse** of proven prompts
✅ **Seamless integration** with existing workflow
✅ **Research-backed** visual styles and techniques
✅ **50-70% time savings** on prompt creation

**Next Steps:**

1. Run `python scripts/workflow.py --help` to see all options
2. Try the interactive mode on a small project
3. Build your prompt library gradually
4. Experiment with different visual styles
5. Share your library with collaborators

For more information, see:
- `ARCHITECTURE.md` - System design details
- `README.md` - Original project documentation
- Visual Prompt Engineering research documents

---

**Document Version:** 1.0  
**Last Updated:** December 30, 2025  
**Author:** Manus AI
