#!/usr/bin/env python3
"""
Interactive Tag Management CLI

A user-friendly command-line interface for managing tags and synchronizing documents.
"""

from tag_manager import TagManager
from pathlib import Path
import sys
import os

class TagCLI:
    """Interactive CLI for tag management"""

    def __init__(self, db_path: str = "tags.db"):
        self.tm = TagManager(db_path)
        self.db_path = db_path

    def show_menu(self):
        """Display main menu"""
        print("\n🏷️  Tag Management System")
        print("=" * 40)
        print("1. 📋 List all tags")
        print("2. ➕ Add new tag")
        print("3. ✏️  Edit existing tag")
        print("4. 🗑️  Delete tag")
        print("5. 📁 Sync directory")
        print("6. 📄 Sync single document")
        print("7. 🔍 Search documents")
        print("8. 📊 Show analytics")
        print("9. 📥 Export tags")
        print("10. 📤 Import tags")
        print("11. 🏷️  Show documents by tag")
        print("12. ⚙️  Database settings")
        print("0. 🚪 Exit")
        print("=" * 40)

    def list_tags_interactive(self):
        """Interactive tag listing"""
        print("\n📋 Tag Listing Options:")
        print("1. All tags")
        print("2. Filter by category")
        print("3. Sort by usage count")

        choice = input("Select option (1-3): ").strip()

        category = None
        sort_by = "name"

        if choice == "2":
            categories = self.tm.get_tag_categories()
            if categories:
                print("\nAvailable categories:")
                for i, cat in enumerate(categories, 1):
                    print(f"{i}. {cat}")
                cat_choice = input(f"Select category (1-{len(categories)}): ").strip()
                try:
                    idx = int(cat_choice) - 1
                    if 0 <= idx < len(categories):
                        category = categories[idx]
                except ValueError:
                    print("Invalid selection")
                    return
            else:
                print("No categories found")
                return
        elif choice == "3":
            sort_by = "usage_count"

        tags = self.tm.list_tags(category, sort_by)

        if tags:
            print(f"\n🏷️  Found {len(tags)} tags:")
            for i, tag in enumerate(tags, 1):
                print(f"{i:2d}. [{tag.category}] {tag.name}")
                print(f"     📊 Used {tag.usage_count} times")
                if tag.description:
                    print(f"     📝 {tag.description}")
                print()
        else:
            print("No tags found")

    def add_tag_interactive(self):
        """Interactive tag addition"""
        print("\n➕ Add New Tag")
        name = input("Tag name: ").strip()
        if not name:
            print("❌ Tag name cannot be empty")
            return

        categories = self.tm.get_tag_categories()
        print("\nExisting categories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        print("0. New category")

        try:
            cat_choice = input("Select category (number or new name): ").strip()
            if cat_choice == "0" or not cat_choice.isdigit():
                category = cat_choice if cat_choice else input("Enter new category: ").strip()
            else:
                idx = int(cat_choice) - 1
                if 0 <= idx < len(categories):
                    category = categories[idx]
                else:
                    print("Invalid selection")
                    return
        except ValueError:
            category = cat_choice

        description = input("Description (optional): ").strip()

        success = self.tm.add_tag(name, category, description)
        if success:
            print(f"✅ Tag '{name}' added successfully")
        else:
            print(f"❌ Failed to add tag")

    def edit_tag_interactive(self):
        """Interactive tag editing"""
        tags = self.tm.list_tags()
        if not tags:
            print("No tags available to edit")
            return

        print("\n✏️  Edit Tag")
        print("Available tags:")
        for i, tag in enumerate(tags, 1):
            print(f"{i:2d}. [{tag.category}] {tag.name}")

        try:
            choice = int(input(f"Select tag to edit (1-{len(tags)}): ").strip()) - 1
            if not (0 <= choice < len(tags)):
                print("Invalid selection")
                return
        except ValueError:
            print("Invalid selection")
            return

        tag = tags[choice]
        print(f"\nEditing: [{tag.category}] {tag.name}")
        print("Leave blank to keep current value")

        new_name = input(f"New name [{tag.name}]: ").strip() or None
        new_category = input(f"New category [{tag.category}]: ").strip() or None
        new_description = input(f"New description [{tag.description}]: ").strip() or None

        success = self.tm.edit_tag(tag.name, new_name, new_category, new_description)
        if success:
            print(f"✅ Tag updated successfully")
        else:
            print(f"❌ Failed to update tag")

    def delete_tag_interactive(self):
        """Interactive tag deletion"""
        tags = self.tm.list_tags()
        if not tags:
            print("No tags available to delete")
            return

        print("\n🗑️  Delete Tag")
        print("Available tags:")
        for i, tag in enumerate(tags, 1):
            print(f"{i:2d}. [{tag.category}] {tag.name} (used {tag.usage_count} times)")

        try:
            choice = int(input(f"Select tag to delete (1-{len(tags)}): ").strip()) - 1
            if not (0 <= choice < len(tags)):
                print("Invalid selection")
                return
        except ValueError:
            print("Invalid selection")
            return

        tag = tags[choice]
        confirm = input(f"\n⚠️  Delete tag '{tag.name}'? This will remove it from all documents. (y/N): ").strip().lower()

        if confirm == 'y':
            success = self.tm.delete_tag(tag.name)
            if success:
                print(f"✅ Tag '{tag.name}' deleted successfully")
            else:
                print(f"❌ Failed to delete tag")
        else:
            print("Operation cancelled")

    def sync_directory_interactive(self):
        """Interactive directory synchronization"""
        default_path = "./efficient_RL_systems/summaries"
        path = input(f"Directory path [{default_path}]: ").strip() or default_path
        pattern = input("File pattern [*.md]: ").strip() or "*.md"
        force = input("Force update all files? (y/N): ").strip().lower() == 'y'

        if not Path(path).exists():
            print(f"❌ Directory does not exist: {path}")
            return

        print(f"\n📁 Syncing directory: {path}")
        print(f"📄 Pattern: {pattern}")
        print(f"🔄 Force update: {force}")

        results = self.tm.sync_directory(path, pattern, force)
        successful = sum(1 for success in results.values() if success)

        print(f"\n✅ Synced {successful}/{len(results)} documents")
        if successful < len(results):
            failed = len(results) - successful
            print(f"❌ {failed} documents failed to sync")

    def search_interactive(self):
        """Interactive document search"""
        query = input("🔍 Enter search query: ").strip()
        if not query:
            print("❌ Search query cannot be empty")
            return

        results = self.tm.search_documents(query)

        if results:
            print(f"\n🔍 Found {len(results)} results for '{query}':")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. 📄 {result['title']}")
                print(f"   📍 {result['path']}")
                print(f"   📅 {result['last_updated']}")
                print(f"   💡 {result['snippet']}")
        else:
            print(f"No results found for '{query}'")

    def show_documents_by_tag_interactive(self):
        """Show documents for a specific tag"""
        tags = self.tm.list_tags()
        if not tags:
            print("No tags available")
            return

        print("\n🏷️  Select Tag:")
        for i, tag in enumerate(tags, 1):
            print(f"{i:2d}. {tag.name} ({tag.usage_count} documents)")

        try:
            choice = int(input(f"Select tag (1-{len(tags)}): ").strip()) - 1
            if not (0 <= choice < len(tags)):
                print("Invalid selection")
                return
        except ValueError:
            print("Invalid selection")
            return

        tag = tags[choice]
        documents = self.tm.get_documents_by_tag(tag.name)

        if documents:
            print(f"\n📄 Documents with tag '{tag.name}' ({len(documents)}):")
            for doc in documents:
                print(f"   • {doc['title']}")
                print(f"     📍 {doc['path']}")
                print(f"     📅 {doc['last_updated']}")
        else:
            print(f"No documents found with tag '{tag.name}'")

    def export_import_interactive(self):
        """Interactive export/import operations"""
        print("\n📥📤 Export/Import Options:")
        print("1. 📥 Export tags to JSON")
        print("2. 📤 Import tags from JSON")

        choice = input("Select option (1-2): ").strip()

        if choice == "1":
            default_file = "tags_export.json"
            filename = input(f"Output file [{default_file}]: ").strip() or default_file
            self.tm.export_tags(filename)
        elif choice == "2":
            filename = input("Input JSON file: ").strip()
            if Path(filename).exists():
                self.tm.import_tags(filename)
            else:
                print(f"❌ File does not exist: {filename}")

    def database_settings(self):
        """Database settings and information"""
        print(f"\n⚙️  Database Settings")
        print(f"📍 Database file: {self.db_path}")

        db_path = Path(self.db_path)
        if db_path.exists():
            size_mb = db_path.stat().st_size / (1024 * 1024)
            print(f"📊 Database size: {size_mb:.2f} MB")
        else:
            print("📊 Database not created yet")

        print("\nOptions:")
        print("1. 🗑️  Clear all data (recreate database)")
        print("2. 📋 Show database info")
        print("0. 🔙 Back to main menu")

        choice = input("Select option (0-2): ").strip()

        if choice == "1":
            confirm = input("⚠️  This will delete all tags and documents. Type 'DELETE' to confirm: ").strip()
            if confirm == "DELETE":
                db_path.unlink(missing_ok=True)
                self.tm = TagManager(self.db_path)  # Recreate database
                print("✅ Database cleared and recreated")
            else:
                print("Operation cancelled")
        elif choice == "2":
            analytics = self.tm.get_tag_analytics()
            print(f"\n📊 Database Information:")
            print(f"   Total Tags: {analytics.get('total_tags', 0)}")
            print(f"   Total Documents: {analytics.get('total_documents', 0)}")

    def run(self):
        """Main CLI loop"""
        while True:
            try:
                self.show_menu()
                choice = input("Select option (0-12): ").strip()

                if choice == "0":
                    print("👋 Goodbye!")
                    break
                elif choice == "1":
                    self.list_tags_interactive()
                elif choice == "2":
                    self.add_tag_interactive()
                elif choice == "3":
                    self.edit_tag_interactive()
                elif choice == "4":
                    self.delete_tag_interactive()
                elif choice == "5":
                    self.sync_directory_interactive()
                elif choice == "6":
                    path = input("📄 Document path: ").strip()
                    if path and Path(path).exists():
                        success = self.tm.sync_document(Path(path))
                        print(f"✅ Document synced successfully" if success else f"❌ Failed to sync document")
                    else:
                        print("❌ Invalid file path")
                elif choice == "7":
                    self.search_interactive()
                elif choice == "8":
                    analytics = self.tm.get_tag_analytics()
                    print(f"\n📊 Tag Analytics:")
                    print(f"   Total Tags: {analytics.get('total_tags', 0)}")
                    print(f"   Total Documents: {analytics.get('total_documents', 0)}")

                    if analytics.get('category_distribution'):
                        print(f"\n📂 Categories:")
                        for cat in analytics['category_distribution']:
                            print(f"   • {cat['category']}: {cat['count']} tags")

                    if analytics.get('top_tags'):
                        print(f"\n🏆 Top 5 Tags:")
                        for tag in analytics['top_tags'][:5]:
                            print(f"   • {tag['name']}: {tag['count']} uses")
                elif choice == "9":
                    self.export_import_interactive()
                elif choice == "10":
                    self.export_import_interactive()
                elif choice == "11":
                    self.show_documents_by_tag_interactive()
                elif choice == "12":
                    self.database_settings()
                else:
                    print("❌ Invalid option")

                input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("\nPress Enter to continue...")

def main():
    """Entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Interactive Tag Management CLI")
    parser.add_argument('--db', default='tags.db', help='Database file path')
    parser.add_argument('--sync', help='Auto-sync directory and exit')
    parser.add_argument('--pattern', default='*.md', help='File pattern for sync')

    args = parser.parse_args()

    if args.sync:
        # Auto-sync mode
        tm = TagManager(args.db)
        print(f"📁 Auto-syncing: {args.sync}")
        results = tm.sync_directory(args.sync, args.pattern)
        successful = sum(1 for success in results.values() if success)
        print(f"✅ Synced {successful}/{len(results)} documents")
        return

    # Interactive mode
    cli = TagCLI(args.db)
    cli.run()

if __name__ == '__main__':
    main()