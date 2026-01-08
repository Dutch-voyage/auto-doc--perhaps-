# Meta-Revision Guide

## Directory Structure

```
opensource_RL_latestpr/
├── meta/                          # Meta layer: governance & usage
│   ├── revision.md                # THIS FILE - Revision workflow
│   └── instruction.md             # (TODO) How to use Requirements/Workflow/Reference
│
├── raw/                           # Raw material: collected data
│   └── [repo_name]/
│       ├── [repo_name]_analysis.md
│       ├── pr_diffs/
│       └── assets/
│
└── task/                          # Task layer: execution framework
    ├── Requirements.md            # What to deliver (tasks, criteria)
    ├── Workflow.md                # How to execute (step-by-step)
    └── Reference/                 # Per-step guidance
        ├── [step1].md
        ├── [step2].md
        └── ...
```

## Purpose
Process user feedback `.md` files containing scattered suggestions to revise framework documentation.

## Target Documents

| File | Location | Purpose | Scope |
|------|----------|---------|-------|
| **Requirements.md** | `task/` | Tasks, criteria, success standards | What to deliver |
| **Workflow.md** | `task/` | Step-by-step execution guidelines | How to execute |
| **Reference/[node].md** | `task/Reference/` | Per-step references & examples | Specific step guidance |
| **[repo]_analysis.md** | `raw/[repo]/` | Collected PR analysis & findings | Output artifacts |

## Revision Workflow

### 1. Parse Feedback
- Extract actionable suggestions from user-provided `.md`
- Categorize by target document (`task/` or `meta/`)
- Identify conflicts or ambiguities → ask for clarification

### 2. Determine Revision Type
- **Minor**: Single section, no cross-file impact → edit directly
- **Major**: Multiple sections/files affected → create revision plan first

### 3. Execute Revisions
- Apply changes to target files
- Update all cross-references
- Maintain consistency across documents
- Preserve version history in comments

### 4. Validate
- ✓ Internal consistency (no contradictions)
- ✓ Cross-document alignment (`task/` ↔ `meta/` ↔ `raw/`)
- ✓ All links functional (relative paths correct)
- ✓ Success criteria still met

### 5. Present Changes
- Summary of modifications made
- Files affected
- Follow-up actions needed

## Revision Log Template

```markdown
## Revision: [DATE]
**Type**: [Minor/Major]
**Source**: [user_feedback_file.md]

### Changes
- [File]: [specific change]

### Impact Assessment
- Cross-references updated: [Yes/No]
- Other files affected: [list]
- Requires re-validation: [Yes/No]

### Status: ✓ Complete | ⏳ In Progress
```

## Key Principles
- **Specificity**: Each suggestion maps to exact file/section
- **Traceability**: All changes logged with source reference
- **Layer Separation**: Meta (governance) / Task (execution) / Raw (output)
- **Consistency**: Requirements, Workflow, and Reference remain aligned
- **Minimal**: Concise edits, no unnecessary expansion