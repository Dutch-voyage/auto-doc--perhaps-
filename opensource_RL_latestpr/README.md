# Getting Started: RL Framework PR Analysis System

**Start Here** → Read this file first to understand the project and begin work.

---

## What This Project Does

Collects, analyzes, and synthesizes recent developments in **Reinforcement Learning Post-Training Frameworks** to maintain an up-to-date repository of:
- Key feature integrations
- Future development directions
- Strategic insights across multiple frameworks

---

## Directory Structure (3-Layer Architecture)

```
opensource_RL_latestpr/
│
├── README.md                    ← YOU ARE HERE (start guide)
│
├── meta/                        # 🔧 Governance & Usage
│   ├── revision.md              # How to revise documents based on feedback
│   └── instruction.md           # How to use Requirements/Workflow/Reference
│
├── task/                        # 📋 Execution Framework
│   ├── Requirements.md          # WHAT to deliver (tasks, criteria)
│   ├── Workflow.md              # HOW to execute (step-by-step)
│   ├── global_keywords.md       # Keyword taxonomy for categorization
│   ├── PR_outline.md            # List of repositories to analyze
│   ├── Suggetions.md            # User feedback/requests
│   └── Reference/               # Per-step detailed guidance
│       ├── step1_roadmap_discovery.md
│       ├── step3_pr_search.md
│       └── [step2/4/5/6].md     # (TODO - create as needed)
│
└── raw/                         # 📦 Output & Collected Data
    ├── completed/               # ✅ Completed analyses (final outputs)
    │   └── [repo_name]/
    │       └── [repo]_analysis.md
    └── [repo_name]/             # 🚧 Work in progress (intermediate files)
        ├── roadmap_summary.md   # Extracted roadmap
        ├── keyword_labels.md    # Assigned keywords
        ├── pr_list.md           # Filtered PR list
        ├── pr_diffs/            # Raw PR patches
        │   ├── [pr_number].patch
        │   └── pr_index.md
        └── assets/              # Screenshots, diagrams
```

---

## Quick Start (5 Minutes)

### For New Agents

**Step 1**: Understand the Framework
```
Read: meta/instruction.md (2 min)
→ Learn how to navigate Requirements → Workflow → Reference → Output
```

**Step 2**: Know What to Deliver
```
Read: task/Requirements.md (2 min)
→ Understand the 6 steps and success criteria
```

**Step 3**: Know How to Execute
```
Read: task/Workflow.md (1 min)
→ Follow step-by-step procedures
```

### For Returning Agents

**Jump to**: `task/PR_outline.md` → See assigned repositories
**Reference**: `task/global_keywords.md` → Use consistent keywords
**Consult**: `task/Reference/[step].md` → Get detailed guidance

---

## Task Types

### Type A: Analyze a New Repository

**When**: `PR_outline.md` has an unanalyzed repository

**Process**:
1. `Requirements.md` Step 1-6
2. `Workflow.md` → Follow sequentially
3. `Reference/` files → Consult as needed
4. Output → `raw/completed/[repo]/[repo]_analysis.md`

**Example**: See `raw/completed/slime/slime_analysis.md`

### Type B: Create Missing Reference Files

**When**: `Workflow.md` references a non-existent `Reference/[step].md`

**Process**:
1. Read corresponding step in `Requirements.md`
2. Read corresponding step in `Workflow.md`
3. Create `task/Reference/[step].md` with detailed guidance
4. Include: examples, templates, tools, troubleshooting

**Pattern**: Follow structure of `step1_roadmap_discovery.md` or `step3_pr_search.md`

### Type C: Revise Existing Documents

**When**: `Suggestions.md` contains feedback/requests

**Process**:
1. Read `meta/revision.md` → Follow revision workflow
2. Parse suggestions → Identify affected documents
3. Execute revisions → Update cross-references
4. Log changes → Update or create `REVISION_LOG.md`

---

## Common Workflows

