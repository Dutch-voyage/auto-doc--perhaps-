# slime PR Collection Index

**Repository**: THUDM/slime
**Collection Date**: 2026-01-08
**Method**: Web-based collection (GitHub API + Web scraping)

---

## Collection Method

### Primary Method: Web Scraping
Since this analysis was conducted via web interface, PR diffs were collected using:

1. **GitHub Web Interface**: Accessed PR pages directly
2. **Web Reader Tools**: Extracted PR descriptions, comments, and metadata
3. **Release Notes**: Collected from GitHub releases page

### Data Collected

For each PR:
- PR number and title
- Author and merge date
- Associated release version (if applicable)
- PR description and key comments
- Code change summary (files affected, lines changed)
- Labels and milestones

---

## High-Priority PRs (Full Collection)

### Fully Documented PRs

The following PRs have complete documentation in this analysis:

#### VLM + FSDP Integration
- `#501` - [FSDP, VLM] feat: add vlm training for FSDP
- `#1056` - [FSDP, VLM] feat: true on policy for VLM
- `#1079` - [VLM, FSDP] Update Experiment Readme
- `#1093` - [VLM] fix: fix non true-on-policy vlm regression

#### FSDP Backend
- `#282` - [feat] init support for FSDP
- `#321` - [FSDP] Data Packing Implementation
- `#344` - [FSDP] Add reference model support for KL
- `#1001` - [FSDP][3/N] support true_on_policy training

#### PPO & RL Algorithms
- `#342` - [feat] init support for PPO
- `#999` - [Feature] Add off-policy sequence masking
- `#1004` - feat: Add Unbiased KL Estimation

---

## Alternative Collection Methods (For Future Use)

### Method 1: GitHub CLI
```bash
# Export individual PR
gh pr view 501 --repo THUDM/slime --json title,body,author,createdAt,mergeCommit,url

# Export PR diff
gh pr diff 501 --repo THUDM/slime > pr_501.patch

# Batch export
gh pr list --repo THUDM/slime --state merged --limit 100 --json number,title | \
  jq -r '.[] | .number' | \
  while read pr; do gh pr diff $pr --repo THUDM/slime > ${pr}.patch; done
```

### Method 2: Git Clone
```bash
# Clone repository
git clone https://github.com/THUDM/slime.git
cd slime

# Export specific PR range
git format-patch -o pr_diffs/ <commit_range>

# Example: v0.2.0 to v0.2.1
git format-patch -o pr_diffs/ v0.2.0..v0.2.1
```

### Method 3: GitHub API
```python
import requests

def collect_prs(repo_owner, repo_name, token=None):
    """Collect PR data using GitHub API"""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    params = {"state": "closed", "per_page": 100}

    all_prs = []
    page = 1

    while True:
        params["page"] = page
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        prs = response.json()
        if not prs:
            break

        all_prs.extend(prs)
        page += 1

    return all_prs

# Usage
prs = collect_prs("THUDM", "slime", token="your_token")
```

---

## PR Storage Structure

### Intended Structure
```
raw/slime/pr_diffs/
├── pr_index.md                    # This file
├── 501_vlm_training_fsdp.patch
├── 1056_true_on_policy_vlm.patch
├── 282_init_fsdp.patch
├── 342_init_ppo.patch
└── ...
```

### Current Status
Due to web-based collection, raw `.patch` files are not stored locally.
All PR information is documented in:
- `pr_list.md` - PR metadata and categorization
- `slime_analysis.md` - Synthesis of PR content

---

## PR Metadata Summary

### Total PRs Analyzed: 150+

| Time Period | Merged PRs | Documented |
|-------------|------------|------------|
| v0.2.1 (latest) | 80+ | 47 high/medium priority |
| v0.2.0 | 100+ | Documented in release notes |
| v0.1.0 | 50+ | Documented in release notes |

### PR Categories
- **High Priority**: 53 PRs (roadmap-aligned, major features)
- **Medium Priority**: 47 PRs (feature additions, optimizations)
- **Low Priority**: 50+ PRs (bug fixes, documentation)

---

## Key PRs by Release

### v0.2.1 (Current)
**Total PRs**: 80+
**Key Features**:
- VLM + FSDP integration
- PD-disaggregation
- DP-attention in R3
- SGLang v0.5.6 upgrade

### v0.2.0 (Major)
**Total PRs**: 100+
**Key Features**:
- FSDP backend introduction
- PPO support
- FP8 full stack
- True on-policy training

### v0.1.0 (Initial)
**Total PRs**: 50+
**Key Features**:
- Initial framework
- SGLang + Megatron integration
- Basic RL algorithms

---

## Collection Completeness

### ✅ Fully Documented
- PR numbers and titles
- Authors and merge dates
- Release associations
- Feature descriptions
- Keyword categorization
- Roadmap alignment

### ⚠️ Partially Documented
- Code diffs (summarized, not raw)
- Comment threads (key points extracted)
- File-level changes (high-level summary)

### ❌ Not Collected
- Raw `.patch` files
- Full comment threads
- Line-by-line diffs
- Commit history

---

## Recommendations for Future Collection

1. **Use GitHub CLI** for automated PR diff collection
2. **Store Raw Patches** for detailed analysis
3. **Create PR Database** for querying and filtering
4. **Automate Collection** with scheduled jobs
5. **Version Control** for PR collections over time

---

## Tools Used

### Current Collection
- Web browser (Chrome/Firefox)
- Web reader tools
- Manual documentation

### Recommended Tools
- **GitHub CLI** (`gh`) - Command-line interface
- **Git** - Version control and patch export
- **Python + PyGitHub** - Automated collection
- **jq** - JSON parsing for API responses

---

## Accessing Raw PR Data

### Online Access
- **PR List**: https://github.com/THUDM/slime/pulls
- **Filtered by Label**: https://github.com/THUDM/slime/pulls?q=label%3Afeature
- **Releases**: https://github.com/THUDM/slime/releases

### API Access
```bash
# Get PR by number
curl https://api.github.com/repos/THUDM/slime/pulls/501

# Get PR diff
curl -L https://github.com/THUDM/slime/pull/501.patch
```

---

**Next Step**: Proceed to synthesis (Step 5)
