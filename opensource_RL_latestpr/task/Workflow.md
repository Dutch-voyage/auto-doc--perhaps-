# Workflow: RL Framework PR Analysis & Synthesis

**Version**: 1.0
**Last Updated**: 2026-01-08

---

## Overview

This workflow provides step-by-step guidelines for collecting, analyzing, and synthesizing recent developments in RL post-training frameworks.

---

## Prerequisites

- Read `task/Requirements.md` for success criteria
- Review `task/global_keywords.md` for keyword taxonomy
- Prepare repository list from `task/PR_outline.md`
- Install required tools: git, web browser, markdown editor

---

## Workflow Steps

## Step 1: Roadmap Discovery

**Objective**: Locate and extract roadmap documentation from target repositories.

### Procedure

1. **Search for Roadmap Issues**
   - Query: `https://github.com/[org]/[repo]/issues?q=state%3Aopen%20label%3Aroadmap`
   - Check for roadmap milestones and projects
   - Look for `ROADMAP.md`, `docs/roadmap.md`, `future-plans.md`

2. **Extract Roadmap Content**
   - Copy official roadmap items with dates
   - Identify version targets and timelines
   - Note dependencies between features

3. **Fallback: No Explicit Roadmap**
   - Extract future-oriented statements from README
   - Search issues with labels: `enhancement`, `future`, `planned`
   - Check documentation for "upcoming" or "planned" sections

### Output
- Document: `raw/[repo]/roadmap_summary.md` (intermediate)
- Fields: Roadmap items, sources, dates, version targets

### Tools
- GitHub advanced search
- Web scraping for docs sites
- Manual review of README/docs

### Reference
- See: `task/Reference/step1_roadmap_discovery.md`

---

## Step 2: Keyword Taxonomy Assignment

**Objective**: Label repository using global keyword pool.

### Procedure

1. **Review Global Keywords**
   - Read `task/global_keywords.md`
   - Identify relevant categories for the repository

2. **Assign Keywords**
   - Map repository features to global keywords
   - Add repository-specific labels if needed
   - Document rationale for unusual assignments

3. **Update Global Pool (if needed)**
   - Propose new keywords with justification
   - Add to `global_keywords.md` if approved
   - Increment version number

### Output
- Document: `raw/[repo]/keyword_labels.md` (intermediate)
- Fields: Assigned keywords, rationale, new proposals

### Tools
- `task/global_keywords.md` as reference
- Repository README and documentation
- Code analysis for feature identification

### Reference
- See: `task/Reference/step2_keywords.md`

---

## Step 3: PR Search & Filtering

**Objective**: Systematically search for relevant Pull Requests.

### Procedure

1. **Construct Search Queries**
   - Use keywords from Step 2
   - Filter by timeframe (default: last 6-12 months)
   - Include labels: `enhancement`, `feature`, `breaking-change`

2. **GitHub Search Syntax**
   ```
   is:pr is:merged repo:[org]/[repo] [keyword]
   is:pr is:merged repo:[org]/[repo] label:enhancement
   ```

3. **Prioritize PRs**
   - High: Aligns with roadmap items
   - Medium: Major feature additions
   - Low: Bug fixes, documentation

4. **Cross-Reference with Roadmap**
   - Mark PRs that implement roadmap features
   - Identify upcoming features not yet implemented

### Output
- Document: `raw/[repo]/pr_list.md` (intermediate)
- Fields: PR number, title, priority, roadmap alignment

### Tools
- GitHub search with filters
- GitHub API for批量 queries
- Labels and milestones

### Reference
- See: `task/Reference/step3_pr_search.md`

---

## Step 4: Raw PR Collection

**Objective**: Gather complete PR data for analysis.

### Procedure

1. **Extract PR Metadata**
   - PR number, title, author, date
   - Merge status and commit count
   - Associated release version (if any)

2. **Capture Code Changes**
   - Clone repository: `git clone --bare [repo_url]`
   - Export diff: `git format-patch [commit_range]`
   - Save to: `raw/[repo]/pr_diffs/[pr_number].patch`

