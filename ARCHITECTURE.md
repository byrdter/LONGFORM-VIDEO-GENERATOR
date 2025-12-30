# Enhanced Architecture: Visual Prompt Engineering Integration

**Author:** Manus AI  
**Date:** December 30, 2025  
**Version:** 1.0

## Overview

This document describes the enhanced architecture that integrates the Agentic AI Visual Prompt Engineering system into the existing LONGFORM-VIDEO-GENERATOR workflow. The enhancement adds intelligent prompt generation, a persistent prompt library, and automated optimization capabilities.

## Current Architecture Analysis

### Existing Workflow

```
1. User writes segments.json
   ├── narration (text)
   └── image_prompt (manual text prompt)
   
2. generate_image.py batch
   └── Generates images from image_prompt
   
3. generate_voice.py batch
   └── Generates audio from narration
   
4. create_segment.py batch
   └── Combines image + audio + Ken Burns
   
5. assemble_video.py
   └── Final video assembly
```

### Current Limitations

1. **Manual Prompt Creation:** Users must manually craft image prompts for each segment
2. **No Prompt Optimization:** No guidance on quality boosters, negative prompts, or style consistency
3. **No Prompt Library:** Successful prompts are not saved for reuse
4. **No Context Awareness:** Prompts don't leverage the Agentic AI domain knowledge
5. **No Iteration Support:** No easy way to refine prompts based on results

## Enhanced Architecture

### New Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Enhanced Workflow                         │
└─────────────────────────────────────────────────────────────┘

1. User writes segments.json (with narration only)
   └── narration (text describing the concept)
   
2. NEW: prompt_generator.py
   ├── Analyzes narration for Agentic AI concepts
   ├── Generates optimized image prompts using research
   ├── Applies style consistency rules
   ├── Adds quality boosters and negative prompts
   └── Saves to enhanced segments.json
   
3. NEW: prompt_library.py
   ├── Stores successful prompts
   ├── Allows rating and tagging
   ├── Enables search and reuse
   └── Tracks prompt performance
   
4. generate_image.py batch (unchanged)
   └── Generates images from enhanced prompts
   
5. NEW: prompt_refiner.py (optional)
   ├── Analyzes generated images
   ├── Suggests prompt improvements
   └── Updates prompt library
   
6-8. Existing pipeline (unchanged)
```

## Module Design

### Module 1: `prompt_generator.py`

**Purpose:** Generate optimized image prompts from narration text and concept analysis.

**Key Features:**
- Concept detection (identifies Agentic AI concepts from narration)
- Visual metaphor selection (maps concepts to visual representations)
- Style application (applies consistent visual style)
- Prompt construction (uses five-layer architecture)
- Quality enhancement (adds boosters and negative prompts)

**Input:** segments.json with narration
**Output:** Enhanced segments.json with generated image_prompt fields

**Core Functions:**
```python
def analyze_narration(text: str) -> List[str]
    """Detect Agentic AI concepts in narration text."""
    
def select_visual_metaphor(concepts: List[str]) -> Dict
    """Choose appropriate visual metaphor for concepts."""
    
def generate_prompt(narration: str, style: str, config: Dict) -> str
    """Generate complete optimized image prompt."""
    
def enhance_segments_file(input_file: str, output_file: str, config: Dict)
    """Process entire segments.json and add prompts."""
```

### Module 2: `prompt_library.py`

**Purpose:** Persistent storage and management of successful prompts.

**Key Features:**
- SQLite database for prompt storage
- Rating system (1-5 stars)
- Tagging system (concepts, styles, use cases)
- Search functionality
- Usage tracking
- Export/import capabilities

**Database Schema:**
```sql
CREATE TABLE prompts (
    id INTEGER PRIMARY KEY,
    prompt_text TEXT NOT NULL,
    narration_context TEXT,
    concepts TEXT,  -- JSON array
    style TEXT,
    rating INTEGER,
    tags TEXT,  -- JSON array
    image_path TEXT,
    created_at TIMESTAMP,
    used_count INTEGER DEFAULT 0
);

