#!/usr/bin/env python3
"""
Lightweight Tag Management System with Database Support and Document Synchronization

Features:
- SQLite database for tag storage and indexing
- Add/Edit/Delete tag operations
- Document label synchronization
- Full-text search on documents
- Tag statistics and analytics
- Batch operations on documents
"""

import sqlite3
import json
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import argparse
import sys

@dataclass
class Tag:
    """Tag data structure"""
    name: str
    category: str
    description: str = ""
    created_at: str = ""
    usage_count: int = 0

@dataclass
class Document:
    """Document data structure"""
    path: str
    title: str = ""
    tags: List[str] = None
    content_hash: str = ""
    last_updated: str = ""

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class TagManager:
    """Main tag management system"""

    def __init__(self, db_path: str = "tags.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tags table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                name TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usage_count INTEGER DEFAULT 0
            )
        ''')

        # Documents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                path TEXT PRIMARY KEY,
                title TEXT,
                content_hash TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Document-Tag relationship table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_tags (
                document_path TEXT,
                tag_name TEXT,
                PRIMARY KEY (document_path, tag_name),
                FOREIGN KEY (document_path) REFERENCES documents(path) ON DELETE CASCADE,
                FOREIGN KEY (tag_name) REFERENCES tags(name) ON DELETE CASCADE
            )
        ''')

        # Full-text search index
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS document_search USING fts5(
                path, title, content, tags
            )
        ''')

        # Create indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags_category ON tags(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags_usage ON tags(usage_count DESC)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_documents_updated ON documents(last_updated DESC)')

        conn.commit()
        conn.close()

    def add_tag(self, name: str, category: str, description: str = "") -> bool:
        """Add a new tag"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT OR REPLACE INTO tags (name, category, description, created_at)
                VALUES (?, ?, ?, ?)
            ''', (name, category, description, datetime.now().isoformat()))

            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error adding tag: {e}")
            return False

    def edit_tag(self, name: str, new_name: str = None, category: str = None, description: str = None) -> bool:
        """Edit an existing tag"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            updates = []
            params = []

            if new_name:
                updates.append("name = ?")
                params.append(new_name)
            if category:
                updates.append("category = ?")
                params.append(category)
            if description is not None:
                updates.append("description = ?")
                params.append(description)

            if not updates:
                conn.close()
                return False

            params.append(name)
            query = f"UPDATE tags SET {', '.join(updates)} WHERE name = ?"
            cursor.execute(query, params)

            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error editing tag: {e}")
            return False

    def delete_tag(self, name: str) -> bool:
        """Delete a tag (cascade deletes document relationships)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM tags WHERE name = ?", (name,))

            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting tag: {e}")
            return False

    def list_tags(self, category: str = None, sort_by: str = "name") -> List[Tag]:
        """List all tags, optionally filtered by category"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if category:
                cursor.execute('''
                    SELECT name, category, description, created_at, usage_count
                    FROM tags WHERE category = ?
                    ORDER BY ?
                ''', (category, sort_by))
            else:
                cursor.execute('''
                    SELECT name, category, description, created_at, usage_count
                    FROM tags ORDER BY ?
                ''', (sort_by,))

            tags = []
            for row in cursor.fetchall():
                tags.append(Tag(*row))

            conn.close()
            return tags
        except sqlite3.Error as e:
            print(f"Error listing tags: {e}")
            return []

    def get_tag_categories(self) -> List[str]:
        """Get all unique tag categories"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT DISTINCT category FROM tags ORDER BY category")
            categories = [row[0] for row in cursor.fetchall()]

            conn.close()
            return categories
        except sqlite3.Error as e:
            print(f"Error getting categories: {e}")
            return []

    def scan_document_tags(self, doc_path: str) -> Set[str]:
        """Extract tags from document content using bracketed format [Tag1][Tag2]"""
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find all bracketed tags: [Tag_Name]
            tags = set(re.findall(r'\[([^\]]+)\]', content))
            return tags
        except Exception as e:
            print(f"Error scanning document {doc_path}: {e}")
            return set()

    def sync_document(self, doc_path: str, force_update: bool = False) -> bool:
        """Synchronize document tags with database"""
        try:
            doc_path = str(Path(doc_path).resolve())

            # Calculate content hash
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            content_hash = hash(content)

            # Check if document needs updating
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT content_hash FROM documents WHERE path = ?", (doc_path,))
            existing = cursor.fetchone()

            if existing and not force_update and existing[0] == str(content_hash):
                conn.close()
                return True  # No update needed

            # Extract title from first line or filename
            lines = content.strip().split('\n')
            title = lines[0].strip('# ') if lines else Path(doc_path).stem

            # Extract tags from content
            extracted_tags = self.scan_document_tags(doc_path)

            # Update/insert document
            cursor.execute('''
                INSERT OR REPLACE INTO documents (path, title, content_hash, last_updated)
                VALUES (?, ?, ?, ?)
            ''', (doc_path, title, str(content_hash), datetime.now().isoformat()))

            # Clear existing tag relationships
            cursor.execute("DELETE FROM document_tags WHERE document_path = ?", (doc_path,))

            # Add new tag relationships and create tags if needed
            for tag_name in extracted_tags:
                # Auto-create tag if it doesn't exist
                cursor.execute('''
                    INSERT OR IGNORE INTO tags (name, category, created_at, usage_count)
                    VALUES (?, 'Auto-detected', ?, 0)
                ''', (tag_name, datetime.now().isoformat()))

                # Add relationship
                cursor.execute('''
                    INSERT INTO document_tags (document_path, tag_name)
                    VALUES (?, ?)
                ''', (doc_path, tag_name))

                # Update usage count
                cursor.execute('''
                    UPDATE tags SET usage_count = usage_count + 1 WHERE name = ?
                ''', (tag_name,))

            # Update full-text search index
            cursor.execute('''
                INSERT OR REPLACE INTO document_search (path, title, content, tags)
                VALUES (?, ?, ?, ?)
            ''', (doc_path, title, content, ' '.join(extracted_tags)))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error syncing document {doc_path}: {e}")
            return False

    def sync_directory(self, directory: str, pattern: str = "*.md", force_update: bool = False) -> Dict[str, bool]:
        """Sync all documents in a directory"""
        results = {}
        directory_path = Path(directory)

        if not directory_path.exists():
            print(f"Directory {directory} does not exist")
            return results

        for doc_path in directory_path.rglob(pattern):
            try:
                success = self.sync_document(doc_path, force_update)
                results[str(doc_path)] = success
                if success:
                    print(f"✅ Synced: {doc_path}")
                else:
                    print(f"❌ Failed to sync: {doc_path}")
            except Exception as e:
                print(f"❌ Error syncing {doc_path}: {e}")
                results[str(doc_path)] = False

        return results

    def search_documents(self, query: str) -> List[Dict]:
        """Full-text search on documents"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT d.path, d.title, d.last_updated, snippet(document_search, 2, '<mark>', '</mark>', '...', 32) as snippet
                FROM document_search ds
                JOIN documents d ON ds.path = d.path
                WHERE document_search MATCH ?
                ORDER BY rank
            ''', (query,))

            results = []
            for row in cursor.fetchall():
                results.append({
                    'path': row[0],
                    'title': row[1],
                    'last_updated': row[2],
                    'snippet': row[3]
                })

            conn.close()
            return results
        except sqlite3.Error as e:
            print(f"Error searching documents: {e}")
            return []

    def get_documents_by_tag(self, tag_name: str) -> List[Dict]:
        """Get all documents that have a specific tag"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT d.path, d.title, d.last_updated
                FROM documents d
                JOIN document_tags dt ON d.path = dt.document_path
                WHERE dt.tag_name = ?
                ORDER BY d.last_updated DESC
            ''', (tag_name,))

            results = []
            for row in cursor.fetchall():
                results.append({
                    'path': row[0],
                    'title': row[1],
                    'last_updated': row[2]
                })

            conn.close()
            return results
        except sqlite3.Error as e:
            print(f"Error getting documents by tag: {e}")
            return []

    def get_tag_analytics(self) -> Dict:
        """Get tag usage statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Most used tags
            cursor.execute("SELECT name, usage_count FROM tags ORDER BY usage_count DESC LIMIT 10")
            top_tags = [{'name': row[0], 'count': row[1]} for row in cursor.fetchall()]

            # Category distribution
            cursor.execute("SELECT category, COUNT(*) FROM tags GROUP BY category ORDER BY COUNT(*) DESC")
            category_dist = [{'category': row[0], 'count': row[1]} for row in cursor.fetchall()]

            # Total stats
            cursor.execute("SELECT COUNT(*) FROM tags")
            total_tags = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM documents")
            total_documents = cursor.fetchone()[0]

            conn.close()

            return {
                'total_tags': total_tags,
                'total_documents': total_documents,
                'top_tags': top_tags,
                'category_distribution': category_dist
            }
        except sqlite3.Error as e:
            print(f"Error getting analytics: {e}")
            return {}

    def export_tags(self, output_file: str):
        """Export tags to JSON file"""
        try:
            tags = self.list_tags()
            tags_data = [asdict(tag) for tag in tags]

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(tags_data, f, indent=2, ensure_ascii=False)

            print(f"Exported {len(tags)} tags to {output_file}")
        except Exception as e:
            print(f"Error exporting tags: {e}")

    def import_tags(self, input_file: str):
        """Import tags from JSON file"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                tags_data = json.load(f)

            for tag_data in tags_data:
                self.add_tag(
                    name=tag_data['name'],
                    category=tag_data['category'],
                    description=tag_data.get('description', '')
                )

            print(f"Imported {len(tags_data)} tags from {input_file}")
        except Exception as e:
            print(f"Error importing tags: {e}")

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(description="Tag Management System")
    parser.add_argument('--db', default='tags.db', help='Database file path')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add tag
    add_parser = subparsers.add_parser('add-tag', help='Add a new tag')
    add_parser.add_argument('name', help='Tag name')
    add_parser.add_argument('category', help='Tag category')
    add_parser.add_argument('--desc', default='', help='Tag description')

    # Edit tag
    edit_parser = subparsers.add_parser('edit-tag', help='Edit a tag')
    edit_parser.add_argument('name', help='Current tag name')
    edit_parser.add_argument('--new-name', help='New tag name')
    edit_parser.add_argument('--category', help='New category')
    edit_parser.add_argument('--desc', help='New description')

    # Delete tag
    delete_parser = subparsers.add_parser('delete-tag', help='Delete a tag')
    delete_parser.add_argument('name', help='Tag name to delete')

    # List tags
    list_parser = subparsers.add_parser('list-tags', help='List all tags')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--sort', default='name', choices=['name', 'category', 'usage_count'], help='Sort by field')

    # Sync document
    sync_parser = subparsers.add_parser('sync', help='Sync document tags')
    sync_parser.add_argument('path', help='Document or directory path')
    sync_parser.add_argument('--pattern', default='*.md', help='File pattern for directory sync')
    sync_parser.add_argument('--force', action='store_true', help='Force update')

    # Search
    search_parser = subparsers.add_parser('search', help='Search documents')
    search_parser.add_argument('query', help='Search query')

    # Analytics
    subparsers.add_parser('analytics', help='Show tag analytics')

    # Export/Import
    export_parser = subparsers.add_parser('export', help='Export tags to JSON')
    export_parser.add_argument('output_file', help='Output JSON file')

    import_parser = subparsers.add_parser('import', help='Import tags from JSON')
    import_parser.add_argument('input_file', help='Input JSON file')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    tm = TagManager(args.db)

    if args.command == 'add-tag':
        success = tm.add_tag(args.name, args.category, args.desc)
        print(f"✅ Tag '{args.name}' added successfully" if success else f"❌ Failed to add tag")

    elif args.command == 'edit-tag':
        success = tm.edit_tag(args.name, args.new_name, args.category, args.desc)
        print(f"✅ Tag '{args.name}' updated successfully" if success else f"❌ Failed to update tag")

    elif args.command == 'delete-tag':
        success = tm.delete_tag(args.name)
        print(f"✅ Tag '{args.name}' deleted successfully" if success else f"❌ Failed to delete tag")

    elif args.command == 'list-tags':
        tags = tm.list_tags(args.category, args.sort)
        if tags:
            print(f"\n📋 Found {len(tags)} tags:")
            for tag in tags:
                print(f"  • [{tag.category}] {tag.name} (used {tag.usage_count} times)")
                if tag.description:
                    print(f"    {tag.description}")
        else:
            print("No tags found")

    elif args.command == 'sync':
        path = Path(args.path)
        if path.is_file():
            success = tm.sync_document(path, args.force)
            print(f"✅ Document synced successfully" if success else f"❌ Failed to sync document")
        elif path.is_dir():
            results = tm.sync_directory(path, args.pattern, args.force)
            successful = sum(1 for success in results.values() if success)
            print(f"✅ Synced {successful}/{len(results)} documents")
        else:
            print(f"❌ Path does not exist: {path}")

    elif args.command == 'search':
        results = tm.search_documents(args.query)
        if results:
            print(f"\n🔍 Found {len(results)} results for '{args.query}':")
            for result in results:
                print(f"\n📄 {result['title']}")
                print(f"   📍 {result['path']}")
                print(f"   📅 {result['last_updated']}")
                print(f"   💡 {result['snippet']}")
        else:
            print(f"No results found for '{args.query}'")

    elif args.command == 'analytics':
        analytics = tm.get_tag_analytics()
        print(f"\n📊 Tag Analytics:")
        print(f"   Total Tags: {analytics.get('total_tags', 0)}")
        print(f"   Total Documents: {analytics.get('total_documents', 0)}")

        if analytics.get('category_distribution'):
            print(f"\n📂 Categories:")
            for cat in analytics['category_distribution']:
                print(f"   • {cat['category']}: {cat['count']} tags")

        if analytics.get('top_tags'):
            print(f"\n🏆 Top Tags:")
            for tag in analytics['top_tags']:
                print(f"   • {tag['name']}: {tag['count']} uses")

    elif args.command == 'export':
        tm.export_tags(args.output_file)

    elif args.command == 'import':
        tm.import_tags(args.input_file)

if __name__ == '__main__':
    main()