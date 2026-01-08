# Step 1: Roadmap Discovery - Detailed Guide

## Purpose
Locate and extract roadmap documentation from target repositories to understand future development directions.

---

## Search Strategies

### Primary: GitHub Roadmap Issues

**Query Template**:
```
https://github.com/[org]/[repo]/issues?q=is%3Aissue+state%3Aopen+label%3Aroadmap
```

**Example (slime)**:
```
https://github.com/THUDM/slime/issues?q=is%3Aissue+state%3Aopen+label%3Aroadmap
```

**What to Look For**:
- Official roadmap issues
- Milestone-linked issues
- Project board items
- Future release plans

### Secondary: Documentation Files

**Common Paths**:
- `ROADMAP.md`
- `docs/roadmap.md`
- `docs/future-plans.md`
- `planning/roadmap.md`

**Access via GitHub**:
```
https://raw.githubusercontent.com/[org]/[repo]/main/ROADMAP.md
```

**Access via Web**:
```
https://github.com/[org]/[repo]/blob/main/ROADMAP.md
```

### Tertiary: README Extraction

**Search Keywords in README**:
- "Upcoming"
- "Planned features"
- "Future work"
- "Roadmap"
- "Todo"

**Look For**:
- Explicit roadmap sections
- Version plans
- Known issues tracking
- Enhancement proposals

### Fallback: Issue Labels

**Search Queries**:
```
label:enhancement state:open
label:future state:open
label:planned state:open
```

---

## Extraction Template

### For Each Roadmap Item

```markdown
## [Feature Name]

**Status**: [Planned/In Progress/Implemented]
**Target Version**: [version if specified]
**Source**: [issue/PR/discussion link]
**Description**: [brief description]
**Dependencies**: [other features/PRs]
```

### Example (slime)

```markdown
## VLM + FSDP Integration

**Status**: Implemented (v0.2.1)
**Target Version**: v0.2.1
**Source**: https://github.com/THUDM/slime/pull/501
**Description**: True on-policy training for vision-language models
**Dependencies**: FSDP backend
```

---

## Roadmap Sources Hierarchy

| Priority | Source | Reliability |
|----------|--------|-------------|
| 1 | Official ROADMAP.md file | High |
| 2 | Labeled roadmap issues | High |
| 3 | Documentation roadmap pages | Medium |
| 4 | README future sections | Medium |
| 5 | Enhancement-labeled issues | Low |

---

## Tools & Commands

### GitHub CLI
```bash
gh issue list --label roadmap --repo [org]/[repo]
gh issue list --label enhancement --state open --repo [org]/[repo]
```

### Curl (for raw files)
```bash
curl https://raw.githubusercontent.com/[org]/[repo]/main/ROADMAP.md
```

### Git (for cloning docs)
```bash
git clone --depth 1 --sparse https://github.com/[org]/[repo].git
cd [repo]
git sparse-checkout set ROADMAP.md docs/
```

---

## Output Format

### File: `raw/[repo]/roadmap_summary.md`

```markdown
# [Repository Name] Roadmap

**Last Updated**: [Date]
**Source**: [URL]

## Official Roadmap Items

[Extracted roadmap items]

## Future Enhancements

[From enhancement-labeled issues]

## Notes

[Additional context, version info, etc.]
```

---

## Troubleshooting

### No Roadmap Found
1. Check alternative spellings: "road map", "future", "plans"
2. Search issues for "roadmap" in title/description
3. Look for wiki pages or external documentation
4. Check releases for future version descriptions

### Roadmap Outdated
1. Check recent issues for updated plans
2. Look for blog posts or announcements
3. Review recent merged PRs for implemented features
4. Document both old and new roadmap items

### Conflicting Roadmap Information
1. Prioritize official documents over issues
2. Note conflicts in your summary
3. Check dates of conflicting sources
4. Verify with maintainers if critical

---

## Examples

### slime Repository
- **Roadmap Issues**: https://github.com/THUDM/slime/issues?q=is%3Aissue+state%3Aopen+label%3Aroadmap
- **Primary Source**: Release notes and blog posts
- **Key Indicators**: Version numbers, feature descriptions

### Common Patterns
- Most RL frameworks document roadmaps in releases
- Issues with `enhancement` label often indicate roadmap items
- Project boards may contain roadmap organization
- External documentation sites often have roadmap pages

---

## Best Practices

1. **Always cite sources** with URLs
2. **Include dates** for all roadmap items
3. **Note version targets** when specified
4. **Track dependencies** between features
5. **Update roadmap** if repository changes
6. **Document uncertainty** if roadmap is unclear

---

## Next Steps

After roadmap discovery:
1. Proceed to **Step 2**: Keyword taxonomy assignment
2. Use roadmap to prioritize PR collection
3. Cross-reference PRs with roadmap items
4. Update roadmap if new information found

---

**Return to**: `task/Workflow.md` → Step 1