CREATE TABLE prompt_history (
    id INTEGER PRIMARY KEY,
    prompt_id INTEGER,
    segment_id TEXT,
    project_name TEXT,
    used_at TIMESTAMP,
    FOREIGN KEY (prompt_id) REFERENCES prompts(id)
);
```

**Core Functions:**
```python
def save_prompt(prompt: str, metadata: Dict) -> int
    """Save a prompt to the library."""
    
def search_prompts(query: str, filters: Dict) -> List[Dict]
    """Search prompts by text, concepts, or tags."""
    
def rate_prompt(prompt_id: int, rating: int)
    """Rate a prompt (1-5 stars)."""
    
def get_similar_prompts(narration: str, limit: int) -> List[Dict]
    """Find similar prompts based on narration."""
    
def export_library(output_file: str)
    """Export library to JSON for backup/sharing."""
```

### Module 3: `prompt_config.py`

**Purpose:** Configuration and knowledge base for prompt generation.

**Key Features:**
- Visual style definitions
- Concept-to-metaphor mappings
- Quality booster templates
- Negative prompt templates
- Platform-specific configurations

**Data Structures:**
```python
VISUAL_STYLES = {
    "minimalist": {
        "keywords": ["flat design", "vector art", "clean lines"],
        "quality_boosters": ["8K", "sharp focus"],
        "negative_prompts": ["cluttered", "complex"]
    },
    "isometric": {...},
    "blueprint": {...},
    "cyberpunk": {...},
    "photorealistic": {...}
}

AGENTIC_CONCEPTS = {
    "multi-agent": {
        "metaphors": ["orchestra", "team", "network"],
        "keywords": ["multi-agent system", "coordination"]
    },
    "orchestration": {...},
    "state management": {...},
    # ... all 9 skills
}

PROMPT_TEMPLATES = {
    "master": "[SUBJECT] - [ACTION] - [STYLE] - [COMPOSITION] - [QUALITY]",
    "skill_1": "...",
    # ... templates for each skill
}
```

### Module 4: `prompt_refiner.py` (Optional)

**Purpose:** Analyze generated images and suggest prompt improvements.

**Key Features:**
- Image quality analysis
- Prompt effectiveness scoring
- Automatic refinement suggestions
- A/B testing support

**Core Functions:**
```python
def analyze_image(image_path: str) -> Dict
    """Analyze image quality and characteristics."""
    
def suggest_improvements(prompt: str, image_analysis: Dict) -> List[str]
    """Suggest prompt refinements based on results."""
    
def compare_variants(prompts: List[str], images: List[str]) -> Dict
    """Compare multiple prompt variants."""
```

## Integration Points

### 1. Enhanced segments.json Schema

Add optional fields while maintaining backward compatibility:

```json
{
  "project_name": "Agentic AI Skills",
  "voice": "en-GB-RyanNeural",
  "visual_config": {
    "primary_style": "isometric",
    "secondary_style": "flat",
    "color_palette": ["#0066FF", "#00FFCC", "#FF00FF"],
    "consistency_mode": "strict"
  },
  "chapters": [
    {
      "chapter_id": 1,
      "title": "Multi-Agent Orchestration",
      "segments": [
        {
          "segment_id": "001",
          "narration": "Multi-agent systems coordinate...",
          "agentic_concepts": ["multi-agent", "orchestration"],
          "image_prompt": "AUTO",  // or manual prompt
          "image_prompt_generated": "...",  // auto-generated
          "image_prompt_source": "auto|manual|library",
          "prompt_library_id": 42,  // if from library
          "visual_style": "isometric",
          "ken_burns_sequence": ["zoom_in"],
          "transition": "fade"
        }
      ]
    }
  ]
}
```

### 2. CLI Integration

New commands added to existing workflow:

```bash
# Generate prompts from narration
python scripts/prompt_generator.py \
    --segments projects/my_project/segments.json \
    --style isometric \
    --output projects/my_project/segments_enhanced.json

# Search prompt library
python scripts/prompt_library.py search \
    --query "multi-agent orchestration" \
    --style isometric

# Save successful prompt to library
python scripts/prompt_library.py save \
    --prompt "A central AI conductor..." \
    --concepts "orchestration,multi-agent" \
    --rating 5 \
    --image projects/my_project/images/001.png

# Export library
python scripts/prompt_library.py export \
    --output my_prompt_library.json
