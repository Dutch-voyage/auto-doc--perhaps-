#!/usr/bin/env python3
"""
Quick setup script for tag management system
"""

from tag_manager import TagManager
import sys

def main():
    """Setup tag management with default categories and sync RL documents"""
    print("🚀 Setting up Tag Management System...")

    # Initialize tag manager
    tm = TagManager("tags.db")

    # Add default categories with sample tags
    default_tags = [
        ("Hardware_Topics", "GPU-side", "GPU-level optimizations and kernel-level performance improvements"),
        ("Hardware_Topics", "CPU-side", "CPU optimizations and multi-threading strategies"),
        ("Hardware_Topics", "Networking", "Network communication and distributed system optimizations"),
        ("Hardware_Topics", "System_/_Runtime", "System-level runtime optimizations and orchestration"),

        ("RL_Training_phases", "Inference", "Model inference and generation phases"),
        ("RL_Training_phases", "Training", "Model training and gradient computation phases"),
        ("RL_Training_phases", "Weight_Synchrony", "Parameter synchronization and gradient aggregation"),
        ("RL_Training_phases", "Experience_Buffer_/_Replay", "Experience replay and buffer management"),

        ("Scenarios", "Math_/_Coding", "Mathematical reasoning and code generation tasks"),
        ("Scenarios", "Alignment", "Model alignment and safety training"),
        ("Scenarios", "Multi-agents", "Multi-agent systems and coordination"),
        ("Scenarios", "GUI-agent", "Graphical user interface automation and interaction")
    ]

    print("📝 Adding default tags...")
    added_count = 0
    for category, name, description in default_tags:
        success = tm.add_tag(name, category, description)
        if success:
            added_count += 1

    print(f"✅ Added {added_count} default tags")

    # Sync RL documents
    rl_docs_path = "./efficient_RL_systems/summaries"
    print(f"📁 Syncing RL documents from {rl_docs_path}...")

    try:
        results = tm.sync_directory(rl_docs_path, "*.md")
        successful = sum(1 for success in results.values() if success)
        print(f"✅ Synced {successful}/{len(results)} documents")
    except Exception as e:
        print(f"❌ Error syncing documents: {e}")

    # Show analytics
    analytics = tm.get_tag_analytics()
    print(f"\n📊 Setup Summary:")
    print(f"   Total Tags: {analytics.get('total_tags', 0)}")
    print(f"   Total Documents: {analytics.get('total_documents', 0)}")
    print(f"   Categories: {len(analytics.get('category_distribution', []))}")

    print(f"\n🎯 Tag Management System is ready!")
    print(f"   Database: tags.db")
    print(f"   CLI: python tag_cli.py")
    print(f"   API: python tag_manager.py --help")

if __name__ == '__main__':
    main()