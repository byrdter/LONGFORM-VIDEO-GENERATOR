"""
prompt_generator.py - Generate optimized image prompts from narration text.

Analyzes narration to detect Agentic AI concepts, selects appropriate visual
metaphors and styles, and constructs high-quality image prompts using the
five-layer architecture.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

from prompt_config import (
    get_style_config,
    get_concept_config,
    get_quality_boosters,
    get_negative_prompts,
    get_platform_format,
    detect_concepts_in_text,
    select_style_for_concepts,
    get_visual_keywords_for_concepts,
    get_metaphors_for_concepts,
    PROMPT_TEMPLATES,
    DEFAULT_CONFIG
)


class PromptGenerator:
    """Generate optimized image prompts from narration text."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the prompt generator.
        
        Args:
            config: Configuration dictionary (uses DEFAULT_CONFIG if None)
        """
        self.config = config or DEFAULT_CONFIG.copy()
    
    def analyze_narration(self, narration: str) -> Dict[str, Any]:
        """
        Analyze narration text to detect concepts and context.
        
        Args:
            narration: The narration text
            
        Returns:
            Dictionary with analysis results
        """
        concepts = detect_concepts_in_text(narration)
        
        return {
            "narration": narration,
            "concepts": concepts,
            "primary_concept": concepts[0] if concepts else None,
            "suggested_style": select_style_for_concepts(concepts),
            "visual_keywords": get_visual_keywords_for_concepts(concepts),
            "metaphors": get_metaphors_for_concepts(concepts)
        }
    
    def construct_prompt(
        self,
        subject: str,
        action: str = "",
        style: str = None,
        composition: str = "",
        additional_keywords: List[str] = None
    ) -> str:
        """
        Construct a prompt using the five-layer architecture.
        
        Args:
            subject: Core subject/concept (Layer 1)
            action: Action/context (Layer 2)
            style: Visual style name (Layer 3)
            composition: Composition/lighting (Layer 4)
            additional_keywords: Additional keywords to include
            
        Returns:
            Complete prompt string
        """
        style = style or self.config["default_style"]
        style_config = get_style_config(style)
        
        # Build prompt layers
        layers = []
        
        # Layer 1: Subject
        layers.append(subject)
        
        # Layer 2: Action/Context
        if action:
            layers.append(action)
        
        # Layer 3: Style keywords
        style_keywords = style_config.get("keywords", [])
        if style_keywords:
            layers.append(", ".join(style_keywords[:3]))  # Use top 3
        
        # Layer 4: Composition
        if composition:
            layers.append(composition)
        elif style_config.get("composition"):
            layers.append(", ".join(style_config["composition"][:2]))
        
        # Layer 5: Quality boosters
        if self.config.get("include_quality_boosters", True):
            quality = get_quality_boosters(count=4)
            layers.append(", ".join(quality))
        
        # Additional keywords
        if additional_keywords:
            layers.append(", ".join(additional_keywords))
        
        # Combine all layers
        prompt = ". ".join(layers)
        
        # Add platform-specific formatting
        platform_format = get_platform_format(
            self.config.get("platform", "nano-banana-pro"),
            aspect_ratio=self.config.get("aspect_ratio", "16:9")
        )
        if platform_format:
            prompt += f" {platform_format}"
        
        return prompt
    
    def generate_from_narration(
        self,
        narration: str,
        style: str = None,
        use_template: bool = False
    ) -> Dict[str, Any]:
        """
        Generate a complete prompt from narration text.
        
        Args:
            narration: The narration text
            style: Override style (uses auto-detection if None)
            use_template: Use predefined template if available
            
        Returns:
            Dictionary with prompt and metadata
        """
        # Analyze narration
        analysis = self.analyze_narration(narration)
        
        # Determine style
        final_style = style or analysis["suggested_style"]
        
        # Check if we have a predefined template
        if use_template and analysis["primary_concept"]:
            template_key = f"skill_{analysis['primary_concept']}"
            if template_key in PROMPT_TEMPLATES:
                base_prompt = PROMPT_TEMPLATES[template_key]
                style_config = get_style_config(final_style)
                
                # Add style keywords to template
                style_keywords = ", ".join(style_config.get("keywords", [])[:3])
                quality = ", ".join(get_quality_boosters(count=4))
                
                prompt = f"{base_prompt} {style_keywords}, {quality}"
                
                # Add platform format
                platform_format = get_platform_format(
                    self.config.get("platform", "nano-banana-pro")
                )
                if platform_format:
                    prompt += f" {platform_format}"
                
                return {
                    "prompt": prompt,
                    "negative_prompt": ", ".join(get_negative_prompts()),
                    "style": final_style,
                    "concepts": analysis["concepts"],
                    "source": "template",
                    "analysis": analysis
                }
        
        # Generate from scratch
        # Create subject from metaphors and visual keywords
        metaphors = analysis["metaphors"]
        visual_keywords = analysis["visual_keywords"]
        
        if metaphors and visual_keywords:
            subject = f"{visual_keywords[0]} represented as {metaphors[0]}"
        elif visual_keywords:
            subject = visual_keywords[0]
        else:
            # Fallback: extract key phrases from narration
            subject = self._extract_subject_from_narration(narration)
        
        # Create action/context from narration
        action = self._extract_action_from_narration(narration)
        
        # Construct prompt
        prompt = self.construct_prompt(
            subject=subject,
            action=action,
            style=final_style,
            additional_keywords=visual_keywords[1:3] if len(visual_keywords) > 1 else None
        )
        
        # Get negative prompts
        style_config = get_style_config(final_style)
        negative = get_negative_prompts(
            additional=style_config.get("negative_prompts", [])
        )
        
        return {
            "prompt": prompt,
            "negative_prompt": ", ".join(negative),
            "style": final_style,
            "concepts": analysis["concepts"],
            "source": "generated",
            "analysis": analysis
        }
    
    def _extract_subject_from_narration(self, narration: str) -> str:
        """Extract a subject description from narration text."""
        # Simple extraction: take first sentence or clause
        sentences = narration.split('.')
        if sentences:
            first = sentences[0].strip()
            # Limit length
            if len(first) > 100:
                first = first[:100] + "..."
            return first
        return "An abstract visualization of the concept"
    
    def _extract_action_from_narration(self, narration: str) -> str:
        """Extract action/context from narration text."""
        # Look for action verbs
        action_verbs = [
            "analyzing", "processing", "managing", "coordinating",
            "monitoring", "protecting", "generating", "optimizing",
            "integrating", "orchestrating"
        ]
        
        narration_lower = narration.lower()
        for verb in action_verbs:
            if verb in narration_lower:
                return f"{verb} data and information"
        
        return "in a futuristic environment"
    
    def enhance_segments_file(
        self,
        input_file: str,
        output_file: str = None,
        style: str = None,
        overwrite: bool = False,
        interactive: bool = False
    ) -> None:
        """
        Process a segments.json file and add generated prompts.
        
        Args:
            input_file: Path to input segments.json
            output_file: Path to output file (overwrites input if None)
            style: Override style for all segments
            overwrite: Overwrite existing prompts
            interactive: Prompt user for review/editing
        """
        output_file = output_file or input_file
        
        # Load segments
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add visual config if not present
        if "visual_config" not in data:
            data["visual_config"] = {
                "primary_style": style or self.config["default_style"],
                "consistency_mode": self.config.get("consistency_mode", "moderate"),
                "platform": self.config.get("platform", "nano-banana-pro")
            }
        
        total_segments = 0
        generated_count = 0
        skipped_count = 0
        
        # Process each segment
        for chapter in data.get("chapters", []):
            for segment in chapter.get("segments", []):
                total_segments += 1
                segment_id = segment.get("segment_id", "unknown")
                
                # Check if prompt already exists
                if segment.get("image_prompt") and not overwrite:
                    if segment["image_prompt"] != "AUTO":
                        print(f"[{segment_id}] Skipping (prompt exists)")
                        skipped_count += 1
                        continue
                
                # Get narration
                narration = segment.get("narration", "")
                if not narration:
                    print(f"[{segment_id}] Skipping (no narration)")
                    skipped_count += 1
                    continue
                
                # Generate prompt
                print(f"[{segment_id}] Generating prompt...")
                result = self.generate_from_narration(
                    narration,
                    style=style or data["visual_config"].get("primary_style")
                )
                
                # Interactive mode
                if interactive:
                    print(f"\nNarration: {narration}")
                    print(f"\nGenerated Prompt:\n{result['prompt']}")
                    print(f"\nNegative Prompt:\n{result['negative_prompt']}")
                    print(f"\nDetected Concepts: {', '.join(result['concepts'])}")
                    print(f"Style: {result['style']}")
                    
                    choice = input("\n[A]ccept, [E]dit, [S]kip? ").strip().lower()
                    
                    if choice == 's':
                        print("Skipped.")
                        skipped_count += 1
                        continue
                    elif choice == 'e':
                        edited_prompt = input("Enter edited prompt: ").strip()
                        if edited_prompt:
                            result['prompt'] = edited_prompt
                            result['source'] = 'manual'
                
                # Save to segment
                segment["image_prompt"] = result["prompt"]
                segment["image_prompt_negative"] = result["negative_prompt"]
                segment["image_prompt_source"] = result["source"]
                segment["agentic_concepts"] = result["concepts"]
                segment["visual_style"] = result["style"]
                
                generated_count += 1
                print(f"[{segment_id}] ✓ Prompt generated")
        
        # Save enhanced file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*60}")
        print(f"Summary:")
        print(f"  Total segments: {total_segments}")
        print(f"  Generated: {generated_count}")
        print(f"  Skipped: {skipped_count}")
        print(f"  Output: {output_file}")
        print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate optimized image prompts from narration text"
    )
    
    subparsers = parser.add_subparsers(dest="command")
    
    # Single prompt generation
    single = subparsers.add_parser("single", help="Generate a single prompt")
    single.add_argument("--narration", required=True, help="Narration text")
    single.add_argument("--style", help="Visual style (minimalist, isometric, blueprint, cyberpunk, photorealistic)")
    single.add_argument("--template", action="store_true", help="Use predefined template if available")
    single.add_argument("--output", help="Output file for prompt (optional)")
    
    # Batch processing
    batch = subparsers.add_parser("batch", help="Process segments.json file")
    batch.add_argument("--segments", required=True, help="Path to segments.json")
    batch.add_argument("--output", help="Output file (overwrites input if not specified)")
    batch.add_argument("--style", help="Override style for all segments")
    batch.add_argument("--overwrite", action="store_true", help="Overwrite existing prompts")
    batch.add_argument("--interactive", action="store_true", help="Review each prompt interactively")
    
    # Configuration
    parser.add_argument("--platform", default="nano-banana-pro", help="Target platform")
    parser.add_argument("--aspect-ratio", default="16:9", help="Aspect ratio")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Create config
    config = DEFAULT_CONFIG.copy()
    config["platform"] = args.platform
    config["aspect_ratio"] = args.aspect_ratio
    
    # Create generator
    generator = PromptGenerator(config)
    
    if args.command == "single":
        # Generate single prompt
        result = generator.generate_from_narration(
            args.narration,
            style=args.style,
            use_template=args.template
        )
        
        print("\n" + "="*60)
        print("GENERATED PROMPT:")
        print("="*60)
        print(result["prompt"])
        print("\n" + "="*60)
        print("NEGATIVE PROMPT:")
        print("="*60)
        print(result["negative_prompt"])
        print("\n" + "="*60)
        print(f"Style: {result['style']}")
        print(f"Detected Concepts: {', '.join(result['concepts']) if result['concepts'] else 'None'}")
        print(f"Source: {result['source']}")
        print("="*60)
        
        # Save if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\nSaved to: {args.output}")
    
    elif args.command == "batch":
        # Process segments file
        generator.enhance_segments_file(
            input_file=args.segments,
            output_file=args.output,
            style=args.style,
            overwrite=args.overwrite,
            interactive=args.interactive
        )


if __name__ == "__main__":
    main()
