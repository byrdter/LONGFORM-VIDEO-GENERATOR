# Quick Start Tutorial: Visual Prompt Engineering

**Time Required:** 15 minutes  
**Difficulty:** Beginner

## What You'll Learn

In this tutorial, you'll:
1. Generate optimized image prompts from narration
2. Save successful prompts to your library
3. Reuse library prompts in a new project
4. Run the complete automated workflow

## Prerequisites

- Python 3.10+ installed
- GEMINI_API_KEY configured in `.env`
- Basic familiarity with command line

## Step 1: Generate Your First Prompt (2 minutes)

Let's generate a single prompt from narration about multi-agent orchestration:

```bash
python scripts/prompt_generator.py single \
    --narration "Multi-agent systems coordinate through a central orchestrator that manages task distribution and monitors agent performance" \
    --style isometric
```

**Output:**
```
==================================================
GENERATED PROMPT:
==================================================
multi-agent system represented as orchestra, coordinating data and information, isometric view, 3D render, low poly, cinematic lighting, 8K resolution, hyper-detailed, sharp focus --ar 16:9 --style raw --stylize 750

==================================================
NEGATIVE PROMPT:
==================================================
blurry, deformed, ugly, low quality, bad anatomy, text, watermark, signature, flat, 2D

==================================================
Style: isometric
Detected Concepts: multi-agent, orchestration
Source: generated
==================================================
```

**What happened?**
- The system detected "multi-agent" and "orchestration" concepts
- Selected "isometric" style (as specified)
- Chose the "orchestra" metaphor for orchestration
- Constructed a five-layer prompt with quality boosters
- Added appropriate negative prompts

## Step 2: Process a Complete Project (5 minutes)

Now let's process the example Agentic AI project:

```bash
python scripts/prompt_generator.py batch \
    --segments projects/agentic_ai_example/segments.json \
    --style isometric
```

**Output:**
```
[001] Generating prompt...
[001] ✓ Prompt generated
[002] Generating prompt...
[002] ✓ Prompt generated
...
[012] Generating prompt...
[012] ✓ Prompt generated

==================================================
Summary:
  Total segments: 12
  Generated: 12
  Skipped: 0
  Output: projects/agentic_ai_example/segments.json
==================================================
```

**What happened?**
- Processed all 12 segments
- Generated optimized prompts for each
- Saved enhanced segments.json with prompts

**Inspect the results:**
```bash
# View the enhanced segments.json
cat projects/agentic_ai_example/segments.json | grep "image_prompt" | head -3
```

## Step 3: Save a Prompt to Your Library (2 minutes)

Let's save one of the generated prompts to your library:

```bash
python scripts/prompt_library.py save \
    --prompt "multi-agent system represented as orchestra, central AI conductor coordinating specialized agents, isometric view, 3D render, low poly, cinematic lighting, 8K resolution, hyper-detailed, sharp focus --ar 16:9 --style raw --stylize 750" \
    --negative "blurry, deformed, ugly, low quality, text, watermark, flat, 2D" \
    --narration "Multi-agent orchestration is the foundation of any reliable agentic system" \
    --concepts "multi-agent,orchestration" \
    --style isometric \
    --rating 5 \
    --tags "orchestration,title-card,hero-shot"
```

**Output:**
```
✓ Saved prompt with ID: 1
```

**What happened?**
- Created a new SQLite database at `~/.prompt_library.db`
- Saved the prompt with metadata
- Rated it 5 stars
- Added tags for easy searching

## Step 4: Search Your Library (1 minute)

Search for prompts about orchestration:

```bash
python scripts/prompt_library.py search \
    --concepts "orchestration" \
    --min-rating 4
```

**Output:**
```
Found 1 prompts:

ID: 1
Prompt: multi-agent system represented as orchestra, central AI conductor coordinating specialized...
Style: isometric
Rating: ⭐⭐⭐⭐⭐
Used: 0 times
------------------------------------------------------------
```

## Step 5: Run the Automated Workflow (5 minutes)

Now let's run the complete workflow on a new project. First, create a simple project:

