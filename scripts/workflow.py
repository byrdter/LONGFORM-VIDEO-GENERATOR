"""
workflow.py - Integrated workflow for automated video generation with prompt engineering.

Combines prompt generation, library management, and video generation into a
streamlined workflow.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any

from prompt_generator import PromptGenerator
from prompt_library import PromptLibrary
from prompt_config import DEFAULT_CONFIG


class VideoWorkflow:
    """Integrated workflow for video generation with prompt engineering."""
    
    def __init__(
        self,
        project_dir: str,
        use_library: bool = True,
        library_db: str = None
    ):
        """
        Initialize the workflow.
        
        Args:
            project_dir: Project directory path
            use_library: Whether to use the prompt library
            library_db: Path to library database
        """
        self.project_dir = Path(project_dir)
        self.segments_file = self.project_dir / "segments.json"
        
        # Initialize components
        self.generator = PromptGenerator()
        self.library = PromptLibrary(db_path=library_db) if use_library else None
        
        # Directories
        self.images_dir = self.project_dir / "images"
        self.audio_dir = self.project_dir / "audio"
        self.clips_dir = self.project_dir / "clips"
        
        # Ensure directories exist
        for dir_path in [self.images_dir, self.audio_dir, self.clips_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def enhance_prompts(
        self,
        style: str = None,
        use_library: bool = True,
        interactive: bool = False
    ) -> Dict[str, Any]:
        """
        Enhance segments.json with generated prompts.
        
        Args:
            style: Override visual style
            use_library: Use library for similar prompts
            interactive: Interactive mode
            
        Returns:
            Statistics dictionary
        """
        print("\n" + "="*60)
        print("STEP 1: PROMPT GENERATION")
        print("="*60 + "\n")
        
        # Load segments
        with open(self.segments_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        stats = {
            "total": 0,
            "generated": 0,
            "from_library": 0,
            "skipped": 0,
            "manual": 0
        }
        
        # Process each segment
        for chapter in data.get("chapters", []):
            for segment in chapter.get("segments", []):
                stats["total"] += 1
                segment_id = segment.get("segment_id", "unknown")
                
                # Check if prompt already exists
                if segment.get("image_prompt") and segment["image_prompt"] != "AUTO":
                    print(f"[{segment_id}] Using existing prompt")
                    stats["manual"] += 1
                    continue
                
                narration = segment.get("narration", "")
                if not narration:
                    print(f"[{segment_id}] No narration, skipping")
                    stats["skipped"] += 1
                    continue
                
                # Try library first
                library_prompt = None
                if use_library and self.library:
                    similar = self.library.get_similar_prompts(
                        narration,
                        limit=3,
                        min_rating=4
                    )
                    
                    if similar:
                        print(f"[{segment_id}] Found {len(similar)} similar prompts in library")
                        
                        if interactive:
                            print(f"\nNarration: {narration}\n")
                            for i, prompt_data in enumerate(similar, 1):
                                print(f"{i}. (ID: {prompt_data['id']}, Rating: {prompt_data['rating']}⭐)")
                                print(f"   {prompt_data['prompt_text'][:100]}...\n")
                            
                            choice = input("Use library prompt? [1-3/n]: ").strip()
                            if choice.isdigit() and 1 <= int(choice) <= len(similar):
                                library_prompt = similar[int(choice) - 1]
                        else:
                            # Auto-select highest rated
                            library_prompt = similar[0]
                
                # Generate or use library
                if library_prompt:
                    segment["image_prompt"] = library_prompt["prompt_text"]
                    segment["image_prompt_negative"] = library_prompt.get("negative_prompt", "")
                    segment["image_prompt_source"] = "library"
                    segment["prompt_library_id"] = library_prompt["id"]
                    
                    # Record usage
                    self.library.record_usage(
                        library_prompt["id"],
                        segment_id=segment_id,
                        project_name=data.get("project_name")
                    )
                    
                    print(f"[{segment_id}] ✓ Using library prompt (ID: {library_prompt['id']})")
                    stats["from_library"] += 1
                else:
                    # Generate new prompt
                    print(f"[{segment_id}] Generating new prompt...")
                    result = self.generator.generate_from_narration(
                        narration,
                        style=style
                    )
                    
                    segment["image_prompt"] = result["prompt"]
                    segment["image_prompt_negative"] = result["negative_prompt"]
                    segment["image_prompt_source"] = "generated"
                    segment["agentic_concepts"] = result["concepts"]
                    segment["visual_style"] = result["style"]
                    
                    print(f"[{segment_id}] ✓ Generated prompt")
                    stats["generated"] += 1
        
        # Save enhanced segments
        with open(self.segments_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*60}")
        print("Prompt Generation Summary:")
        print(f"  Total segments: {stats['total']}")
        print(f"  Generated: {stats['generated']}")
        print(f"  From library: {stats['from_library']}")
        print(f"  Manual/existing: {stats['manual']}")
        print(f"  Skipped: {stats['skipped']}")
        print(f"{'='*60}\n")
        
        return stats
    
    def generate_images(self, delay: float = 2.0) -> bool:
        """
        Generate images using the existing generate_image.py script.
        
        Args:
            delay: Delay between API calls
            
        Returns:
            True if successful
        """
        print("\n" + "="*60)
        print("STEP 2: IMAGE GENERATION")
        print("="*60 + "\n")
        
        cmd = [
            sys.executable,
            str(Path(__file__).parent / "generate_image.py"),
            "batch",
            "--segments", str(self.segments_file),
            "--output-dir", str(self.images_dir),
            "--delay", str(delay)
        ]
        
        result = subprocess.run(cmd)
        return result.returncode == 0
    
    def generate_audio(self) -> bool:
        """
        Generate audio using the existing generate_voice.py script.
        
        Returns:
            True if successful
        """
        print("\n" + "="*60)
        print("STEP 3: AUDIO GENERATION")
        print("="*60 + "\n")
        
        cmd = [
            sys.executable,
            str(Path(__file__).parent / "generate_voice.py"),
            "batch",
            "--segments", str(self.segments_file),
            "--output-dir", str(self.audio_dir)
        ]
        
        result = subprocess.run(cmd)
        return result.returncode == 0
    
    def create_segments(self, music_dir: str = None) -> bool:
        """
        Create video segments using the existing create_segment.py script.
        
        Args:
            music_dir: Music directory path
            
        Returns:
            True if successful
        """
        print("\n" + "="*60)
        print("STEP 4: VIDEO SEGMENT CREATION")
        print("="*60 + "\n")
        
        music_dir = music_dir or str(Path(__file__).parent.parent / "music")
        
        cmd = [
            sys.executable,
            str(Path(__file__).parent / "create_segment.py"),
            "batch",
            "--segments", str(self.segments_file),
            "--images-dir", str(self.images_dir),
            "--audio-dir", str(self.audio_dir),
            "--output-dir", str(self.clips_dir),
            "--music-dir", music_dir
        ]
        
        result = subprocess.run(cmd)
        return result.returncode == 0
    
    def assemble_video(self, output_file: str = None) -> bool:
        """
        Assemble final video using the existing assemble_video.py script.
        
        Args:
            output_file: Output video file path
            
        Returns:
            True if successful
        """
        print("\n" + "="*60)
        print("STEP 5: FINAL VIDEO ASSEMBLY")
        print("="*60 + "\n")
        
        output_file = output_file or str(self.project_dir / "final_video.mp4")
        
        cmd = [
            sys.executable,
            str(Path(__file__).parent / "assemble_video.py"),
            "--clips-dir", str(self.clips_dir),
            "--segments", str(self.segments_file),
            "--output", output_file
        ]
        
        result = subprocess.run(cmd)
        return result.returncode == 0
    
    def review_and_save_prompts(self) -> int:
        """
        Review generated images and save successful prompts to library.
        
        Returns:
            Number of prompts saved
        """
        if not self.library:
            print("Library not enabled")
            return 0
        
        print("\n" + "="*60)
        print("PROMPT REVIEW & LIBRARY SAVE")
        print("="*60 + "\n")
        
        # Load segments
        with open(self.segments_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        saved_count = 0
        
        for chapter in data.get("chapters", []):
            for segment in chapter.get("segments", []):
                segment_id = segment.get("segment_id")
                
                # Skip if from library
                if segment.get("image_prompt_source") == "library":
                    continue
                
                # Check if image exists
                image_path = self.images_dir / f"{segment_id}.png"
                if not image_path.exists():
                    continue
                
                prompt = segment.get("image_prompt")
                if not prompt:
                    continue
                
                print(f"\n[{segment_id}]")
                print(f"Prompt: {prompt[:100]}...")
                print(f"Image: {image_path}")
                
                # Ask for rating
                rating_input = input("Rate this prompt (0-5, or 's' to skip): ").strip()
                
                if rating_input.lower() == 's':
                    continue
                
                try:
                    rating = int(rating_input)
                    if not 0 <= rating <= 5:
                        print("Invalid rating, skipping")
                        continue
                except ValueError:
                    print("Invalid input, skipping")
                    continue
                
                # Ask for tags
                tags_input = input("Tags (comma-separated, optional): ").strip()
                tags = [t.strip() for t in tags_input.split(',')] if tags_input else None
                
                # Save to library
                prompt_id = self.library.save_prompt(
                    prompt=prompt,
                    negative_prompt=segment.get("image_prompt_negative"),
                    narration=segment.get("narration"),
                    concepts=segment.get("agentic_concepts"),
                    style=segment.get("visual_style"),
                    rating=rating,
                    tags=tags,
                    image_path=str(image_path)
                )
                
                print(f"✓ Saved to library (ID: {prompt_id})")
                saved_count += 1
        
        print(f"\n{'='*60}")
        print(f"Saved {saved_count} prompts to library")
        print(f"{'='*60}\n")
        
        return saved_count
    
    def run_full_workflow(
        self,
        style: str = None,
        use_library: bool = True,
        interactive: bool = False,
        skip_review: bool = False
    ) -> bool:
        """
        Run the complete workflow from prompts to final video.
        
        Args:
            style: Visual style override
            use_library: Use prompt library
            interactive: Interactive mode
            skip_review: Skip prompt review step
            
        Returns:
            True if successful
        """
        print("\n" + "="*60)
        print("INTEGRATED VIDEO GENERATION WORKFLOW")
        print("="*60)
        print(f"Project: {self.project_dir.name}")
        print(f"Segments: {self.segments_file}")
        print("="*60 + "\n")
        
        # Step 1: Enhance prompts
        self.enhance_prompts(
            style=style,
            use_library=use_library,
            interactive=interactive
        )
        
        # Step 2: Generate images
        if not self.generate_images():
            print("✗ Image generation failed")
            return False
        
        # Step 3: Generate audio
        if not self.generate_audio():
            print("✗ Audio generation failed")
            return False
        
        # Step 4: Create segments
        if not self.create_segments():
            print("✗ Segment creation failed")
            return False
        
        # Step 5: Assemble video
        if not self.assemble_video():
            print("✗ Video assembly failed")
            return False
        
        # Step 6: Review and save prompts (optional)
        if not skip_review and self.library:
            self.review_and_save_prompts()
        
        print("\n" + "="*60)
        print("✓ WORKFLOW COMPLETE!")
        print("="*60 + "\n")
        
        return True
    
    def close(self):
        """Clean up resources."""
        if self.library:
            self.library.close()


def main():
    parser = argparse.ArgumentParser(
        description="Integrated workflow for video generation with prompt engineering"
    )
    
    parser.add_argument(
        "project_dir",
        help="Project directory path"
    )
    
    parser.add_argument(
        "--style",
        choices=["minimalist", "isometric", "blueprint", "cyberpunk", "photorealistic"],
        help="Visual style override"
    )
    
    parser.add_argument(
        "--no-library",
        action="store_true",
        help="Disable prompt library"
    )
    
    parser.add_argument(
        "--library-db",
        help="Path to library database"
    )
    
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode for prompt review"
    )
    
    parser.add_argument(
        "--skip-review",
        action="store_true",
        help="Skip prompt review step"
    )
    
    parser.add_argument(
        "--prompts-only",
        action="store_true",
        help="Only generate prompts, don't create video"
    )
    
    args = parser.parse_args()
    
    # Create workflow
    workflow = VideoWorkflow(
        project_dir=args.project_dir,
        use_library=not args.no_library,
        library_db=args.library_db
    )
    
    try:
        if args.prompts_only:
            # Only enhance prompts
            workflow.enhance_prompts(
                style=args.style,
                use_library=not args.no_library,
                interactive=args.interactive
            )
        else:
            # Run full workflow
            success = workflow.run_full_workflow(
                style=args.style,
                use_library=not args.no_library,
                interactive=args.interactive,
                skip_review=args.skip_review
            )
            
            if not success:
                sys.exit(1)
    
    finally:
        workflow.close()


if __name__ == "__main__":
    main()
