"""
prompt_config.py - Configuration and knowledge base for visual prompt engineering.

Contains visual style definitions, concept-to-metaphor mappings, quality boosters,
and prompt templates based on the Agentic AI Visual Prompt Engineering research.
"""

from typing import Dict, List, Any

# ============================================================================
# VISUAL STYLES
# ============================================================================

VISUAL_STYLES: Dict[str, Dict[str, Any]] = {
    "minimalist": {
        "description": "Simple shapes, bright colors, no depth or texture",
        "keywords": ["flat design", "vector art", "minimalist", "simple shapes", "clean lines", "infographic style", "2D illustration", "solid colors"],
        "composition": ["clean background", "centered composition"],
        "quality_boosters": ["8K resolution", "sharp focus", "clean lines"],
        "negative_prompts": ["cluttered", "busy", "complex", "detailed background", "3d render"],
        "best_for": ["icons", "simple diagrams", "concept illustrations", "title cards"]
    },
    
    "isometric": {
        "description": "3D perspective with depth and structure",
        "keywords": ["isometric view", "isometric perspective", "3D render", "low poly", "voxel art", "axonometric projection"],
        "composition": ["structured layout", "geometric arrangement"],
        "quality_boosters": ["8K resolution", "sharp focus", "clean edges", "vibrant colors"],
        "negative_prompts": ["flat", "2D", "blurry", "distorted perspective"],
        "best_for": ["system architecture", "data flow", "complex relationships", "technical diagrams"]
    },
    
    "blueprint": {
        "description": "Technical drawing style showing internal workings",
        "keywords": ["blueprint style", "schematic diagram", "technical drawing", "wireframe", "HUD display", "engineering drawing", "CAD design"],
        "composition": ["technical layout", "grid background", "annotation style"],
        "quality_boosters": ["sharp focus", "precise lines", "technical accuracy"],
        "negative_prompts": ["photorealistic", "artistic", "painterly", "organic"],
        "best_for": ["internal mechanisms", "algorithms", "system components", "technical specifications"]
    },
    
    "cyberpunk": {
        "description": "High-tech, neon-lit, futuristic atmosphere",
        "keywords": ["cyberpunk", "neon glow", "holographic display", "futuristic UI", "sci-fi", "octane render", "unreal engine", "blade runner aesthetic"],
        "composition": ["dramatic lighting", "neon accents", "dark background"],
        "quality_boosters": ["8K resolution", "cinematic lighting", "volumetric light", "hyper-detailed"],
        "negative_prompts": ["bright", "cheerful", "minimalist", "simple"],
        "best_for": ["title cards", "establishing shots", "high-tech atmosphere", "engaging thumbnails"]
    },
    
    "photorealistic": {
        "description": "Realistic photographic look with cinematic quality",
        "keywords": ["photorealistic", "cinematic lighting", "volumetric light", "depth of field", "bokeh", "studio lighting"],
        "composition": ["cinematic composition", "dramatic angle", "professional photography"],
        "quality_boosters": ["8K resolution", "hyper-detailed", "sharp focus", "masterpiece", "trending on ArtStation"],
        "negative_prompts": ["cartoon", "illustration", "flat", "vector art", "low quality"],
        "best_for": ["hero shots", "high-impact visuals", "realism", "professional content"]
    }
}

# ============================================================================
# AGENTIC AI CONCEPTS
# ============================================================================

