# Tag Management System

A lightweight SQLite-based tag management system with document synchronization, full-text search, and indexing capabilities.

## 🚀 Quick Start

### 1. Initialize the System
```bash
python setup_tags.py
```
This will:
- Create the SQLite database (`tags.db`)
- Add default RL-related tags
- Sync all markdown documents from `efficient_RL_systems/summaries/`
- Extract bracketed tags from document content

### 2. Interactive CLI
```bash
python tag_cli.py
```
Launch the interactive menu-based interface for managing tags.

### 3. Command-Line Interface
```bash
# List all tags
python tag_manager.py list-tags

# Add a new tag
python tag_manager.py add-tag "NewTag" "Category" --desc "Description"

# Search documents
python tag_manager.py search "asynchronous"

# Show analytics
python tag_manager.py analytics

# Sync directory
python tag_manager.py sync ./efficient_RL_systems/summaries
```

## 📚 Features

### ✅ Core Operations
- **Add/Edit/Delete** tags with categories and descriptions
- **Auto-sync** documents extracting bracketed tags `[Tag_Name]`
- **Full-text search** across document content and tags
- **Tag analytics** with usage statistics
- **Import/Export** tags in JSON format

### 🏷️ Tag Categories
Pre-configured categories for RL systems:
- **Hardware_Topics**: GPU-side, CPU-side, Networking, System/_Runtime
- **RL_Training_phases**: Inference, Training, Weight_Synchrony, Experience_Buffer/_Replay
- **Scenarios**: Math/_Coding, Alignment, Multi-agents, GUI-agent

### 🔍 Search Capabilities
- Full-text search across documents
- Tag-based document filtering
- Ranked search results with snippets
- Category-based tag organization

### 📊 Analytics & Insights
- Tag usage frequency tracking
- Category distribution analysis
- Document synchronization status
- Top-performing tags identification

## 📖 Usage Examples

### Document Tag Format
Documents should use bracketed tags in markdown:
```markdown
# Title [Hardware_Topics][GPU-side]

## Section [Training][System_/_Runtime]

Content with technical details...

**External Resources:**
- [GPU Tech]: [CUDA Documentation](https://docs.nvidia.com/cuda/)
```

### Common Operations

#### Add Custom Tag
```bash
python tag_manager.py add-tag "Custom_Optimization" "Hardware_Topics" --desc "Custom GPU optimization technique"
```

#### Search by Technology
```bash
python tag_manager.py search "RDMA"
python tag_manager.py search "asynchronous"
python tag_manager.py search "MoE"
```

#### Show Documents by Tag
```python
from tag_manager import TagManager

tm = TagManager()
docs = tm.get_documents_by_tag("GPU-side")
for doc in docs:
    print(f"📄 {doc['title']}")
    print(f"   📍 {doc['path']}")
```

#### Sync New Documents
```bash
python tag_manager.py sync ./new_documents --pattern "*.md" --force
```

### Interactive Mode
Launch the interactive CLI for guided operations:
```bash
python tag_cli.py
```

Menu options include:
- 📋 List all tags
- ➕ Add new tag
- ✏️ Edit existing tag
- 🗑️ Delete tag
- 📁 Sync directory
- 🔍 Search documents
- 📊 Show analytics
- 📥📤 Export/Import tags

## 🔧 Technical Details

### Database Schema
- **tags**: Tag definitions with categories and usage counts
- **documents**: Document metadata and content hashes
- **document_tags**: Many-to-many relationship between documents and tags
- **document_search**: Full-text search index (SQLite FTS5)

### Performance Features
- **SQLite indexes** for fast tag lookups
- **FTS5 full-text search** with ranking
- **Content hash tracking** for efficient sync
- **Batch operations** for bulk processing

### Tag Extraction
Automatically extracts tags from:
- Bracketed format: `[Tag_Name]`
- Header tags: `# Title [Tag1][Tag2]`
- Section tags: `## Section [Tag3]`
- Any location in document content

## 📁 File Structure
```
material_collection/
├── tags.db                    # SQLite database
├── tag_manager.py            # Core API and CLI
├── tag_cli.py               # Interactive interface
├── setup_tags.py            # Quick setup script
├── README_Tags.md           # This documentation
└── efficient_RL_systems/
    └── summaries/
        ├── *.md             # Documents with bracketed tags
        └── images/          # Associated images
```

## 🔄 Integration with Existing Workflow

### Automatic Sync
The system automatically:
- Detects content changes via file hashing
- Updates tag relationships when documents change
- Maintains search indexes for fast queries
- Tracks tag usage statistics

### API Integration
```python
from tag_manager import TagManager

# Initialize
tm = TagManager("custom_tags.db")

# Sync documents
results = tm.sync_directory("./docs", "*.md")

# Search and filter
docs = tm.get_documents_by_tag("GPU-side")
results = tm.search_documents("performance optimization")

# Analytics
analytics = tm.get_tag_analytics()
print(f"Most used tag: {analytics['top_tags'][0]['name']}")
```

### Batch Operations
```bash
# Sync multiple directories
python tag_manager.py sync ./docs1
python tag_manager.py sync ./docs2 --pattern "*.rst"

# Export for backup
python tag_manager.py export tags_backup.json

# Import tags
python tag_manager.py import tags_backup.json
```

## 🛠️ Maintenance

### Backup Database
```bash
cp tags.db tags_backup.db
```

### Clear and Reset
```python
python tag_cli.py
# Option 12: Database settings
# Option 1: Clear all data
```

### Rebuild Indexes
The system automatically maintains search indexes. No manual rebuild needed.

## 📝 Advanced Usage

### Custom Tag Categories
Add new categories during tag creation:
```bash
python tag_manager.py add-tag "NewTechnique" "NewCategory" --desc "Description"
```

### Integration with Other Tools
The system outputs structured data that can be easily integrated with:
- Documentation generators
- Static site builders
- Knowledge management systems
- API endpoints

### Performance Optimization
- Use specific search queries rather than broad terms
- Sync directories periodically rather than continuously
- Export/import for large-scale tag management
- Use category filtering for faster tag listing

---

**Current Status**: ✅ Fully operational with 445+ tags and 40+ synchronized RL documents.