3. **Capture Discussion**
   - Copy PR description and comments
   - Note review feedback and decisions
   - Document breaking changes and deprecations

4. **Organize Data**
   - Create directory structure: `raw/[repo]/pr_diffs/`
   - Name files: `[pr_number]_[short_title].patch`
   - Index in: `raw/[repo]/pr_index.md`

### Output
- Directory: `raw/[repo]/pr_diffs/` (intermediate)
- Files: `[pr_number].patch`, `pr_index.md`

### Tools
- Git commands: `git format-patch`, `git show`
- GitHub CLI: `gh pr view [pr_number]`
- Python for bulk processing

### Reference
- See: `task/Reference/step4_pr_collection.md`

---

## Step 5: Keyword-Based Synthesis

**Objective**: Create comprehensive summaries organized by theme.

### Procedure

1. **Group PRs by Keyword**
   - Use labels from Step 2
   - Create keyword-based subdirectories
   - Sort PRs by merge date within each group

2. **Analyze Patterns**
   - Identify trends across multiple PRs
   - Note breaking changes and deprecations
   - Track feature evolution over time

3. **Write Thematic Summaries**
   - For each keyword category:
     - Summary of changes
     - Key PRs with numbers
     - Impact assessment
     - Links to raw diffs

4. **Identify Cross-Repo Dependencies**
   - Note if changes affect other frameworks
   - Identify shared patterns across repos
   - Document architectural trends

### Output
- Document: `raw/completed/[repo]/[repo]_analysis.md` (FINAL)
- Structure: Keyword categories → PR summaries → Links

### Tools
- Markdown editor
- Spreadsheet for tracking
- `global_keywords.md` for consistency

### Reference
- See: `task/Reference/step5_synthesis.md`

---

## Step 6: Guidance Documentation

**Objective**: Provide actionable guidelines for staying current.

### Procedure

1. **Summarize Key Trends**
   - Identify 3-5 major development directions
   - Explain significance for users
   - Link to specific PRs as evidence

2. **High-Impact Repositories**
   - Rank repositories by activity and impact
   - Recommend monitoring priority
   - Note release frequency and stability

3. **Monitoring Recommendations**
   - Specific GitHub notifications to watch
   - Key contributors to follow
   - Release channels and feeds

4. **Quick Reference Links**
   - Repository URLs
   - Documentation sites
   - Release pages
   - PR lists filtered by labels

### Output
- Document: `raw/completed/[repo]/guidance.md` (FINAL)
- Sections: Trends, Repositories, Monitoring, Links

### Tools
- Repository analysis
- GitHub insights and statistics
- Community metrics (stars, forks, activity)

### Reference
- See: `task/Reference/step6_guidance.md`

---

## Iteration & Improvement

### After Each Analysis
1. **Review global_keywords.md** for additions
2. **Update workflow** based on learnings
3. **Add examples** to Reference files
4. **Document patterns** for future use

### Continuous Improvement
- Collect feedback on workflow pain points
- Refine keyword taxonomy based on usage
- Automate repetitive steps
- Share learnings across team

---

## Quality Checklist

Before considering analysis complete:

- [ ] All 6 steps executed
- [ ] Roadmap documented with sources
- [ ] Keywords assigned from global pool
- [ ] PRs filtered and prioritized
- [ ] Raw diffs collected and indexed
- [ ] Thematic summaries written
- [ ] Guidance documentation complete
- [ ] All links functional
- [ ] Cross-references updated
- [ ] Version history logged

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No roadmap found | Use README + issues with enhancement labels |
| Too many PRs | Narrow by date, priority, or roadmap alignment |
| Rate limiting | Use GitHub API with authentication |
| Large diffs | Clone repo locally, use git commands |
| Uncategorizable PR | Create new keyword proposal |

---

## Next Steps

After completing workflow:
1. Review `task/Requirements.md` success criteria
2. Move final outputs to `raw/completed/[repo]/`
3. Keep intermediate files in `raw/[repo]/` for reference
4. Propose improvements to this workflow
5. Share findings with team

---

**Workflow Complete** → Return to `task/Requirements.md` for validation
