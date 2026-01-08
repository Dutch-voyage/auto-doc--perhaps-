# Step 3: PR Search & Filtering - Detailed Guide

## Purpose
Systematically search for and prioritize relevant Pull Requests using keyword taxonomy.

---

## Search Query Construction

### Basic Structure

```
is:pr is:merged repo:[org]/[repo] [keyword]
```

### With Time Filter

```
is:pr is:merged repo:[org]/[repo] [keyword] merged:>=2024-07-01
```

### With Labels

```
is:pr is:merged repo:[org]/[repo] label:enhancement
is:pr is:merged repo:[org]/[repo] label:feature
is:pr is:merged repo:[org]/[repo] label:breaking-change
```

---

## Keyword-Based Searches

### Using `global_keywords.md`

For each assigned keyword, construct queries:

**Example - slime with "training-backend"**:
```
is:pr is:merged repo:THUDM/slime FSDP
is:pr is:merged repo:THUDM/slime Megatron
is:pr is:merged repo:THUDM/slime backend
```

**Example - slime with "performance"**:
```
is:pr is:merged repo:THUDM/slime FP8
is:pr is:merged repo:THUDM/slime optimization
is:pr is:merged repo:THUDM/slime speedup
```

---

## GitHub Search Operators

### Common Operators

| Operator | Purpose | Example |
|----------|---------|---------|
| `is:pr` | Pull requests only | `is:pr repo:org/repo` |
| `is:merged` | Merged PRs only | `is:merged is:pr` |
| `is:open` | Open PRs only | `is:open is:pr` |
| `repo:` | Specific repository | `repo:THUDM/slime` |
| `label:` | Specific label | `label:enhancement` |
| `author:` | Specific author | `author:username` |
| `merged:` | Merge date filter | `merged:>=2024-01-01` |
| `created:` | Creation date filter | `created:>=2024-01-01` |

### Combining Operators

```
is:pr is:merged repo:THUDM/slime label:feature merged:>=2024-01-01
```

---

## Priority Assignment

### High Priority
- Implements roadmap items
- Major feature additions
- Breaking changes
- Architectural improvements

### Medium Priority
- Bug fixes for critical features
- Performance improvements
- Documentation for major features
- Configuration changes

### Low Priority
- Minor bug fixes
- Typo corrections
- Comment improvements
- Test updates

---

## Roadmap Alignment

### Check PR Titles
Look for roadmap keywords:
- Version numbers (e.g., "v0.2.0")
- Feature names from roadmap
- Release milestone links

### Check PR Descriptions
- Mention of roadmap features
- Links to roadmap issues
- Milestone assignments

### Mark in PR List
Add `✓` column for roadmap alignment:
```markdown
| PR # | Title | Priority | Roadmap |
|------|-------|----------|---------|
| 501  | VLM training | High | ✓ |
| 502  | Bug fix | Low | |
```

---

## Timeframe Recommendations

| Repository Type | Recommended Window |
|-----------------|-------------------|
| Active (daily commits) | 3 months |
| Moderate (weekly commits) | 6 months |
| Slow (monthly commits) | 12 months |
| New/Experimental | All time |

---

## Search Strategy

### 1. Broad Search First
```
is:pr is:merged repo:[org]/[repo] merged:>=2024-07-01
```
Purpose: Get overview of all merged PRs

### 2. Label-Based Search
```
is:pr is:merged repo:[org]/[repo] label:enhancement label:feature
```
Purpose: Find feature additions

### 3. Keyword Search
```
is:pr is:merged repo:[org]/[repo] [keyword1] [keyword2]
```
Purpose: Find specific feature areas

### 4. Release-Based Search
```
is:pr is:merged repo:[org]/[repo] milestone:v0.2.0
```
Purpose: Find PRs in specific releases

---

## Collection Template

### File: `raw/[repo]/pr_list.md`

```markdown
# PR List: [Repository Name]

**Timeframe**: [date range]
**Total PRs**: [count]
**Keywords**: [from Step 2]

## High Priority

| PR # | Title | Keywords | Roadmap | Link |
|------|-------|----------|---------|------|
| 501 | VLM training | training-backend,vlm | ✓ | [link] |

## Medium Priority

[Same format]

## Low Priority

[Same format]

## Roadmap Alignment

- Implemented: [count] PRs
- In Progress: [count] PRs
- Not Started: [count] items
```

---

## Tools & Automation

### GitHub CLI
```bash
gh pr list --repo [org]/[repo] --state merged --limit 100 --search "merged:>=2024-01-01"
gh pr list --repo [org]/[repo] --label enhancement --state merged
```

### GitHub API
```python
import requests

url = "https://api.github.com/repos/{org}/{repo}/pulls?state=closed&per_page=100"
params = {
    "since": "2024-01-01",
    "labels": "enhancement"
}
response = requests.get(url, params=params)
```

### Python Script Template
```python
from datetime import datetime, timedelta

# Calculate date range
end_date = datetime.now()
start_date = end_date - timedelta(days=180)

# Construct query
query = f"repo:THUDM/slime is:pr is:merged merged:>={start_date.strftime('%Y-%m-%d')}"

# Use GitHub API to fetch
```

---

## Common Patterns

### Feature PRs
- Title: "feat:", "add:", "implement:"
- Labels: `enhancement`, `feature`
- Size: Large (many files changed)

### Bug Fix PRs
- Title: "fix:", "bugfix:"
- Labels: `bug`, `fix`
- Size: Small (few files changed)

### Breaking Changes
- Title: "BREAKING:", "major:"
- Labels: `breaking-change`
- Description: Mentions API changes

### Documentation
- Title: "docs:", "update docs:"
- Labels: `documentation`
- Files: Only `.md` files

---

## Quality Checks

Before proceeding to Step 4:

- [ ] All keywords searched
- [ ] Timeframe appropriate for repo activity
- [ ] High-priority PRs identified
- [ ] Roadmap alignment marked
- [ ] No obvious gaps in search results
- [ ] PR numbers and links verified

---

## Troubleshooting

### Too Many Results
- Narrow timeframe
- Use more specific keywords
- Filter by labels first
- Focus on high-priority only

### Too Few Results
- Expand timeframe
- Try related keywords
- Check for different label names
- Include open PRs if relevant

### Missing Known Features
- Search by author (known contributors)
- Search by milestone (release versions)
- Try alternative terminology
- Check if in different repo

---

## Next Steps

After PR search and filtering:
1. Proceed to **Step 4**: Raw PR collection
2. Export diffs for high/medium priority PRs
3. Capture metadata for all PRs
4. Index for easy reference

---

**Return to**: `task/Workflow.md` → Step 3
