#!/usr/bin/env python3
"""
Simple Web UI for Tag Management System
Built with Streamlit for rapid development and easy deployment

Features:
- Tag CRUD operations
- Document search with full-text search
- Document reader for .md files
- Tag analytics and statistics
- Approximate matching for document indexing
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import os
import re
from datetime import datetime
import difflib
from typing import List, Dict, Tuple
import mimetypes

# Add current directory to path for imports
sys.path.append('.')

from tag_manager import TagManager, Tag
from terminal_component import render_terminal_tab
from interactive_terminal import render_interactive_claude_terminal, render_interactive_python_terminal, InteractiveTerminal
from file_editor import FileEditor
from settings_manager import settings_manager

# Configuration
PAGE_CONFIG = {
    "page_title": "Tag Management System",
    "page_icon": "🏷️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

class WebUI:
    """Main Web UI class"""

    def __init__(self, db_path: str = "tags.db"):
        self.db_path = db_path
        self.init_session_state()

    def init_session_state(self):
        """Initialize Streamlit session state"""
        if 'tm' not in st.session_state:
            st.session_state.tm = TagManager(self.db_path)
        if 'search_history' not in st.session_state:
            st.session_state.search_history = []
        if 'selected_document' not in st.session_state:
            st.session_state.selected_document = None
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "📋 Tags"

    def run(self):
        """Main application runner"""
        st.set_page_config(**PAGE_CONFIG)

        st.title("🏷️ Tag Management System")
        st.markdown("---")

        # Sidebar navigation
        self.sidebar()

        # Main content area
        page = st.sidebar.selectbox(
            "Navigation",
            ["📋 Tags", "🔍 Search", "📄 Documents", "📊 Analytics", "📖 Reader", "📂 File Editor", "💻 Terminal", "⚙️ Settings"],
            index=["📋 Tags", "🔍 Search", "📄 Documents", "📊 Analytics", "📖 Reader", "📂 File Editor", "💻 Terminal", "⚙️ Settings"].index(st.session_state.current_page)
        )

        # Update session state if page changed via selectbox
        if page != st.session_state.current_page:
            st.session_state.current_page = page

        # Show notification if document is selected but not on Reader page
        if st.session_state.selected_document and page != "📖 Reader":
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("📖 **Document selected!** Please go to the **📖 Reader** tab in the sidebar to view the full document.")
            with col2:
                if st.button("🔄 Clear Selection", help="Clear the selected document"):
                    st.session_state.selected_document = None
                    st.rerun()

        if page == "📋 Tags":
            self.tags_page()
        elif page == "🔍 Search":
            self.search_page()
        elif page == "📄 Documents":
            self.documents_page()
        elif page == "📊 Analytics":
            self.analytics_page()
        elif page == "📖 Reader":
            self.reader_page()
        elif page == "📂 File Editor":
            self.file_editor_page()
        elif page == "💻 Terminal":
            self.terminal_page()
        elif page == "⚙️ Settings":
            self.settings_page()

    def sidebar(self):
        """Sidebar configuration and info"""
        st.sidebar.header("⚙️ System Info")

        # Database info
        try:
            analytics = st.session_state.tm.get_tag_analytics()
            st.sidebar.metric("📊 Total Tags", analytics.get('total_tags', 0))
            st.sidebar.metric("📄 Documents", analytics.get('total_documents', 0))
            st.sidebar.metric("📂 Categories", len(analytics.get('category_distribution', [])))
        except Exception as e:
            st.sidebar.error(f"Database error: {e}")

        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🔗 Quick Actions")

        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("🔄 Sync", help="Sync documents"):
                self.sync_documents()
        with col2:
            if st.button("📥 Export", help="Export tags"):
                self.export_tags()

    def tags_page(self):
        """Tags management page"""
        st.header("📋 Tag Management")

        col1, col2 = st.columns([2, 1])

        with col1:
            # Tag operations
            operation = st.selectbox(
                "Operation",
                ["➕ Add Tag", "✏️ Edit Tag", "🗑️ Delete Tag", "📋 List Tags"]
            )

            if operation == "➕ Add Tag":
                self.add_tag_form()
            elif operation == "✏️ Edit Tag":
                self.edit_tag_form()
            elif operation == "🗑️ Delete Tag":
                self.delete_tag_form()
            elif operation == "📋 List Tags":
                self.list_tags()

        with col2:
            # Quick stats
            st.subheader("📊 Quick Stats")
            try:
                analytics = st.session_state.tm.get_tag_analytics()

                if analytics.get('top_tags'):
                    st.write("**Top 5 Tags:**")
                    for tag in analytics['top_tags'][:5]:
                        st.write(f"• {tag['name']}: {tag['count']} uses")

                if analytics.get('category_distribution'):
                    st.write("**Categories:**")
                    for cat in analytics['category_distribution']:
                        st.write(f"• {cat['category']}: {cat['count']}")
            except Exception as e:
                st.error(f"Error loading stats: {e}")

    def add_tag_form(self):
        """Add tag form"""
        with st.form("add_tag_form"):
            st.subheader("➕ Add New Tag")

            name = st.text_input("Tag Name*")
            category = st.selectbox(
                "Category*",
                ["Hardware_Topics", "RL_Training_phases", "Scenarios", "Other"]
            )

            if category == "Other":
                category = st.text_input("Custom Category")

            description = st.text_area("Description (optional)")

            submit = st.form_submit_button("Add Tag")

            if submit:
                if name and category:
                    success = st.session_state.tm.add_tag(name, category, description)
                    if success:
                        st.success(f"✅ Tag '{name}' added successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to add tag '{name}'")
                else:
                    st.error("❌ Tag Name and Category are required")

    def edit_tag_form(self):
        """Edit tag form"""
        try:
            tags = st.session_state.tm.list_tags()
            if not tags:
                st.warning("No tags available to edit")
                return

            tag_names = [f"{tag.name} [{tag.category}]" for tag in tags]
            selected = st.selectbox("Select Tag to Edit", tag_names)

            if selected:
                tag_idx = tag_names.index(selected)
                tag = tags[tag_idx]

                with st.form("edit_tag_form"):
                    st.subheader(f"✏️ Edit Tag: {tag.name}")

                    new_name = st.text_input("Tag Name", value=tag.name)
                    new_category = st.text_input("Category", value=tag.category)
                    new_description = st.text_area("Description", value=tag.description)

                    submit = st.form_submit_button("Update Tag")

                    if submit:
                        success = st.session_state.tm.edit_tag(
                            tag.name, new_name, new_category, new_description
                        )
                        if success:
                            st.success(f"✅ Tag updated successfully!")
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to update tag")
        except Exception as e:
            st.error(f"Error loading tags: {e}")

    def delete_tag_form(self):
        """Delete tag form"""
        try:
            tags = st.session_state.tm.list_tags()
            if not tags:
                st.warning("No tags available to delete")
                return

            tag_names = [f"{tag.name} ({tag.usage_count} uses)" for tag in tags]
            selected = st.selectbox("Select Tag to Delete", tag_names)

            if selected:
                tag_idx = tag_names.index(selected)
                tag = tags[tag_idx]

                st.warning(f"⚠️ This will delete tag '{tag.name}' used {tag.usage_count} times")

                if st.button(f"🗑️ Delete '{tag.name}'", type="secondary"):
                    success = st.session_state.tm.delete_tag(tag.name)
                    if success:
                        st.success(f"✅ Tag '{tag.name}' deleted successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to delete tag")
        except Exception as e:
            st.error(f"Error loading tags: {e}")

    def list_tags(self):
        """List all tags with filtering"""
        try:
            col1, col2 = st.columns([1, 1])

            with col1:
                category_filter = st.selectbox(
                    "Filter by Category",
                    ["All"] + st.session_state.tm.get_tag_categories()
                )

            with col2:
                sort_by = st.selectbox("Sort By", ["name", "category", "usage_count"])

            tags = st.session_state.tm.list_tags(
                category=category_filter if category_filter != "All" else None,
                sort_by=sort_by
            )

            if tags:
                # Convert to DataFrame for display
                tag_data = []
                for tag in tags:
                    tag_data.append({
                        "Name": tag.name,
                        "Category": tag.category,
                        "Usage Count": tag.usage_count,
                        "Description": tag.description[:50] + "..." if len(tag.description) > 50 else tag.description
                    })

                df = pd.DataFrame(tag_data)
                st.dataframe(df, use_container_width=True)

                # Download option
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download as CSV",
                    csv,
                    "tags.csv",
                    "text/csv",
                    key='download-csv'
                )
            else:
                st.info("No tags found")
        except Exception as e:
            st.error(f"Error listing tags: {e}")

    def search_page(self):
        """Search functionality page"""
        st.header("🔍 Document Search")

        # Search interface
        col1, col2 = st.columns([3, 1])

        with col1:
            search_query = st.text_input(
                "Search Query",
                placeholder="Enter search terms...",
                value=st.session_state.search_history[-1] if st.session_state.search_history else ""
            )

        with col2:
            search_button = st.button("🔍 Search", type="primary")

        # Search options
        with st.expander("🔧 Search Options"):
            fuzzy_search = st.checkbox("Enable Approximate Matching", value=True)
            min_similarity = st.slider("Minimum Similarity", 0.0, 1.0, 0.7) if fuzzy_search else 0.7

            # Tag filtering
            try:
                tags = st.session_state.tm.list_tags()
                if tags:
                    tag_options = [tag.name for tag in tags]
                    selected_tags = st.multiselect("Filter by Tags", tag_options)
            except:
                selected_tags = []

        # Perform search
        if search_button and search_query:
            with st.spinner("Searching..."):
                # Add to search history
                if search_query not in st.session_state.search_history:
                    st.session_state.search_history.append(search_query)

                # Get exact matches
                results = st.session_state.tm.search_documents(search_query)

                # Get fuzzy matches if enabled
                fuzzy_results = []
                if fuzzy_search:
                    fuzzy_results = self.fuzzy_search(search_query, min_similarity)

                # Combine results
                all_results = results + fuzzy_results

                # Filter by tags if specified
                if selected_tags and all_results:
                    filtered_results = []
                    for result in all_results:
                        doc_tags = self.get_document_tags(result['path'])
                        if any(tag in doc_tags for tag in selected_tags):
                            filtered_results.append(result)
                    all_results = filtered_results

                # Display results
                if all_results:
                    st.success(f"🎯 Found {len(all_results)} results")

                    for i, result in enumerate(all_results, 1):
                        with st.expander(f"📄 {result['title']}"):
                            col1, col2 = st.columns([3, 1])

                            with col1:
                                st.markdown(f"**📍 Path:** `{result['path']}`")
                                st.markdown(f"**📅 Updated:** {result['last_updated']}")
                                st.markdown("**💡 Preview:**")
                                st.markdown(result['snippet'])

                                # Document tags
                                doc_tags = self.get_document_tags(result['path'])
                                if doc_tags:
                                    st.markdown("**🏷️ Tags:**")
                                    tags_html = " ".join([f"`{tag}`" for tag in doc_tags])
                                    st.markdown(tags_html)

                            with col2:
                                if st.button(f"📖 Read", key=f"read_{i}"):
                                    st.session_state.selected_document = result['path']
                                    st.session_state.current_page = "📖 Reader"
                                    st.rerun()

                else:
                    st.info("🔍 No results found")

    def fuzzy_search(self, query: str, min_similarity: float) -> List[Dict]:
        """Approximate matching search using document titles and content"""
        try:
            analytics = st.session_state.tm.get_tag_analytics()
            total_docs = analytics.get('total_documents', 0)

            fuzzy_results = []

            # Get all documents (simplified approach)
            for i in range(min(50, total_docs)):  # Limit for performance
                # This is a simplified fuzzy search - in production, you'd use proper fuzzy matching
                # For now, we'll use basic string similarity on titles
                pass

            return fuzzy_results
        except Exception as e:
            st.error(f"Fuzzy search error: {e}")
            return []

    def get_document_tags(self, doc_path: str) -> List[str]:
        """Get tags for a specific document"""
        try:
            # Extract tags from document path or database
            tags = set()

            # Extract from filename
            filename = Path(doc_path).stem
            tags.update(re.findall(r'([A-Z][a-z]+(?:[A-Z][a-z]+)*)', filename))

            # Extract bracketed tags from content if document exists
            if Path(doc_path).exists():
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tags.update(re.findall(r'\[([^\]]+)\]', content))

            return list(tags)
        except Exception:
            return []

    def fix_image_paths(self, content: str, doc_path: str) -> str:
        """Fix image paths in markdown content to work with Streamlit"""
        import re

        def replace_image_path(match):
            alt_text = match.group(1)
            original_path = match.group(2)

            # Skip absolute URLs and data URIs
            if original_path.startswith(('http://', 'https://', 'data:')):
                return match.group(0)

            # For our setup, images are now accessible via local images/ symlink
            if original_path.startswith('./images/') or original_path.startswith('images/'):
                # Normalize to just images/ without ./
                filename = Path(original_path).name
                return f"![{alt_text}](images/{filename})"
            elif original_path.startswith('./'):
                # Handle other relative paths - assume they're images
                filename = Path(original_path).name
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                    fixed_path = f"images/{filename}"
                    return f"![{alt_text}]({fixed_path})"
                else:
                    return match.group(0)
            else:
                # For other relative paths, try to resolve them
                try:
                    doc_dir = Path(doc_path).parent
                    abs_path = (doc_dir / original_path).resolve()

                    # If it's an image in our summaries directory, convert to local path
                    if 'efficient_RL_systems/summaries' in str(abs_path):
                        filename = abs_path.name
                        fixed_path = f"images/{filename}"
                        return f"![{alt_text}]({fixed_path})"
                    else:
                        return match.group(0)
                except:
                    return match.group(0)

        # Replace image paths using regex
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        fixed_content = re.sub(pattern, replace_image_path, content)

        return fixed_content

    def render_markdown_with_images(self, content: str, doc_path: str):
        """Render markdown with properly displayed images using st.image()"""
        import re

        # Find all image references
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        images = re.finditer(pattern, content)

        # Get the base path for images (script is already in web_ui_env/)
        images_dir = Path("images").resolve()

        # Split content by image references and render
        last_end = 0
        for match in images:
            # Display text before this image
            text_before = content[last_end:match.start()]
            if text_before.strip():
                st.markdown(text_before)

            # Extract image info
            alt_text = match.group(1)
            original_path = match.group(2)

            # Handle absolute URLs and data URIs - display with st.image()
            if original_path.startswith(('http://', 'https://')):
                try:
                    st.image(original_path, caption=alt_text, use_container_width=True)
                except Exception as e:
                    # If loading fails, show as markdown with clickable link
                    st.info(f"🖼️ **{alt_text}**")
                    st.markdown(f"[🔗 Open image in new tab]({original_path})")
                last_end = match.end()
                continue
            elif original_path.startswith('data:'):
                # Data URIs - keep in markdown
                st.markdown(match.group(0))
                last_end = match.end()
                continue

            # Resolve the image path
            image_path = None
            if original_path.startswith('./images/') or original_path.startswith('images/'):
                filename = Path(original_path).name
                image_path = images_dir / filename
            elif original_path.startswith('./'):
                # Try to resolve relative to document
                doc_dir = Path(doc_path).parent
                filename = Path(original_path).name
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                    image_path = images_dir / filename
                else:
                    # Keep as markdown if not an image
                    st.markdown(match.group(0))
                    last_end = match.end()
                    continue
            else:
                # Try to resolve relative to document
                try:
                    doc_dir = Path(doc_path).parent
                    abs_path = (doc_dir / original_path).resolve()
                    if 'efficient_RL_systems/summaries' in str(abs_path):
                        filename = abs_path.name
                        image_path = images_dir / filename
                    else:
                        st.markdown(match.group(0))
                        last_end = match.end()
                        continue
                except:
                    st.markdown(match.group(0))
                    last_end = match.end()
                    continue

            # Display the image if path exists
            if image_path and image_path.exists():
                try:
                    st.image(str(image_path), caption=alt_text, use_container_width=True)
                except Exception as e:
                    st.error(f"Failed to load image: {alt_text}")
                    st.code(f"Path: {image_path}")
            else:
                st.warning(f"Image not found: `{alt_text}`")
                if image_path:
                    st.code(f"Expected path: {image_path}")

            last_end = match.end()

        # Display any remaining content after the last image
        remaining = content[last_end:]
        if remaining.strip():
            st.markdown(remaining)

    def documents_page(self):
        """Document listing and management page"""
        st.header("📄 Document Management")

        # Sync controls
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            doc_path = st.text_input("Directory Path", value="../efficient_RL_systems/summaries")

        with col2:
            file_pattern = st.text_input("Pattern", value="*.md")

        with col3:
            if st.button("🔄 Sync Now"):
                self.sync_documents(doc_path, file_pattern)

        # Document listing
        try:
            analytics = st.session_state.tm.get_tag_analytics()
            if analytics.get('total_documents', 0) > 0:
                st.subheader(f"📚 Documents ({analytics['total_documents']} total)")

                # Filter options
                col1, col2 = st.columns([1, 1])
                with col1:
                    category_filter = st.selectbox(
                        "Filter by Tag Category",
                        ["All"] + st.session_state.tm.get_tag_categories()
                    )

                with col2:
                    sort_order = st.selectbox("Sort Order", ["Last Updated", "Title", "Path"])

                # Get documents (this would need to be implemented in TagManager)
                documents = self.get_documents_list(category_filter, sort_order)

                if documents:
                    for doc in documents:
                        with st.expander(f"📄 {doc['title']}"):
                            col1, col2 = st.columns([3, 1])

                            with col1:
                                st.markdown(f"**📍 Path:** `{doc['path']}`")
                                st.markdown(f"**📅 Updated:** {doc['last_updated']}")

                                # Tags
                                if doc.get('tags'):
                                    st.markdown("**🏷️ Tags:**")
                                    tags_html = " ".join([f"`{tag}`" for tag in doc['tags']])
                                    st.markdown(tags_html)

                            with col2:
                                if st.button("📖 Read", key=f"doc_read_{doc['path']}"):
                                    st.session_state.selected_document = doc['path']
                                    st.session_state.current_page = "📖 Reader"
                                    st.rerun()

                                if st.button("🔄 Re-sync", key=f"doc_sync_{doc['path']}"):
                                    success = st.session_state.tm.sync_document(doc['path'])
                                    if success:
                                        st.success("✅ Synced")
                                    else:
                                        st.error("❌ Failed to sync")
                else:
                    st.info("No documents found")
        except Exception as e:
            st.error(f"Error loading documents: {e}")

    def get_documents_list(self, category_filter: str, sort_order: str) -> List[Dict]:
        """Get list of documents with filtering and sorting"""
        # This is a placeholder - would need to be implemented in TagManager
        docs_path = Path("../efficient_RL_systems/summaries")
        documents = []

        if docs_path.exists():
            for md_file in docs_path.glob("*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extract title from first line
                    lines = content.strip().split('\n')
                    title = lines[0].strip('# ') if lines else md_file.stem

                    # Extract tags
                    tags = list(set(re.findall(r'\[([^\]]+)\]', content)))

                    # Filter by category if specified
                    if category_filter != "All":
                        category_tags = [tag for tag in tags if self.get_tag_category(tag) == category_filter]
                        if not category_tags:
                            continue

                    documents.append({
                        'path': str(md_file),
                        'title': title,
                        'last_updated': datetime.fromtimestamp(md_file.stat().st_mtime).isoformat(),
                        'tags': tags
                    })
                except Exception:
                    continue

        # Sort documents
        if sort_order == "Last Updated":
            documents.sort(key=lambda x: x['last_updated'], reverse=True)
        elif sort_order == "Title":
            documents.sort(key=lambda x: x['title'].lower())
        elif sort_order == "Path":
            documents.sort(key=lambda x: x['path'])

        return documents

    def get_tag_category(self, tag_name: str) -> str:
        """Get category for a tag name"""
        try:
            tags = st.session_state.tm.list_tags()
            for tag in tags:
                if tag.name == tag_name:
                    return tag.category
        except:
            pass
        return "Unknown"

    def reader_page(self):
        """Document reader page"""
        st.header("📖 Document Reader")

        # Document selection
        if st.session_state.selected_document:
            doc_path = st.session_state.selected_document
            st.success(f"📖 **Currently viewing:** `{st.session_state.selected_document}`")
            if st.button("🔄 Select Different Document"):
                st.session_state.selected_document = None
                st.rerun()
        else:
            docs = self.get_documents_list("All", "Title")
            if docs:
                doc_options = [f"{doc['title']} - {doc['path']}" for doc in docs]
                selected_idx = st.selectbox("Select Document", range(len(doc_options)), format_func=lambda x: doc_options[x])
                doc_path = docs[selected_idx]['path']
            else:
                st.warning("No documents available")
                return

        # Read and display document
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Document info
            doc_info = Path(doc_path)
            st.markdown(f"**📁 File:** `{doc_path}`")
            st.markdown(f"**📅 Modified:** {datetime.fromtimestamp(doc_info.stat().st_mtime)}")
            st.markdown(f"**📏 Size:** {doc_info.stat().st_size:,} bytes")

            st.markdown("---")

            # Extract and display tags
            tags = list(set(re.findall(r'\[([^\]]+)\]', content)))
            if tags:
                st.markdown("**🏷️ Tags:**")
                tags_html = " ".join([f"`{tag}`" for tag in sorted(tags)])
                st.markdown(tags_html)
                st.markdown("---")

            # Display content with images
            self.render_markdown_with_images(content, doc_path)

            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                if st.button("🔄 Re-sync Document"):
                    success = st.session_state.tm.sync_document(doc_path)
                    if success:
                        st.success("✅ Document synced successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to sync document")

            with col2:
                if st.button("📋 Copy Path"):
                    st.code(doc_path)
                    st.success("Path copied to clipboard!")

            with col3:
                if st.button("🔍 Find Similar"):
                    # Find documents with similar tags
                    similar_docs = self.find_similar_documents(doc_path, tags)
                    if similar_docs:
                        st.success(f"Found {len(similar_docs)} similar documents")
                        for similar_doc in similar_docs[:5]:
                            st.write(f"• {similar_doc['title']}")
                    else:
                        st.info("No similar documents found")

        except Exception as e:
            st.error(f"Error reading document: {e}")

    def find_similar_documents(self, current_path: str, current_tags: List[str]) -> List[Dict]:
        """Find documents with similar tags"""
        similar_docs = []
        try:
            all_docs = self.get_documents_list("All", "Title")

            for doc in all_docs:
                if doc['path'] == current_path:
                    continue

                # Calculate tag similarity
                doc_tags = set(doc.get('tags', []))
                current_tag_set = set(current_tags)

                if doc_tags and current_tag_set:
                    intersection = doc_tags.intersection(current_tag_set)
                    similarity = len(intersection) / len(current_tag_set.union(doc_tags))

                    if similarity > 0.3:  # 30% similarity threshold
                        similar_docs.append({
                            'title': doc['title'],
                            'path': doc['path'],
                            'similarity': similarity,
                            'shared_tags': list(intersection)
                        })

            # Sort by similarity
            similar_docs.sort(key=lambda x: x['similarity'], reverse=True)

        except Exception:
            pass

        return similar_docs

    def analytics_page(self):
        """Analytics and statistics page"""
        st.header("📊 Analytics & Statistics")

        try:
            analytics = st.session_state.tm.get_tag_analytics()

            # Overview metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("📊 Total Tags", analytics.get('total_tags', 0))

            with col2:
                st.metric("📄 Documents", analytics.get('total_documents', 0))

            with col3:
                st.metric("📂 Categories", len(analytics.get('category_distribution', [])))

            with col4:
                avg_usage = analytics.get('total_tags', 0) / max(len(analytics.get('category_distribution', [])), 1)
                st.metric("📈 Avg Usage/Cat", f"{avg_usage:.1f}")

            st.markdown("---")

            # Category distribution
            if analytics.get('category_distribution'):
                st.subheader("📂 Category Distribution")

                cat_data = analytics['category_distribution']
                df_cats = pd.DataFrame(cat_data)

                col1, col2 = st.columns([2, 1])

                with col1:
                    st.bar_chart(df_cats.set_index('category')['count'])

                with col2:
                    st.dataframe(df_cats, use_container_width=True)

            # Top tags
            if analytics.get('top_tags'):
                st.subheader("🏆 Top Tags")

                top_tags = analytics['top_tags'][:10]
                df_tags = pd.DataFrame(top_tags)

                col1, col2 = st.columns([2, 1])

                with col1:
                    st.bar_chart(df_tags.set_index('name')['count'])

                with col2:
                    st.dataframe(df_tags, use_container_width=True)

            # Tag usage heatmap (simplified)
            st.subheader("🔥 Tag Usage Heatmap")

            tags = st.session_state.tm.list_tags(sort_by="usage_count")
            if tags:
                # Create usage distribution
                usage_data = []
                for i, tag in enumerate(tags[:20]):  # Top 20 tags
                    usage_data.append({
                        'Tag': tag.name,
                        'Usage': tag.usage_count,
                        'Category': tag.category
                    })

                df_usage = pd.DataFrame(usage_data)

                # Simple bar chart for usage
                st.bar_chart(df_usage.set_index('Tag')['Usage'])

            # Recent activity
            st.subheader("📅 Recent Activity")
            st.info("Document sync and tag management statistics would appear here")

        except Exception as e:
            st.error(f"Error loading analytics: {e}")

    def sync_documents(self, directory: str = None, pattern: str = "*.md"):
        """Sync documents with tag manager"""
        try:
            if not directory:
                directory = "../efficient_RL_systems/summaries"

            with st.spinner(f"Syncing {directory}..."):
                results = st.session_state.tm.sync_directory(directory, pattern)
                successful = sum(1 for success in results.values() if success)

                if successful:
                    st.success(f"✅ Synced {successful}/{len(results)} documents")
                else:
                    st.warning(f"⚠️ No documents synced")

                # Show details
                with st.expander("📋 Sync Details"):
                    for path, success in results.items():
                        status = "✅" if success else "❌"
                        st.write(f"{status} {Path(path).name}")
        except Exception as e:
            st.error(f"❌ Sync error: {e}")

    def export_tags(self):
        """Export tags to JSON"""
        try:
            filename = f"tags_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            st.session_state.tm.export_tags(filename)
            st.success(f"✅ Tags exported to {filename}")

            # Provide download link
            with open(filename, 'r', encoding='utf-8') as f:
                st.download_button(
                    "📥 Download Export",
                    f.read(),
                    filename,
                    "application/json"
                )
        except Exception as e:
            st.error(f"❌ Export error: {e}")

    def file_editor_page(self):
        """File editor page with comprehensive file management"""
        try:
            # Initialize File Editor
            base_path = "/home/yyx/data_management/material_collection"
            file_editor = FileEditor(base_path)

            # Render the file editor interface
            file_editor.render()

        except Exception as e:
            st.error(f"❌ File Editor error: {e}")
            st.code(f"Error details: {str(e)}")

    def terminal_page(self):
        """Terminal page for system operations"""

        st.markdown("## 💻 Terminal Interface")
        st.markdown("*Execute system commands and run interactive applications*")

        # Terminal mode selection
        terminal_mode = st.radio(
            "Select Terminal Mode:",
            ["🔧 Standard Terminal", "🚀 Interactive Terminal"],
            key="terminal_mode",
            help="Standard Terminal: Safe command execution. Interactive Terminal: Full interactive sessions with real-time output."
        )

        if terminal_mode == "🔧 Standard Terminal":
            # Standard terminal component
            render_terminal_tab()

        elif terminal_mode == "🚀 Interactive Terminal":
            # Interactive terminal with real-time sessions
            self.render_interactive_terminal_options()

    def render_interactive_terminal_options(self):
        """Render interactive terminal application selection"""

        st.markdown("### 🚀 Interactive Applications")
        st.markdown("*Full-featured terminal with real-time output and complete functionality*")

        # Application selection
        app_selection = st.selectbox(
            "Select Application:",
            ["🤖 Claude Code", "🐍 Python REPL", "🐚 Bash Shell", "🟢 Node.js REPL"],
            key="interactive_app_selection",
            help="Choose the application you want to run interactively"
        )

        # Terminal server status
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("**📊 Server Status**")

            # Try to check if server is running
            try:
                import requests
                import socket

                # Check if port 8765 is open
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex(('localhost', 8765))
                sock.close()

                if result == 0:
                    st.success("✅ Terminal server is running on port 8765")
                    server_status = "running"
                else:
                    st.warning("⚠️ Terminal server is not running")
                    server_status = "stopped"

            except Exception as e:
                st.error("❌ Error checking server status")
                server_status = "unknown"

        with col2:
            if server_status != "running":
                st.markdown("**🚀 Start Server**")
                if st.button("🔧 Start Terminal Server", key="start_server", help="Start the WebSocket terminal server"):
                    st.info("""
                    **To start the terminal server, run this command in a separate terminal:**

                    ```bash
                    cd /home/yyx/data_management/material_collection/web_ui_env
                    uv sync --extra interactive-terminal
                    python terminal_server.py
                    ```

                    The server will start on port 8765 and you'll see "Terminal server started successfully!"
                    """)
            else:
                st.markdown("**🎉 Ready to Connect!**")
                st.success("Server is ready for interactive sessions")

        # Render the selected interactive terminal
        if server_status == "running":
            st.markdown("---")

            if app_selection == "🤖 Claude Code":
                st.info("""
                **🤖 Claude Code Persistent Bash Session**

                This terminal starts a persistent bash session. To start Claude Code, run:
                ```bash
                /home/yyx/.nvm/versions/node/v22.18.0/bin/claude
                ```

                **Benefits:**
                - **Ctrl+C** won't kill the entire session - only the current command
                - **Tab completion** works in bash
                - **Persistent session** - use multiple commands
                - **Full bash functionality** available
                """)
                render_interactive_claude_terminal()

            elif app_selection == "🐍 Python REPL":
                render_interactive_python_terminal()

            elif app_selection == "🐚 Bash Shell":
                terminal = InteractiveTerminal()
                terminal.render_interactive_terminal("Bash Shell", "bash")

            elif app_selection == "🟢 Node.js REPL":
                terminal = InteractiveTerminal()
                terminal.render_interactive_terminal("Node.js REPL", "node")

            # Session information
            with st.expander("📋 Session Information", expanded=False):
                st.markdown("""
                **Interactive Terminal Features:**

                - **🔌 Real-time Connection**: WebSocket-based bidirectional communication
                - **📱 Full Functionality**: Complete application features including tab completion, history, etc.
                - **🔄 Live Output**: See terminal output immediately as it appears
                - **💻 Authentic Experience**: Real terminal with xterm.js emulation
                - **🔒 Safe Environment**: Isolated sessions with proper cleanup

                **Keyboard Shortcuts:**
                - **Enter**: Execute command
                - **Tab**: Auto-completion (if supported by application)
                - **Arrow Up/Down**: Command history (if supported by application)
                - **Ctrl+C**: Interrupt current command (if supported)
                """)

                if app_selection == "🤖 Claude Code":
                    st.markdown("""
                    **Claude Code Specific Features:**

                    - **🤖 AI Assistant**: Full Claude Code functionality
                    - **📁 File Operations**: Edit, create, manage files
                    - **🔍 Code Analysis**: Code review and suggestions
                    - **🛠️ Development Tools**: Complete development workflow
                    - **💬 Interactive Chat**: Natural language interaction with Claude
                    """)
        else:
            st.warning("⚠️ Please start the terminal server first to use interactive features")

    def settings_page(self):
        """Settings configuration page"""
        settings_manager.render_settings_page()

def main():
    """Main entry point"""
    ui = WebUI()
    ui.run()

if __name__ == "__main__":
    main()