AGENTIC_CONCEPTS: Dict[str, Dict[str, Any]] = {
    "agent": {
        "keywords": ["agent", "autonomous", "AI entity", "intelligent system"],
        "metaphors": ["robot", "digital entity", "glowing orb", "stylized figure"],
        "visual_keywords": ["AI agent", "autonomous entity", "digital being", "robotic figure"],
        "default_style": "cyberpunk"
    },
    
    "multi-agent": {
        "keywords": ["multi-agent", "multiple agents", "agent team", "collaborative agents"],
        "metaphors": ["orchestra", "team", "network", "swarm"],
        "visual_keywords": ["multi-agent system", "team of agents", "network of AI", "swarm intelligence"],
        "default_style": "isometric"
    },
    
    "orchestration": {
        "keywords": ["orchestration", "coordination", "workflow", "management", "control"],
        "metaphors": ["conductor", "control panel", "flowchart", "command center"],
        "visual_keywords": ["orchestration", "coordination", "workflow management", "control system"],
        "default_style": "isometric"
    },
    
    "state_management": {
        "keywords": ["state", "memory", "persistence", "data storage", "state machine"],
        "metaphors": ["gears", "memory banks", "state machine diagram", "data vault"],
        "visual_keywords": ["state management", "memory", "data persistence", "state machine"],
        "default_style": "blueprint"
    },
    
    "decision_making": {
        "keywords": ["decision", "reasoning", "planning", "logic", "choice"],
        "metaphors": ["branching paths", "flowchart", "glowing core", "logic gates"],
        "visual_keywords": ["decision-making", "reasoning", "planning", "logic gates"],
        "default_style": "blueprint"
    },
    
    "memory": {
        "keywords": ["memory", "knowledge", "storage", "retrieval", "database"],
        "metaphors": ["library", "database", "crystalline structure", "data vault"],
        "visual_keywords": ["memory", "knowledge base", "data storage", "information retrieval"],
        "default_style": "photorealistic"
    },
    
    "planning": {
        "keywords": ["planning", "strategy", "goal", "roadmap", "task"],
        "metaphors": ["blueprint", "roadmap", "network of nodes", "strategic map"],
        "visual_keywords": ["planning", "strategy", "goal decomposition", "task planning"],
        "default_style": "blueprint"
    },
    
    "tool_use": {
        "keywords": ["tool", "function", "API", "capability", "integration"],
        "metaphors": ["toolbox", "robotic arm", "API connections", "interface"],
        "visual_keywords": ["tool use", "function calling", "API integration", "external tools"],
        "default_style": "isometric"
    },
    
    "observability": {
        "keywords": ["monitoring", "logging", "metrics", "observability", "tracking"],
        "metaphors": ["dashboard", "monitoring screen", "logs", "analytics display"],
        "visual_keywords": ["observability", "monitoring", "logging", "performance metrics"],
        "default_style": "cyberpunk"
    },
    
    "security": {
        "keywords": ["security", "protection", "access control", "authentication", "threat"],
        "metaphors": ["fortress", "shield", "lock and key", "guardian"],
        "visual_keywords": ["security", "protection", "access control", "threat detection"],
        "default_style": "cyberpunk"
    },
    
    "data_flow": {
        "keywords": ["data flow", "pipeline", "stream", "transfer", "processing"],
        "metaphors": ["streams of light", "pipelines", "rivers", "data streams"],
        "visual_keywords": ["data flow", "data stream", "information pipeline", "data transfer"],
        "default_style": "isometric"
    },
    
    "knowledge_graph": {
        "keywords": ["knowledge graph", "graph", "network", "relationships", "entities"],
        "metaphors": ["network of nodes", "constellation", "web of connections"],
        "visual_keywords": ["knowledge graph", "semantic network", "entity relationships", "graph database"],
        "default_style": "isometric"
    },
    
    "interoperability": {
        "keywords": ["interoperability", "integration", "connection", "bridge", "interface"],
        "metaphors": ["handshake", "bridge", "connector", "gateway"],
        "visual_keywords": ["interoperability", "integration", "cross-system communication", "API bridge"],
        "default_style": "minimalist"
    },
    
    "data_quality": {
        "keywords": ["data quality", "cleansing", "validation", "governance", "accuracy"],
        "metaphors": ["gardener", "filter", "refinery", "quality check"],
        "visual_keywords": ["data quality", "data cleansing", "data validation", "data integrity"],
        "default_style": "minimalist"
    }
}