### I Need to Analyze a Repository
```
1. task/PR_outline.md          → Get repo URL
2. task/global_keywords.md     → Review keywords
3. task/Requirements.md        → Understand requirements
4. task/Workflow.md            → Execute steps 1-6
5. task/Reference/[step].md    → Detailed guidance per step
6. raw/[repo]/                 → Output results
```

### I Need to Update Framework Documents
```
1. task/Suggestions.md         → Read user feedback
2. meta/revision.md            → Follow revision process
3. task/Requirements.md        → Update if needed
4. task/Workflow.md            → Update if needed
5. task/global_keywords.md     → Update if needed
6. task/REVISION_LOG.md        → Log changes
```

### I Need to Find Something Specific
```
- What to deliver?     → task/Requirements.md
- How to execute?      → task/Workflow.md
- Step details?        → task/Reference/[step].md
- Keywords to use?     → task/global_keywords.md
- How to revise?       → meta/revision.md
- How to navigate?     → meta/instruction.md
```

---

## Essential Reading Order

### Absolute Minimum (2 min)
1. `meta/instruction.md` - Navigation guide

### Before Starting Work (10 min)
1. `meta/instruction.md` - Navigation
2. `task/Requirements.md` - What & why
3. `task/Workflow.md` - How

### Deep Dive (30 min)
1. `meta/instruction.md` - Navigation
2. `task/Requirements.md` - Requirements
3. `task/Workflow.md` - Process
4. `task/global_keywords.md` - Taxonomy
5. `task/Reference/` - Step details (as needed)

---

## File Reference Table

| File | Location | Purpose | When to Read |
|------|----------|---------|--------------|
| **README.md** | Root | Start guide (this file) | **Read first** |
| **Requirements.md** | task/ | What to deliver | Before any work |
| **Workflow.md** | task/ | How to execute | During execution |
| **global_keywords.md** | task/ | Keyword taxonomy | Step 2 |
| **PR_outline.md** | task/ | Repository list | New analysis |
| **Suggestions.md** | task/ | User feedback | Revisions |
| **instruction.md** | meta/ | Navigation guide | When lost |
| **revision.md** | meta/ | Revision workflow | Making changes |
| **step*_*.md** | task/Reference/ | Step details | Stuck on step |

---

## Checklist: Am I Ready?

- [ ] I've read `meta/instruction.md`
- [ ] I understand the 3-layer structure (meta/task/raw)
- [ ] I know where to find Requirements (task/Requirements.md)
- [ ] I know where to find Workflow (task/Workflow.md)
- [ ] I know where to find keywords (task/global_keywords.md)
- [ ] I know where to output results (raw/[repo]/)
- [ ] I know where to log changes (task/REVISION_LOG.md)

**All checked?** → You're ready to begin!

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Don't know where to start | Read `meta/instruction.md` |
| Unsure what to do | Read `task/Requirements.md` |
| Don't know how to do it | Read `task/Workflow.md` |
| Stuck on a specific step | Read `task/Reference/[step].md` |
| Need to change something | Read `meta/revision.md` |
| Can't find a file | Check directory structure above |
| Confused by terminology | Check `global_keywords.md` |

---

## Key Concepts

### Keywords
Standardized tags for categorizing RL framework features. See `task/global_keywords.md`.

### Roadmap Discovery
Finding future plans via GitHub issues labeled "roadmap". See `task/Reference/step1_roadmap_discovery.md`.

### PR Collection
Gathering pull requests with git patches for analysis. See `task/Reference/step4_pr_collection.md` (TODO).

### Synthesis
Organizing PRs by keyword themes to identify trends. See `task/Requirements.md` Step 5.

---

## Version Info

- **Framework Version**: 1.0
- **Last Updated**: 2026-01-08
- **Revision Log**: `task/REVISION_LOG.md`

---

## Support

- **Usage questions**: `meta/instruction.md`
- **Revision process**: `meta/revision.md`
- **Step-by-step help**: `task/Reference/[step].md`

---

**Ready to start?** → Begin with your task type above or read `meta/instruction.md` for detailed navigation.
