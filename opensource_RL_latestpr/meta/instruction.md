# Framework Usage Guide

## Quick Start

1. **Read** `task/Requirements.md` → Understand what to deliver
2. **Follow** `task/Workflow.md` → Execute step-by-step
3. **Reference** `task/Reference/[step].md` → Get detailed guidance for specific steps

---

## Document Navigation

### task/Requirements.md
**Purpose**: Defines tasks, criteria, and success standards

**When to read**:
- Before starting any work
- When unsure about deliverable requirements
- To validate completion

**Key sections**:
- Core Requirements (Steps 1-6)
- Feedback & Revision Guidelines
- Success Criteria checklist

---

### task/Workflow.md
**Purpose**: Step-by-step execution guidelines

**When to read**:
- During execution (follow sequentially)
- When stuck on a specific step
- To understand the overall process flow

**Key sections**:
- Sequential workflow steps
- Tool usage patterns
- Input/output specifications

---

### task/Reference/[step].md
**Purpose**: Per-step detailed guidance, examples, and references

**When to read**:
- When Workflow.md is insufficient
- Need concrete examples for a step
- Troubleshooting specific step issues

**Structure**:
- Each file corresponds to a workflow step
- Contains examples, templates, best practices
- Links to external resources

---

## Usage Patterns

### New User
1. Read `Requirements.md` completely
2. Skim `Workflow.md` for overview
3. Execute steps sequentially, consulting `Reference/` as needed

### Returning User
1. Check `Requirements.md` for any updates
2. Jump to relevant step in `Workflow.md`
3. Reference specific `Reference/[step].md` for details

### Troubleshooting
1. Check `Requirements.md` → Success Criteria
2. Review `Workflow.md` → Current step
3. Deep dive into `Reference/[step].md` → Specific guidance

---

## File Relationships

```
Requirements.md (WHAT)
       ↓
Workflow.md (HOW)
       ↓
Reference/[step].md (DETAILS)
       ↓
raw/[repo]/[repo]_analysis.md (OUTPUT)
```

---

## Common Workflows

### Analyzing a New Repository
1. `Requirements.md` → Step 1-6 overview
2. `Workflow.md` → Follow sequential steps
3. `Reference/step1.md` through `Reference/step6.md` → As needed
4. Output → `raw/[repo]/[repo]_analysis.md`

### Updating Existing Analysis
1. `Requirements.md` → Feedback & Revision Guidelines
2. `meta/revision.md` → Follow revision workflow
3. Update `raw/[repo]/[repo]_analysis.md`

### Adding New Reference Material
1. Identify target step in `Workflow.md`
2. Add content to `Reference/[step].md`
3. Cross-link from `Workflow.md` if needed

---

## Maintenance

- **Requirements.md**: Update when task criteria change
- **Workflow.md**: Update when process improves
- **Reference/**: Add per-step examples as they emerge
- **meta/revision.md**: Track all changes

---

## Key Principles

- **Start with Requirements**: Never skip understanding what to deliver
- **Follow Workflow Sequentially**: Steps build on each other
- **Reference as Needed**: Deep dive only when necessary
- **Output to raw/**: Keep raw material separate from framework