# ============================================================================
# QUALITY BOOSTERS
# ============================================================================

QUALITY_BOOSTERS: List[str] = [
    "8K resolution",
    "hyper-detailed",
    "sharp focus",
    "cinematic lighting",
    "trending on ArtStation",
    "masterpiece",
    "high quality",
    "professional"
]

# ============================================================================
# NEGATIVE PROMPTS
# ============================================================================

NEGATIVE_PROMPTS: List[str] = [
    "blurry",
    "deformed",
    "ugly",
    "low quality",
    "bad anatomy",
    "extra limbs",
    "text",
    "watermark",
    "signature",
    "logo",
    "artist name",
    "cropped",
    "out of frame",
    "worst quality",
    "low res",
    "jpeg artifacts",
    "noise",
    "grain"
]

# ============================================================================
# PROMPT TEMPLATES
# ============================================================================

PROMPT_TEMPLATES: Dict[str, str] = {
    "master": "{subject} - {action} - {style} - {composition} - {quality}",
    
    "skill_1_orchestration": "A central, glowing AI entity, depicted as a conductor, leading an orchestra of smaller, specialized AI agents. Each agent is represented by a unique geometric shape and is connected to the conductor by lines of light. The background is a dark, futuristic concert hall.",
    
    "skill_2_interoperability": "Two stylized, robotic hands, one representing a legacy system and the other a modern AI, shaking hands. Glowing data streams are flowing between their connected fingers. The background is a neutral, minimalist environment.",
    
    "skill_3_observability": "A futuristic, holographic dashboard displaying intricate charts, graphs, and logs of an AI agent's performance. The dashboard is being viewed by a stylized, non-humanoid AI figure. The environment is a dark, high-tech control room.",
    
    "skill_4_memory": "A luminous, crystalline brain structure with distinct, color-coded sections representing different memory types. Data streams are flowing into and out of the structure, connecting it to a vast, digital library in the background.",
    
    "skill_5_context": "A set of futuristic, glowing scales. On one side, a large, chaotic mass of data. On the other, a single, perfectly formed, glowing data token. The scales are perfectly balanced, symbolizing optimization.",
    
    "skill_6_data_quality": "A stylized, robotic gardener tending to a vibrant, digital garden. The gardener is carefully removing dark, thorny weeds and watering glowing, healthy plants. The garden is arranged in neat, orderly rows, representing a well-governed data ecosystem.",
    
    "skill_7_identity": "A series of massive, glowing digital gates, each with a unique, complex keyhole. A single, stylized AI agent, represented as a key master, is holding a ring of glowing keys, ready to unlock the gates.",
    
    "skill_8_capability": "A high-tech, futuristic workbench. A stylized, robotic blacksmith is using a glowing hammer to forge new tools from streams of raw data. Sparks of light and code are flying from the anvil.",
    
    "skill_9_security": "A massive, glowing, digital fortress with high walls and watchtowers. AI guardians, represented as knights of light, are defending the fortress from a swarm of dark, shadowy creatures attempting to breach the walls."
}

# ============================================================================
# PLATFORM CONFIGURATIONS
# ============================================================================

PLATFORM_CONFIGS: Dict[str, Dict[str, Any]] = {
    "nano-banana-pro": {
        "aspect_ratio": "16:9",
        "style_param": "raw",
        "stylize_value": 750,
        "format_string": "--ar {aspect_ratio} --style {style_param} --stylize {stylize_value}"
    },
    
    "midjourney": {
        "aspect_ratio": "16:9",
        "style_param": "raw",
        "stylize_value": 750,
        "format_string": "--ar {aspect_ratio} --style {style_param} --stylize {stylize_value}"
    },
    
    "dalle3": {
        "aspect_ratio": "16:9",
        "format_string": ""  # DALL-E uses natural language
    },
    
    "stable-diffusion": {
        "aspect_ratio": "16:9",
        "format_string": ""  # Uses natural language with negative prompts
    }
}

