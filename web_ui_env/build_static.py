#!/usr/bin/env python3
"""
Static Site Builder for Streamlit Web UI
Converts Streamlit app to static HTML for GitHub Pages deployment
"""

import os
import json
import sqlite3
import shutil
from pathlib import Path
from typing import Dict, List, Any
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.codehilite

def extract_database_data() -> Dict[str, Any]:
    """Extract data from SQLite database for static generation"""
    conn = sqlite3.connect('tags.db')
    conn.row_factory = sqlite3.Row

    # Extract tags
    cursor = conn.execute('SELECT * FROM tags')
    tags = [dict(row) for row in cursor.fetchall()]

    # Extract documents
    cursor = conn.execute('SELECT * FROM documents')
    documents = [dict(row) for row in cursor.fetchall()]

    # Extract document tags
    cursor = conn.execute('SELECT * FROM document_tags')
    document_tags = [dict(row) for row in cursor.fetchall()]

    # Extract analytics
    cursor = conn.execute('SELECT COUNT(*) as total_tags FROM tags')
    total_tags = cursor.fetchone()['total_tags']

    cursor = conn.execute('SELECT COUNT(*) as total_documents FROM documents')
    total_documents = cursor.fetchone()['total_documents']

    conn.close()

    return {
        'tags': tags,
        'documents': documents,
        'document_tags': document_tags,
        'analytics': {
            'total_tags': total_tags,
            'total_documents': total_documents
        }
    }

def extract_document_content() -> List[Dict[str, Any]]:
    """Extract content from markdown documents"""
    documents_dir = Path('../efficient_RL_systems/summaries')
    documents = []

    if not documents_dir.exists():
        return documents

    for md_file in documents_dir.glob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Convert markdown to HTML
            html_content = markdown.markdown(
                content,
                extensions=['fenced_code', 'codehilite', 'tables', 'toc']
            )

            documents.append({
                'filename': md_file.name,
                'title': md_file.stem.replace('_', ' ').title(),
                'content': content,
                'html_content': html_content,
                'path': str(md_file)
            })
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
            continue

    return documents

def generate_static_html(db_data: Dict[str, Any], documents: List[Dict[str, Any]]) -> str:
    """Generate static HTML version of the Streamlit app"""

    # Generate tag analytics HTML
    tag_categories = {}
    for tag in db_data['tags']:
        category = tag['category']
        if category not in tag_categories:
            tag_categories[category] = []
        tag_categories[category].append(tag)

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Material Collection System - Web UI</title>
    <style>
        {get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🏷️ Material Collection System</h1>
            <p class="subtitle">Comprehensive RL Materials Management</p>
        </header>

        <nav class="nav-tabs">
            <button class="tab-btn active" onclick="showTab('tags')">📋 Tags</button>
            <button class="tab-btn" onclick="showTab('search')">🔍 Search</button>
            <button class="tab-btn" onclick="showTab('documents')">📄 Documents</button>
            <button class="tab-btn" onclick="showTab('analytics')">📊 Analytics</button>
        </nav>

        <!-- Tags Tab -->
        <div id="tags" class="tab-content active">
            <h2>🏷️ Tag Management</h2>
            <div class="stats">
                <div class="stat-card">
                    <h3>{db_data['analytics']['total_tags']}</h3>
                    <p>Total Tags</p>
                </div>
                <div class="stat-card">
                    <h3>{len(tag_categories)}</h3>
                    <p>Categories</p>
                </div>
                <div class="stat-card">
                    <h3>{db_data['analytics']['total_documents']}</h3>
                    <p>Documents</p>
                </div>
            </div>

            <div class="tag-categories">
                {generate_tag_categories_html(tag_categories)}
            </div>
        </div>

        <!-- Search Tab -->
        <div id="search" class="tab-content">
            <h2>🔍 Search Documents</h2>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Search documents, tags, or content..." onkeyup="performSearch()">
                <button onclick="performSearch()">Search</button>
            </div>
            <div id="searchResults"></div>
        </div>

        <!-- Documents Tab -->
        <div id="documents" class="tab-content">
            <h2>📄 Document Reader</h2>
            <div class="document-list">
                {generate_document_list_html(documents)}
            </div>
        </div>

        <!-- Analytics Tab -->
        <div id="analytics" class="tab-content">
            <h2>📊 System Analytics</h2>
            <div class="analytics-grid">
                <div class="analytics-card">
                    <h3>📈 Collection Growth</h3>
                    <div class="chart-placeholder">
                        <p>{db_data['analytics']['total_documents']} documents processed</p>
                        <p>{db_data['analytics']['total_tags']} tags generated</p>
                    </div>
                </div>
                <div class="analytics-card">
                    <h3>🏷️ Tag Distribution</h3>
                    <div class="tag-cloud">
                        {generate_tag_cloud_html(db_data['tags'])}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        {get_javascript_code(documents, db_data)}
    </script>
</body>
</html>
"""

    return html_content

def get_css_styles() -> str:
    """Return CSS styles for the static site"""
    return """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f8f9fa;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.header {
    text-align: center;
    margin-bottom: 30px;
    padding: 40px 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
}

.header h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 1.2em;
    opacity: 0.9;
}