```bash
# Create project directory
mkdir -p projects/test_workflow
mkdir -p projects/test_workflow/images
mkdir -p projects/test_workflow/audio
mkdir -p projects/test_workflow/clips

# Create a simple segments.json
cat > projects/test_workflow/segments.json << 'EOF'
{
  "project_name": "Test Workflow",
  "voice": "en-GB-RyanNeural",
  "chapters": [
    {
      "chapter_id": 1,
      "title": "Introduction",
      "music_track": "background.mp3",
      "music_volume": 0.15,
      "segments": [
        {
          "segment_id": "001",
          "narration": "Multi-agent orchestration enables autonomous systems to coordinate complex tasks through centralized management.",
          "ken_burns_sequence": ["zoom_in"],
          "transition": "fade"
        }
      ]
    }
  ]
}
EOF
```

Run the workflow (prompts only, to avoid image generation):

```bash
python scripts/workflow.py projects/test_workflow/ \
    --prompts-only \
    --style isometric
```

**Output:**
```
==================================================
INTEGRATED VIDEO GENERATION WORKFLOW
==================================================
Project: test_workflow
Segments: projects/test_workflow/segments.json
==================================================

==================================================
STEP 1: PROMPT GENERATION
==================================================

[001] Found 1 similar prompts in library
[001] ✓ Using library prompt (ID: 1)

==================================================
Prompt Generation Summary:
  Total segments: 1
  Generated: 0
  From library: 1
  Manual/existing: 0
  Skipped: 0
==================================================
```

**What happened?**
- The system found your library prompt about orchestration
- Reused it automatically (because the narration is similar)
- Saved time by not generating a new prompt

## Step 6: View Library Statistics (1 minute)

Check your library stats:

```bash
python scripts/prompt_library.py stats
```

**Output:**
```
==================================================
PROMPT LIBRARY STATISTICS
==================================================

Total Prompts: 1

By Rating:
  ⭐⭐⭐⭐⭐: 1

By Style:
  isometric: 1

Most Used:
  1. ID 1: 1 uses, 5⭐

Highest Rated:
  1. ID 1: 5⭐, 1 uses
==================================================
```

## Next Steps

### Continue Learning

1. **Try Interactive Mode:**
   ```bash
   python scripts/workflow.py projects/agentic_ai_example/ \
       --prompts-only \
       --interactive
   ```

2. **Experiment with Styles:**
   ```bash
   # Try cyberpunk style
   python scripts/prompt_generator.py single \
       --narration "AI security systems protect against threats" \
       --style cyberpunk
   
   # Try photorealistic
   python scripts/prompt_generator.py single \
       --narration "Memory systems store knowledge" \
       --style photorealistic
   ```

3. **Build Your Library:**
   - Generate prompts for your own content
   - Rate them after seeing results
   - Add descriptive tags
   - Export for backup

4. **Run Complete Workflow:**
   ```bash
   # This will generate images, audio, and video
   python scripts/workflow.py projects/agentic_ai_example/
   ```

### Advanced Topics

- Read `PROMPT_ENGINEERING_GUIDE.md` for comprehensive documentation
- Explore `ARCHITECTURE.md` for system design details
- Check `prompt_config.py` to customize concepts and styles
- Review the visual prompt engineering research documents

## Troubleshooting

**Issue: "Module not found" error**
```bash
# Make sure you're in the project root
cd /path/to/LONGFORM-VIDEO-GENERATOR

# Ensure scripts are importable
export PYTHONPATH="${PYTHONPATH}:$(pwd)/scripts"
```

**Issue: Database locked**
```bash
# Close any open database connections
# Or specify a different database
python scripts/prompt_library.py --db /tmp/test.db stats
```

**Issue: No concepts detected**
- Add concept keywords to your narration
- See `prompt_config.py` for the full list of keywords
- Or manually specify style with `--style`

## Summary

In this tutorial, you:

✅ Generated your first optimized prompt  
✅ Processed a complete project with 12 segments  
✅ Saved a prompt to your library  
✅ Searched and reused library prompts  
✅ Ran the automated workflow  
✅ Viewed library statistics  

**Time Saved:** With the library, the second project took 0 seconds for prompt generation instead of ~2 minutes per segment!

**Next:** Read the full guide to learn about all features and workflows.

---

**Tutorial Version:** 1.0  
**Last Updated:** December 30, 2025  
**Author:** Manus AI