# ============================================================================
# DEFAULT CONFIGURATION
# ============================================================================

DEFAULT_CONFIG: Dict[str, Any] = {
    "default_style": "isometric",
    "platform": "nano-banana-pro",
    "aspect_ratio": "16:9",
    "include_quality_boosters": True,
    "include_negative_prompts": True,
    "consistency_mode": "moderate",  # strict, moderate, flexible
    "concept_detection": True,
    "auto_style_selection": True
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_style_config(style_name: str) -> Dict[str, Any]:
    """Get configuration for a specific visual style."""
    return VISUAL_STYLES.get(style_name, VISUAL_STYLES["isometric"])


def get_concept_config(concept_name: str) -> Dict[str, Any]:
    """Get configuration for a specific Agentic AI concept."""
    return AGENTIC_CONCEPTS.get(concept_name, {})


def get_quality_boosters(count: int = None) -> List[str]:
    """Get quality booster keywords."""
    if count:
        return QUALITY_BOOSTERS[:count]
    return QUALITY_BOOSTERS


def get_negative_prompts(additional: List[str] = None) -> List[str]:
    """Get negative prompt keywords, optionally with additional ones."""
    prompts = NEGATIVE_PROMPTS.copy()
    if additional:
        prompts.extend(additional)
    return prompts


def get_platform_format(platform: str, **kwargs) -> str:
    """Get platform-specific format string."""
    config = PLATFORM_CONFIGS.get(platform, PLATFORM_CONFIGS["nano-banana-pro"])
    
    # Merge default values with provided kwargs
    params = {
        "aspect_ratio": kwargs.get("aspect_ratio", config.get("aspect_ratio", "16:9")),
        "style_param": config.get("style_param", "raw"),
        "stylize_value": config.get("stylize_value", 750)
    }
    
    format_string = config.get("format_string", "")
    if format_string:
        return format_string.format(**params)
    return ""


def detect_concepts_in_text(text: str) -> List[str]:
    """
    Detect Agentic AI concepts in text.
    
    Args:
        text: The text to analyze (narration)
        
    Returns:
        List of detected concept names
    """
    text_lower = text.lower()
    detected = []
    
    for concept_name, concept_config in AGENTIC_CONCEPTS.items():
        keywords = concept_config.get("keywords", [])
        for keyword in keywords:
            if keyword.lower() in text_lower:
                detected.append(concept_name)
                break  # Only add once per concept
    
    return detected


def select_style_for_concepts(concepts: List[str]) -> str:
    """
    Select the most appropriate visual style based on detected concepts.
    
    Args:
        concepts: List of detected concept names
        
    Returns:
        Style name
    """
    if not concepts:
        return DEFAULT_CONFIG["default_style"]
    
    # Get default styles for each concept
    styles = []
    for concept in concepts:
        concept_config = get_concept_config(concept)
        if concept_config:
            styles.append(concept_config.get("default_style", "isometric"))
    
    # Return most common style, or first if tie
    if styles:
        return max(set(styles), key=styles.count)
    
    return DEFAULT_CONFIG["default_style"]


def get_visual_keywords_for_concepts(concepts: List[str]) -> List[str]:
    """
    Get visual keywords for a list of concepts.
    
    Args:
        concepts: List of concept names
        
    Returns:
        List of visual keywords
    """
    keywords = []
    for concept in concepts:
        concept_config = get_concept_config(concept)
        if concept_config:
            keywords.extend(concept_config.get("visual_keywords", []))
    return keywords


def get_metaphors_for_concepts(concepts: List[str]) -> List[str]:
    """
    Get visual metaphors for a list of concepts.
    
    Args:
        concepts: List of concept names
        
    Returns:
        List of metaphor descriptions
    """
    metaphors = []
    for concept in concepts:
        concept_config = get_concept_config(concept)
        if concept_config:
            metaphors.extend(concept_config.get("metaphors", []))
    return metaphors