.nav-tabs {
    display: flex;
    background: white;
    border-radius: 10px;
    padding: 5px;
    margin-bottom: 30px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.tab-btn {
    flex: 1;
    padding: 15px 20px;
    border: none;
    background: transparent;
    font-size: 16px;
    cursor: pointer;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.tab-btn.active, .tab-btn:hover {
    background: #667eea;
    color: white;
}

.tab-content {
    display: none;
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 20px rgba(0,0,0,0.1);
}

.tab-content.active {
    display: block;
}

.stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.stat-card {
    background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
    color: white;
    padding: 30px;
    border-radius: 10px;
    text-align: center;
}

.stat-card h3 {
    font-size: 2.5em;
    margin-bottom: 10px;
}

.tag-categories {
    display: grid;
    gap: 20px;
}

.category-section {
    border: 1px solid #e1e8ed;
    border-radius: 10px;
    overflow: hidden;
}

.category-header {
    background: #f7f9fa;
    padding: 15px 20px;
    border-bottom: 1px solid #e1e8ed;
    font-weight: bold;
    color: #333;
}

.tag-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 10px;
    padding: 20px;
}

.tag-item {
    background: #f1f3f4;
    padding: 10px 15px;
    border-radius: 20px;
    font-size: 14px;
    border: 1px solid #e1e8ed;
}

.search-box {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

.search-box input {
    flex: 1;
    padding: 15px;
    border: 1px solid #e1e8ed;
    border-radius: 8px;
    font-size: 16px;
}

.search-box button {
    padding: 15px 30px;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
}

.document-list {
    display: grid;
    gap: 15px;
}

.document-item {
    border: 1px solid #e1e8ed;
    border-radius: 8px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.document-item:hover {
    border-color: #667eea;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
}

.document-title {
    font-weight: bold;
    color: #333;
    margin-bottom: 5px;
}

.document-filename {
    color: #666;
    font-size: 14px;
}

.analytics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}

.analytics-card {
    border: 1px solid #e1e8ed;
    border-radius: 10px;
    padding: 20px;
}

.analytics-card h3 {
    margin-bottom: 15px;
    color: #333;
}

.chart-placeholder {
    background: #f7f9fa;
    padding: 30px;
    border-radius: 8px;
    text-align: center;
}

.tag-cloud {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.tag-cloud span {
    background: #e1f5fe;
    color: #0277bd;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 14px;
}

.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
}

.modal-content {
    background-color: white;
    margin: 5% auto;
    padding: 30px;
    border-radius: 10px;
    width: 90%;
    max-width: 800px;
    max-height: 80vh;
    overflow-y: auto;
}

.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
}

.close:hover {
    color: black;
}

@media (max-width: 768px) {
    .nav-tabs {
        flex-direction: column;
    }

    .stats {
        grid-template-columns: 1fr;
    }

    .tag-grid {
        grid-template-columns: 1fr;
    }
}
"""

def generate_tag_categories_html(tag_categories: Dict[str, List]) -> str:
    """Generate HTML for tag categories"""
    html = ""
    for category, tags in tag_categories.items():
        html += f"""
        <div class="category-section">
            <div class="category-header">
                📁 {category} ({len(tags)} tags)
            </div>
            <div class="tag-grid">
        """

        for tag in tags[:20]:  # Limit to 20 tags per category
            html += f'<div class="tag-item">#{tag["name"]}</div>'

        if len(tags) > 20:
            html += f'<div class="tag-item">... and {len(tags) - 20} more</div>'

        html += """
            </div>
        </div>
        """
    return html

def generate_document_list_html(documents: List[Dict[str, Any]]) -> str:
    """Generate HTML for document list"""
    html = ""
    for doc in documents:
        html += f"""
        <div class="document-item" onclick="showDocument('{doc['filename']}')">
            <div class="document-title">{doc['title']}</div>
            <div class="document-filename">{doc['filename']}</div>
        </div>
        """
    return html

def generate_tag_cloud_html(tags: List[Dict[str, Any]]) -> str:
    """Generate HTML for tag cloud"""
    html = ""
    tag_counts = {}

    for tag in tags[:50]:  # Top 50 tags
        tag_counts[tag['name']] = tag.get('count', 1)

    for tag_name, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
        html += f'<span>#{tag_name}</span>'

    return html

def get_javascript_code(documents: List[Dict[str, Any]], db_data: Dict[str, Any]) -> str:
    """Return JavaScript code for interactivity"""
    # Convert documents to JSON for JavaScript
    docs_json = json.dumps(documents)
    tags_json = json.dumps(db_data['tags'])

    return f"""
    const documents = {docs_json};
    const tags = {tags_json};

    function showTab(tabName) {{
        // Hide all tabs
        const tabContents = document.querySelectorAll('.tab-content');
        tabContents.forEach(tab => tab.classList.remove('active'));

        // Remove active class from all buttons
        const tabButtons = document.querySelectorAll('.tab-btn');
        tabButtons.forEach(btn => btn.classList.remove('active'));

        // Show selected tab
        document.getElementById(tabName).classList.add('active');
        event.target.classList.add('active');
    }}

    function showDocument(filename) {{
        const doc = documents.find(d => d.filename === filename);
        if (doc) {{
            const modal = document.createElement('div');
            modal.className = 'modal';
            modal.style.display = 'block';
            modal.innerHTML = `
                <div class="modal-content">
                    <span class="close" onclick="this.closest('.modal').remove()">&times;</span>
                    <h2>${{doc.title}}</h2>
                    <hr style="margin: 20px 0;">
                    ${{doc.html_content}}
                </div>
            `;
            document.body.appendChild(modal);
        }}
    }}

    function performSearch() {{
        const query = document.getElementById('searchInput').value.toLowerCase();
        const resultsDiv = document.getElementById('searchResults');

        if (query.length < 2) {{
            resultsDiv.innerHTML = '<p>Please enter at least 2 characters to search.</p>';
            return;
        }}

        const results = [];

        // Search in documents
        documents.forEach(doc => {{
            if (doc.content.toLowerCase().includes(query) ||
                doc.title.toLowerCase().includes(query) ||
                doc.filename.toLowerCase().includes(query)) {{
                results.push({{
                    type: 'document',
                    title: doc.title,
                    filename: doc.filename,
                    snippet: getSnippet(doc.content, query)
                }});
            }}
        }});

        // Search in tags
        tags.forEach(tag => {{
            if (tag.name.toLowerCase().includes(query) ||
                tag.description.toLowerCase().includes(query)) {{
                results.push({{
                    type: 'tag',
                    name: tag.name,
                    category: tag.category,
                    description: tag.description
                }});
            }}
        }});

        displayResults(results);
    }}

    function getSnippet(content, query, length = 150) {{
        const index = content.toLowerCase().indexOf(query.toLowerCase());
        if (index === -1) return content.substring(0, length) + '...';

        const start = Math.max(0, index - 50);
        const end = Math.min(content.length, index + query.length + 50);
        return '...' + content.substring(start, end) + '...';
    }}

    function displayResults(results) {{
        const resultsDiv = document.getElementById('searchResults');

        if (results.length === 0) {{
            resultsDiv.innerHTML = '<p>No results found.</p>';
            return;
        }}

        let html = `<h3>Found ${{results.length}} results:</h3>`;

        results.forEach(result => {{
            if (result.type === 'document') {{
                html += `
                    <div class="document-item" onclick="showDocument('${{result.filename}}')">
                        <div class="document-title">📄 ${{result.title}}</div>
                        <div class="document-filename">${{result.filename}}</div>
                        <div style="margin-top: 10px; color: #666;">${{result.snippet}}</div>
                    </div>
                `;
            }} else if (result.type === 'tag') {{
                html += `
                    <div class="document-item">
                        <div class="document-title">🏷️ #${{result.name}}</div>
                        <div style="color: #666;">Category: ${{result.category}}</div>
                        <div style="margin-top: 10px; color: #666;">${{result.description}}</div>
                    </div>
                `;
            }}
        }});

        resultsDiv.innerHTML = html;
    }}

    // Close modal when clicking outside
    window.onclick = function(event) {{
        const modal = document.querySelector('.modal');
        if (event.target === modal) {{
            modal.remove();
        }}
    }}
"""

def main():
    """Main build function"""
    print("🚀 Building static site...")

    # Create output directory
    output_dir = Path('dist')
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()

    # Extract data
    print("📊 Extracting database data...")
    db_data = extract_database_data()

    print("📄 Extracting document content...")
    documents = extract_document_content()

    # Generate HTML
    print("🏗️ Generating static HTML...")
    html_content = generate_static_html(db_data, documents)

    # Save HTML
    output_file = output_dir / 'index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Static site built successfully!")
    print(f"📁 Output: {output_file.absolute()}")
    print(f"📊 Processed {db_data['analytics']['total_documents']} documents and {db_data['analytics']['total_tags']} tags")

if __name__ == "__main__":
    main()