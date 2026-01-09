# Directory Structure Update - 2026-01-08

## Summary

Reorganized the `raw/` directory to separate **completed analyses** from **work-in-progress files**.

---

## New Structure

### Before
```
raw/
└── [repo_name]/
    ├── [repo]_analysis.md       # Mixed: final + intermediate
    ├── roadmap_summary.md
    ├── keyword_labels.md
    ├── pr_list.md
    ├── pr_diffs/
    └── assets/
```

### After
```
raw/
├── completed/                   # ✅ Final outputs only
│   └── [repo_name]/
│       ├── [repo]_analysis.md   # Main synthesis (Step 5)
│       └── guidance.md          # Monitoring guide (Step 6)
│
└── [repo_name]/                 # 🚧 Work in progress (intermediate)
    ├── roadmap_summary.md       # Step 1 output
    ├── keyword_labels.md        # Step 2 output
    ├── pr_list.md               # Step 3 output
    ├── pr_diffs/                # Step 4 output
    │   ├── [pr_number].patch
    │   └── pr_index.md
    └── assets/                  # Screenshots, diagrams
```

---

## File Locations

### Final Outputs (Completed)

| File | Location | Step |
|------|----------|------|
| `[repo]_analysis.md` | `raw/completed/[repo]/` | Step 5 |
| `guidance.md` | `raw/completed/[repo]/` | Step 6 |

### Intermediate Files (Work in Progress)

| File | Location | Step |
|------|----------|------|
| `roadmap_summary.md` | `raw/[repo]/` | Step 1 |
| `keyword_labels.md` | `raw/[repo]/` | Step 2 |
| `pr_list.md` | `raw/[repo]/` | Step 3 |
| `pr_diffs/` | `raw/[repo]/` | Step 4 |
| `assets/` | `raw/[repo]/` | Any |

---

## Files Updated

### 1. README.md
- Updated directory structure diagram
- Changed example link to `raw/completed/slime/slime_analysis.md`
- Updated output path in Type A workflow

### 2. task/Requirements.md
- Updated all 6 steps with correct output paths
- Added "(intermediate)" or "(final)" notes to each deliverable
- Updated Quick Start section

### 3. task/Workflow.md
- Updated Output sections for all 6 steps
- Marked Steps 1-4 as "(intermediate)"
- Marked Steps 5-6 as "(FINAL)"
- Updated "Next Steps" section

---

## Actions Taken

1. ✅ Created `raw/completed/` directory
2. ✅ Created `raw/completed/slime/` subdirectory
3. ✅ Moved `slime_analysis.md` to `raw/completed/slime/`
4. ✅ Updated `README.md` links
5. ✅ Updated `task/Requirements.md` output paths
6. ✅ Updated `task/Workflow.md` output paths
7. ✅ Verified all cross-references

---

## Benefits

- **Clear separation**: Final outputs clearly distinguished from work files
- **Easier navigation**: Completed analyses in one location
- **Better organization**: Work-in-progress files separate from deliverables
- **Scalability**: Easy to add multiple completed analyses

---

## Example Workflow

```
Analyzing a new repository (e.g., "openrlhf"):

1. Create working directory:
   raw/openrlhf/
   ├── roadmap_summary.md
   ├── keyword_labels.md
   ├── pr_list.md
   ├── pr_diffs/
   └── assets/

2. After completing Steps 1-6:
   raw/completed/openrlhf/
   ├── openrlhf_analysis.md
   └── guidance.md
```

---

**Last Updated**: 2026-01-08