```

### 3. Workflow Integration

**Option A: Automatic Mode**
```bash
# 1. Write segments.json with narration only
# 2. Auto-generate prompts
python scripts/prompt_generator.py --segments segments.json

# 3. Continue with existing workflow
python scripts/generate_image.py batch --segments segments.json ...
```

**Option B: Interactive Mode**
```bash
# Generate prompts with review
python scripts/prompt_generator.py \
    --segments segments.json \
    --interactive

# System shows generated prompt, user can:
# - Accept (a)
# - Edit (e)
# - Search library (s)
# - Skip (k)
```

**Option C: Hybrid Mode**
```bash
# Use library for known concepts, generate for new ones
python scripts/prompt_generator.py \
    --segments segments.json \
    --use-library \
    --fallback-generate
```

## Configuration System

### Global Config: `prompt_config.yaml`

```yaml
# Default visual style
default_style: isometric

# Style preferences by concept
concept_styles:
  orchestration: isometric
  security: cyberpunk
  memory: photorealistic

# Quality settings
quality:
  resolution: 8K
  boosters:
    - hyper-detailed
    - sharp focus
    - cinematic lighting
  
# Negative prompts (always applied)
negative_prompts:
  - blurry
  - deformed
  - text
  - watermark

# Platform settings
platform: nano-banana-pro
platform_params:
  style: raw
  stylize: 750
  aspect_ratio: "16:9"

# Library settings
library:
  path: ~/.prompt_library.db
  auto_save: true
  min_rating_for_reuse: 4
```

### Project-Specific Config: `projects/my_project/prompt_config.yaml`

```yaml
# Override global settings for this project
primary_style: cyberpunk
color_palette:
  - "#FF00FF"
  - "#00FFCC"

# Concept detection
detect_concepts: true
concept_keywords:
  orchestration:
    - "coordinate"
    - "manage"
    - "control"
```

## Data Flow

### Prompt Generation Flow

```
1. Load segments.json
   ↓
2. For each segment:
   ├── Extract narration
   ├── Detect Agentic AI concepts
   ├── Check prompt library for similar prompts
   ├── If found: Use library prompt (with rating > threshold)
   └── If not found: Generate new prompt
       ├── Select visual metaphor
       ├── Choose style (from config)
       ├── Construct prompt (5-layer architecture)
       ├── Add quality boosters
       ├── Add negative prompts
       └── Format for platform
   ↓
3. Save enhanced segments.json
   ↓
4. Optionally: Review and refine prompts
   ↓
5. Continue to generate_image.py
```

### Prompt Library Flow

```
1. User generates images
   ↓
2. User reviews results
   ↓
3. For successful images:
   ├── Rate prompt (1-5 stars)
   ├── Add tags
   ├── Save to library
   └── Link to image file
   ↓
4. Library builds knowledge base
   ↓
5. Future projects can search/reuse prompts
```

## Implementation Priority

### Phase 1: Core Functionality (MVP)
- [ ] `prompt_config.py` - Configuration and knowledge base
- [ ] `prompt_generator.py` - Basic prompt generation
- [ ] `prompt_library.py` - Database and storage
- [ ] Integration with existing generate_image.py

### Phase 2: Enhanced Features
- [ ] Concept detection from narration
- [ ] Library search and reuse
- [ ] Interactive mode
- [ ] Configuration system

### Phase 3: Advanced Features
- [ ] `prompt_refiner.py` - Image analysis and refinement
- [ ] A/B testing support
- [ ] Batch optimization
- [ ] Analytics and reporting

## Backward Compatibility

All enhancements maintain full backward compatibility:

1. **Existing segments.json files work unchanged**
2. **Manual prompts are preserved** (not overwritten)
3. **New fields are optional**
4. **Existing scripts work without modification**

Users can adopt the new system incrementally:
- Start with manual prompts (current workflow)
- Add prompt generation for new projects
- Gradually build prompt library
- Eventually automate most prompt creation

## Success Metrics

- **Time Savings:** 70%+ reduction in prompt creation time
- **Quality Improvement:** Higher average image quality scores
- **Consistency:** Uniform visual style across projects
- **Reusability:** 50%+ of prompts reused from library
- **Scalability:** Handle 100+ segment projects efficiently
