"""
prompt_library.py - Persistent storage and management of successful prompts.

Provides a SQLite-based library for storing, searching, rating, and reusing
image prompts. Includes tagging, usage tracking, and export/import capabilities.
"""

import argparse
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

from prompt_config import detect_concepts_in_text


class PromptLibrary:
    """Manage a persistent library of image prompts."""
    
    def __init__(self, db_path: str = None):
        """
        Initialize the prompt library.
        
        Args:
            db_path: Path to SQLite database (default: ~/.prompt_library.db)
        """
        if db_path is None:
            db_path = str(Path.home() / ".prompt_library.db")
        
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Access columns by name
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema."""
        cursor = self.conn.cursor()
        
        # Prompts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt_text TEXT NOT NULL,
                negative_prompt TEXT,
                narration_context TEXT,
                concepts TEXT,
                style TEXT,
                rating INTEGER DEFAULT 0,
                tags TEXT,
                image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used_count INTEGER DEFAULT 0,
                notes TEXT
            )
        """)
        
        # Prompt history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompt_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt_id INTEGER NOT NULL,
                segment_id TEXT,
                project_name TEXT,
                used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (prompt_id) REFERENCES prompts(id)
            )
        """)
        
        # Create indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_prompts_rating 
            ON prompts(rating)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_prompts_style 
            ON prompts(style)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_prompts_concepts 
            ON prompts(concepts)
        """)
        
        self.conn.commit()
    
    def save_prompt(
        self,
        prompt: str,
        negative_prompt: str = None,
        narration: str = None,
        concepts: List[str] = None,
        style: str = None,
        rating: int = 0,
        tags: List[str] = None,
        image_path: str = None,
        notes: str = None
    ) -> int:
        """
        Save a prompt to the library.
        
        Args:
            prompt: The image prompt text
            negative_prompt: Negative prompt text
            narration: Original narration context
            concepts: List of Agentic AI concepts
            style: Visual style used
            rating: Rating (0-5 stars)
            tags: List of tags
            image_path: Path to generated image
            notes: Additional notes
            
        Returns:
            Prompt ID
        """
        # Auto-detect concepts if not provided
        if concepts is None and narration:
            concepts = detect_concepts_in_text(narration)
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO prompts (
                prompt_text, negative_prompt, narration_context,
                concepts, style, rating, tags, image_path, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prompt,
            negative_prompt,
            narration,
            json.dumps(concepts) if concepts else None,
            style,
            rating,
            json.dumps(tags) if tags else None,
            image_path,
            notes
        ))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def update_prompt(
        self,
        prompt_id: int,
        rating: int = None,
        tags: List[str] = None,
        image_path: str = None,
        notes: str = None
    ) -> bool:
        """
        Update an existing prompt.
        
        Args:
            prompt_id: Prompt ID
            rating: New rating
            tags: New tags
            image_path: New image path
            notes: New notes
            
        Returns:
            True if successful
        """
        updates = []
        values = []
        
        if rating is not None:
            updates.append("rating = ?")
            values.append(rating)
        
        if tags is not None:
            updates.append("tags = ?")
            values.append(json.dumps(tags))
        
        if image_path is not None:
            updates.append("image_path = ?")
            values.append(image_path)
        
        if notes is not None:
            updates.append("notes = ?")
            values.append(notes)
        
        if not updates:
            return False
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        values.append(prompt_id)
        
        cursor = self.conn.cursor()
        cursor.execute(f"""
            UPDATE prompts 
            SET {', '.join(updates)}
            WHERE id = ?
        """, values)
        
        self.conn.commit()
        return cursor.rowcount > 0
    
    def rate_prompt(self, prompt_id: int, rating: int) -> bool:
        """
        Rate a prompt (1-5 stars).
        
        Args:
            prompt_id: Prompt ID
            rating: Rating (1-5)
            
        Returns:
            True if successful
        """
        if not 0 <= rating <= 5:
            raise ValueError("Rating must be between 0 and 5")
        
        return self.update_prompt(prompt_id, rating=rating)
    
    def search_prompts(
        self,
        query: str = None,
        concepts: List[str] = None,
        style: str = None,
        min_rating: int = None,
        tags: List[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search prompts in the library.
        
        Args:
            query: Text search in prompt and narration
            concepts: Filter by concepts
            style: Filter by style
            min_rating: Minimum rating
            tags: Filter by tags
            limit: Maximum results
            
        Returns:
            List of matching prompts
        """
        conditions = []
        values = []
        
        if query:
            conditions.append("(prompt_text LIKE ? OR narration_context LIKE ?)")
            values.extend([f"%{query}%", f"%{query}%"])
        
        if concepts:
            for concept in concepts:
                conditions.append("concepts LIKE ?")
                values.append(f"%{concept}%")
        
        if style:
            conditions.append("style = ?")
            values.append(style)
        
        if min_rating is not None:
            conditions.append("rating >= ?")
            values.append(min_rating)
        
        if tags:
            for tag in tags:
                conditions.append("tags LIKE ?")
                values.append(f"%{tag}%")
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        cursor = self.conn.cursor()
        cursor.execute(f"""
            SELECT * FROM prompts
            WHERE {where_clause}
            ORDER BY rating DESC, used_count DESC, created_at DESC
            LIMIT ?
        """, values + [limit])
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_prompt(self, prompt_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific prompt by ID.
        
        Args:
            prompt_id: Prompt ID
            
        Returns:
            Prompt dictionary or None
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_similar_prompts(
        self,
        narration: str,
        limit: int = 5,
        min_rating: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Find similar prompts based on narration.
        
        Args:
            narration: Narration text to match
            limit: Maximum results
            min_rating: Minimum rating
            
        Returns:
            List of similar prompts
        """
        # Detect concepts in narration
        concepts = detect_concepts_in_text(narration)
        
        if not concepts:
            # Fallback to text search
            return self.search_prompts(
                query=narration[:50],  # First 50 chars
                min_rating=min_rating,
                limit=limit
            )
        
        # Search by concepts
        return self.search_prompts(
            concepts=concepts,
            min_rating=min_rating,
            limit=limit
        )
    
    def record_usage(
        self,
        prompt_id: int,
        segment_id: str = None,
        project_name: str = None
    ) -> bool:
        """
        Record usage of a prompt.
        
        Args:
            prompt_id: Prompt ID
            segment_id: Segment ID where used
            project_name: Project name
            
        Returns:
            True if successful
        """
        cursor = self.conn.cursor()
        
        # Add to history
        cursor.execute("""
            INSERT INTO prompt_history (prompt_id, segment_id, project_name)
            VALUES (?, ?, ?)
        """, (prompt_id, segment_id, project_name))
        
        # Increment usage count
        cursor.execute("""
            UPDATE prompts
            SET used_count = used_count + 1
            WHERE id = ?
        """, (prompt_id,))
        
        self.conn.commit()
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get library statistics.
        
        Returns:
            Dictionary with statistics
        """
        cursor = self.conn.cursor()
        
        # Total prompts
        cursor.execute("SELECT COUNT(*) FROM prompts")
        total = cursor.fetchone()[0]
        
        # By rating
        cursor.execute("""
            SELECT rating, COUNT(*) as count
            FROM prompts
            GROUP BY rating
            ORDER BY rating DESC
        """)
        by_rating = {row[0]: row[1] for row in cursor.fetchall()}
        
        # By style
        cursor.execute("""
            SELECT style, COUNT(*) as count
            FROM prompts
            WHERE style IS NOT NULL
            GROUP BY style
            ORDER BY count DESC
        """)
        by_style = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Most used
        cursor.execute("""
            SELECT id, prompt_text, used_count, rating
            FROM prompts
            ORDER BY used_count DESC
            LIMIT 5
        """)
        most_used = [dict(zip(['id', 'prompt', 'used_count', 'rating'], row)) 
                     for row in cursor.fetchall()]
        
        # Highest rated
        cursor.execute("""
            SELECT id, prompt_text, rating, used_count
            FROM prompts
            WHERE rating > 0
            ORDER BY rating DESC, used_count DESC
            LIMIT 5
        """)
        highest_rated = [dict(zip(['id', 'prompt', 'rating', 'used_count'], row)) 
                        for row in cursor.fetchall()]
        
        return {
            "total_prompts": total,
            "by_rating": by_rating,
            "by_style": by_style,
            "most_used": most_used,
            "highest_rated": highest_rated
        }
    
    def export_library(self, output_file: str) -> bool:
        """
        Export library to JSON file.
        
        Args:
            output_file: Output file path
            
        Returns:
            True if successful
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM prompts ORDER BY created_at DESC")
        
        prompts = []
        for row in cursor.fetchall():
            prompt_dict = dict(row)
            # Parse JSON fields
            if prompt_dict.get('concepts'):
                prompt_dict['concepts'] = json.loads(prompt_dict['concepts'])
            if prompt_dict.get('tags'):
                prompt_dict['tags'] = json.loads(prompt_dict['tags'])
            prompts.append(prompt_dict)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "exported_at": datetime.now().isoformat(),
                "total_prompts": len(prompts),
                "prompts": prompts
            }, f, indent=2, ensure_ascii=False)
        
        return True
    
    def import_library(self, input_file: str, merge: bool = True) -> int:
        """
        Import prompts from JSON file.
        
        Args:
            input_file: Input file path
            merge: If True, merge with existing; if False, replace
            
        Returns:
            Number of prompts imported
        """
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not merge:
            # Clear existing data
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM prompt_history")
            cursor.execute("DELETE FROM prompts")
            self.conn.commit()
        
        imported = 0
        for prompt_data in data.get('prompts', []):
            try:
                self.save_prompt(
                    prompt=prompt_data['prompt_text'],
                    negative_prompt=prompt_data.get('negative_prompt'),
                    narration=prompt_data.get('narration_context'),
                    concepts=prompt_data.get('concepts'),
                    style=prompt_data.get('style'),
                    rating=prompt_data.get('rating', 0),
                    tags=prompt_data.get('tags'),
                    image_path=prompt_data.get('image_path'),
                    notes=prompt_data.get('notes')
                )
                imported += 1
            except Exception as e:
                print(f"Error importing prompt: {e}")
        
        return imported
    
    def delete_prompt(self, prompt_id: int) -> bool:
        """
        Delete a prompt from the library.
        
        Args:
            prompt_id: Prompt ID
            
        Returns:
            True if successful
        """
        cursor = self.conn.cursor()
        
        # Delete history
        cursor.execute("DELETE FROM prompt_history WHERE prompt_id = ?", (prompt_id,))
        
        # Delete prompt
        cursor.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
        
        self.conn.commit()
        return cursor.rowcount > 0
    
    def close(self):
        """Close the database connection."""
        self.conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Manage the prompt library"
    )
    
    subparsers = parser.add_subparsers(dest="command")
    
    # Save prompt
    save = subparsers.add_parser("save", help="Save a prompt to the library")
    save.add_argument("--prompt", required=True, help="Prompt text")
    save.add_argument("--negative", help="Negative prompt")
    save.add_argument("--narration", help="Original narration")
    save.add_argument("--concepts", help="Comma-separated concepts")
    save.add_argument("--style", help="Visual style")
    save.add_argument("--rating", type=int, default=0, help="Rating (0-5)")
    save.add_argument("--tags", help="Comma-separated tags")
    save.add_argument("--image", help="Path to generated image")
    save.add_argument("--notes", help="Additional notes")
    
    # Search prompts
    search = subparsers.add_parser("search", help="Search the library")
    search.add_argument("--query", help="Text search query")
    search.add_argument("--concepts", help="Comma-separated concepts")
    search.add_argument("--style", help="Visual style")
    search.add_argument("--min-rating", type=int, help="Minimum rating")
    search.add_argument("--tags", help="Comma-separated tags")
    search.add_argument("--limit", type=int, default=10, help="Max results")
    
    # Rate prompt
    rate = subparsers.add_parser("rate", help="Rate a prompt")
    rate.add_argument("--id", type=int, required=True, help="Prompt ID")
    rate.add_argument("--rating", type=int, required=True, help="Rating (0-5)")
    
    # Statistics
    stats = subparsers.add_parser("stats", help="Show library statistics")
    
    # Export
    export = subparsers.add_parser("export", help="Export library to JSON")
    export.add_argument("--output", required=True, help="Output file")
    
    # Import
    import_cmd = subparsers.add_parser("import", help="Import library from JSON")
    import_cmd.add_argument("--input", required=True, help="Input file")
    import_cmd.add_argument("--replace", action="store_true", help="Replace existing library")
    
    # Database path
    parser.add_argument("--db", help="Database path (default: ~/.prompt_library.db)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Create library
    library = PromptLibrary(db_path=args.db)
    
    try:
        if args.command == "save":
            concepts = args.concepts.split(',') if args.concepts else None
            tags = args.tags.split(',') if args.tags else None
            
            prompt_id = library.save_prompt(
                prompt=args.prompt,
                negative_prompt=args.negative,
                narration=args.narration,
                concepts=concepts,
                style=args.style,
                rating=args.rating,
                tags=tags,
                image_path=args.image,
                notes=args.notes
            )
            
            print(f"✓ Saved prompt with ID: {prompt_id}")
        
        elif args.command == "search":
            concepts = args.concepts.split(',') if args.concepts else None
            tags = args.tags.split(',') if args.tags else None
            
            results = library.search_prompts(
                query=args.query,
                concepts=concepts,
                style=args.style,
                min_rating=args.min_rating,
                tags=tags,
                limit=args.limit
            )
            
            print(f"\nFound {len(results)} prompts:\n")
            for result in results:
                print(f"ID: {result['id']}")
                print(f"Prompt: {result['prompt_text'][:100]}...")
                print(f"Style: {result['style']}")
                print(f"Rating: {'⭐' * result['rating']}")
                print(f"Used: {result['used_count']} times")
                print("-" * 60)
        
        elif args.command == "rate":
            success = library.rate_prompt(args.id, args.rating)
            if success:
                print(f"✓ Rated prompt {args.id} with {args.rating} stars")
            else:
                print(f"✗ Failed to rate prompt {args.id}")
        
        elif args.command == "stats":
            stats = library.get_statistics()
            
            print("\n" + "="*60)
            print("PROMPT LIBRARY STATISTICS")
            print("="*60)
            print(f"\nTotal Prompts: {stats['total_prompts']}")
            
            print("\nBy Rating:")
            for rating in sorted(stats['by_rating'].keys(), reverse=True):
                stars = '⭐' * rating if rating > 0 else 'Unrated'
                print(f"  {stars}: {stats['by_rating'][rating]}")
            
            print("\nBy Style:")
            for style, count in stats['by_style'].items():
                print(f"  {style}: {count}")
            
            print("\nMost Used:")
            for i, prompt in enumerate(stats['most_used'], 1):
                print(f"  {i}. ID {prompt['id']}: {prompt['used_count']} uses, {prompt['rating']}⭐")
            
            print("\nHighest Rated:")
            for i, prompt in enumerate(stats['highest_rated'], 1):
                print(f"  {i}. ID {prompt['id']}: {prompt['rating']}⭐, {prompt['used_count']} uses")
            
            print("="*60)
        
        elif args.command == "export":
            library.export_library(args.output)
            print(f"✓ Exported library to: {args.output}")
        
        elif args.command == "import":
            count = library.import_library(args.input, merge=not args.replace)
            action = "Replaced" if args.replace else "Imported"
            print(f"✓ {action} {count} prompts")
    
    finally:
        library.close()


if __name__ == "__main__":
    main()
