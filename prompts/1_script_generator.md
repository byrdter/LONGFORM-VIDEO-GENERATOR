# Prompt 1: Documentary Script Generator

Use this prompt with Claude, GPT, or another AI assistant to generate a complete documentary script.

---

## The Prompt

```
You are an expert documentary scriptwriter. Your task is to write a compelling, well-researched narration script for a documentary video.

## Project Details

**Topic**: [INSERT YOUR TOPIC HERE - e.g., "The Fall of the Roman Empire", "The Apollo 11 Moon Landing", "Life on Mars in 2150"]

**Target Duration**: [INSERT DURATION - e.g., "30-35 minutes of narration"]

**Tone**: [INSERT TONE - e.g., "Thoughtful and dramatic, like a Ken Burns documentary" or "Epic and inspiring, like a National Geographic special" or "Mysterious and speculative, like a science fiction exploration"]

**Audience**: [INSERT AUDIENCE - e.g., "General audience interested in history" or "Science enthusiasts" or "Young adults interested in space exploration"]

## Structure Requirements

Organize the script into **4-6 chapters**, each covering a major theme, time period, or aspect of the topic. Each chapter should be roughly 5-8 minutes of narration when read aloud at a measured pace.

## For Each Chapter, Provide:

1. **Chapter Title** - A compelling, evocative title
2. **Opening Hook** - 1-2 sentences that grab attention and set the scene
3. **Main Narration** - The body of the chapter, written as flowing prose paragraphs (NOT bullet points)
4. **Closing Transition** - 1-2 sentences that lead naturally into the next chapter

## Writing Guidelines

**Voice & Style:**
- Write in present tense for immediacy ("The emperor stands..." not "The emperor stood...")
- Use second person sparingly for impact ("Imagine yourself standing at the gates...")
- Vary sentence length - short punchy sentences for impact, longer ones for description
- This will be READ ALOUD - write for the ear, not the eye

**Content Quality:**
- Include specific details: names, dates, places, numbers
- Balance big-picture themes with human-scale stories
- Use vivid sensory descriptions (sights, sounds, textures)
- Include moments of emotional resonance

**Pacing:**
- Open each chapter with something visual/dramatic that could be illustrated
- Build tension and release it
- End chapters on moments of significance or anticipation

**Avoid:**
- Bullet points or lists (this is flowing narration)
- Academic jargon without explanation
- Excessive hedging ("perhaps", "maybe", "some historians think")
- Modern slang or anachronistic language

## Output Format

For each chapter:

---
## Chapter [N]: [Title]

[Opening hook paragraph]

[Main narration - multiple paragraphs of flowing prose]

[Closing transition to next chapter]

---

## Begin

Write the complete documentary script for the topic specified above. Aim for approximately [WORD COUNT - e.g., "4,500-5,500 words total"] to achieve the target duration.
```

---

## Example Usage

If your topic is "The Silk Road", you might fill in:

- **Topic**: "The Silk Road: Ancient Highway of Civilizations"
- **Target Duration**: "30 minutes of narration"
- **Tone**: "Epic and educational, emphasizing the human connections across vast distances"
- **Audience**: "History enthusiasts and general viewers interested in trade, culture, and adventure"

---

## Tips for Best Results

1. **Be Specific About Tone**: "Like a Ken Burns documentary" gives the AI a clear style reference
2. **Specify What to Emphasize**: If you want more human stories vs. political history, say so
3. **Request Specific Elements**: "Include at least 3 specific historical figures" or "Include sensory descriptions of the landscape"
4. **Iterate**: Generate once, then ask the AI to expand weak sections or add more detail to specific chapters

---

## What to Do With the Output

1. Review the script for accuracy (AI can make factual errors)
2. Adjust pacing - read sections aloud to check flow
3. Note which parts would make strong visual moments (for image prompts later)
4. Save as `script.md` in your project folder
5. Move on to Prompt 2: Segment Planner
