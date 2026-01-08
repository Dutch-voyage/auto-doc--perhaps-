# slime: Guidance for Staying Current

**Repository**: [THUDM/slime](https://github.com/THUDM/slime)
**Last Updated**: 2026-01-08
**Purpose**: Actionable guidelines for monitoring slime developments

---

## Key Trends (What to Watch)

### 1. 🎯 Multi-Modal RL Training (HIGH PRIORITY)
**Trend**: True on-policy VLM training is slime's breakthrough capability

**What to Monitor**:
- VLM + FSDP integration PRs (#1210 series)
- Qwen3-VL and Qwen2.5-VL support
- True on-policy training enhancements
- VLM bug fixes and optimizations

**Why It Matters**:
- Industry-first capability
- Competitive advantage over other frameworks
- Critical for vision-language model post-training

**Tracking Links**:
- [VLM-related PRs](https://github.com/THUDM/slime/pulls?q=is%3Apr+VLM)
- [Megatron VLM Support](https://github.com/THUDM/slime/pull/1210)

---

### 2. ⚡ FSDP Backend Evolution (HIGH PRIORITY)
**Trend**: FSDP becoming the primary training backend

**What to Monitor**:
- FSDP feature additions and optimizations
- FSDP training script additions
- True on-policy training improvements
- FSDP bug fixes and stability improvements

**Why It Matters**:
- Replacing Megatron for new deployments
- Better scalability and memory efficiency
- Industry-wide trend toward FSDP

**Tracking Links**:
- [FSDP PRs](https://github.com/THUDM/slime/pulls?q=is%3Apr+FSDP)
- [FSDP Issues](https://github.com/THUDM/slime/issues?q=is%3Aissue+FSDP)

---

### 3. 🤖 Agent-Centric Features (MEDIUM PRIORITY)
**Trend**: Growing investment in agentic AI and tool use

**What to Monitor**:
- Multi-agent training examples
- Tool call support and integration
- Strands-agents integration
- Router OAI interface updates

**Why It Matters**:
- Aligns with agentic AI industry trend
- Growing importance of tool-using agents
- Multi-agent scenarios becoming more common

**Tracking Links**:
- [Agent PRs](https://github.com/THUDM/slime/pulls?q=is%3Apr+agent)
- [Tool Integration PRs](https://github.com/THUDM/slime/pulls?q=is%3Apr+tool)

---

### 4. 🎛️ Quantization & Efficiency (MEDIUM PRIORITY)
**Trend**: Comprehensive quantization support for deployment efficiency

**What to Monitor**:
- Int4 QAT implementation (#1172)
- FP8 weight updates and optimizations
- Quantization workflow improvements
- Memory optimization features

**Why It Matters**:
- Critical for production deployment
- Significant cost savings (2x+ speedup, 50% memory reduction)
- Expands deployment options

**Tracking Links**:
- [Quantization PRs](https://github.com/THUDM/slime/pulls?q=is%3Apr+quantization)
- [FP8 PRs](https://github.com/THUDM/slime/pulls?q=is%3Apr+FP8)

---

### 5. 🛡️ Production Readiness (MEDIUM PRIORITY)
**Trend**: Focus on fault tolerance and reproducibility

**What to Monitor**:
- Fault tolerance improvements (#1311)
- Deterministic training features
- Docker and deployment fixes
- CI/CD enhancements

**Why It Matters**:
- Production deployment requirements
- Reliability at scale
- slime's production-first philosophy

**Tracking Links**:
- [Fault Tolerance PRs](https://github.com/THUDM/slime/pulls?q=is%3Apr+fault)
- [Docker PRs](https://github.com/THUDM/slime/pulls?q=is%3Apr+docker)

---

## High-Priority Repositories to Monitor

### Primary: slime (THUDM/slime)
**Priority**: ⭐⭐⭐⭐⭐ (Highest)

**Why Monitor**:
- Most active RL framework development
- Industry-leading VLM capabilities
- Production battle-tested (GLM-4.5/4.6)
- Rapid innovation cycle

**Monitoring Strategy**:
- **Daily**: Watch for new PRs and issues
- **Weekly**: Review merged PRs in high-priority categories
- **Monthly**: Comprehensive review of all changes

**Activity Level**: Very High (50+ active contributors, 55 open PRs)

---

### Secondary: Related Projects

**SGLang** (sgl-project/sglang)
- **Priority**: ⭐⭐⭐⭐
- **Why**: Tight integration with slime
- **Monitor**: Rollout/inference features
- **Link**: https://github.com/sgl-project/sglang

**Megatron-LM** (NVIDIA/Megatron-LM)
- **Priority**: ⭐⭐⭐
- **Why**: Training backend for slime
- **Monitor**: Parallel strategy improvements
- **Link**: https://github.com/NVIDIA/Megatron-LM

---

## Monitoring Strategy

### GitHub Notifications

**Watch Settings**:
1. Go to https://github.com/THUDM/slime
2. Click "Watch" → Select "Custom"
3. Enable:
   - ✓ Issues
   - ✓ Pull requests
   - ✓ Releases
   - ✗ Discussions (optional)

**Email Filters** (Gmail example):
```
from:github.com  subject:[THUDM/slime]
```

---

### Weekly Checks (30 minutes)

**1. Review New PRs** (10 min)
- Visit: https://github.com/THUDM/slime/pulls
- Filter by: "label:enhancement" or "label:feature"
- Focus: VLM, FSDP, agent, quantization

**2. Check Releases** (5 min)
- Visit: https://github.com/THUDM/slime/releases
- Look for: New versions, breaking changes

**3. Review Issues** (10 min)
- Visit: https://github.com/THUDM/slime/issues
- Filter by: "label:roadmap" or "label:enhancement"
- Identify: Future planned features

**4. Scan Commits** (5 min)
- Visit: https://github.com/THUDM/slime/commits/main
- Look for: High-impact commits

---

### Monthly Deep Dive (2 hours)

**1. Review All Merged PRs** (45 min)
- Filter by: "is:pr is:merged merged:>=2024-XX-01"
- Categorize by keyword
- Update analysis document

**2. Analyze Trends** (30 min)
- Identify new development patterns
- Compare with previous month
- Note strategic shifts

**3. Update Keyword Taxonomy** (15 min)
- Review `global_keywords.md`
- Add new keywords if needed
- Update keyword labels for slime

**4. Documentation Updates** (30 min)
- Update `slime_analysis.md`
- Add new PRs to `pr_list.md`
- Document roadmap changes

---

## Key Contributors to Follow

### Core Maintainers
- **@zhuzilin** - Core architecture, FSDP features
- **@lilei199908** - FSDP backend, releases
- **@nanjiangwill** - VLM features and integration
- **@fzyzcjy** - Performance optimization

### How to Follow
1. Visit contributor's GitHub profile
2. Click "Follow" to see their activity
3. Monitor their PRs and issues in slime

---

## RSS Feeds & Atom Feeds

### Releases Feed
```
https://github.com/THUDM/slime/releases.atom
```

### Commits Feed
```
https://github.com/THUDM/slime/commits/main.atom
```

### PRs Feed
```
https://github.com/THUDM/slime/pulls.atom
```

---

## Quick Reference Links

### Essential Resources
| Resource | URL | Purpose |
|----------|-----|---------|
| **Repository** | https://github.com/THUDM/slime | Main repo |
| **Documentation** | https://thudm.github.io/slime/ | Official docs |
| **Releases** | https://github.com/THUDM/slime/releases | Version history |
| **Pull Requests** | https://github.com/THUDM/slime/pulls | All PRs |
| **Issues** | https://github.com/THUDM/slime/issues | Roadmap, bugs |
| **Discussions** | https://github.com/THUDM/slime/discussions | Community |

### Filtered Views (High-Priority Keywords)
| Keyword | URL | Focus |
|---------|-----|-------|
| **VLM** | [PRs](https://github.com/THUDM/slime/pulls?q=is%3Apr+VLM) | Vision-language |
| **FSDP** | [PRs](https://github.com/THUDM/slime/pulls?q=is%3Apr+FSDP) | Training backend |
| **PPO** | [PRs](https://github.com/THUDM/slime/pulls?q=is%3Apr+PPO) | RL algorithms |
| **Agent** | [PRs](https://github.com/THUDM/slime/pulls?q=is%3Apr+agent) | Agentic AI |
| **Quantization** | [PRs](https://github.com/THUDM/slime/pulls?q=is%3Apr+quantization) | Efficiency |

### Roadmap & Future
| Resource | URL | Content |
|----------|-----|---------|
| **Roadmap Issues** | https://github.com/THUDM/slime/issues?q=label%3Aroadmap | Future plans |
| **Enhancement Issues** | https://github.com/THUDM/slime/issues?q=is%3Aissue+label%3Aenhancement | Planned features |
| **Blog Posts** | https://github.com/THUDM/slime#blogs | Vision & direction |

---

## Triggers for Immediate Review

**Review Immediately When**:
1. New major version released (v0.3.0, etc.)
2. Breaking changes announced
3. Security vulnerabilities disclosed
4. Significant architecture changes
5. New model family support announced

**Review Within 24 Hours**:
- High-priority PRs merged (VLM, FSDP)
- Critical bug fixes
- Performance regression fixes

---

## Integration with Analysis Documents

### Link to Full Analysis
This guidance document is part of the comprehensive slime analysis:
- **Main Analysis**: [slime_analysis.md](./slime_analysis.md)
- **Roadmap**: [roadmap_summary.md](../../slime/roadmap_summary.md)
- **Keywords**: [keyword_labels.md](../../slime/keyword_labels.md)
- **PR List**: [pr_list.md](../../slime/pr_list.md)

### Update Workflow
1. Follow monitoring strategy above
2. Collect new PR data
3. Update intermediate files
4. Regenerate analysis (Step 5)
5. Update this guidance (Step 6)

---

## Success Metrics

**You're staying current if**:
- ✓ Aware of new releases within 24 hours
- ✓ Review high-priority PRs weekly
- ✓ Understand key development trends
- ✓ Can explain slime's competitive advantages
- ✓ Know upcoming features from roadmap
- ✓ Track progress on in-development features

---

## Summary

**slime's Key Strengths**:
1. **VLM RL Training**: Industry-leading true on-policy capabilities
2. **Scalability**: Comprehensive parallel strategies, FSDP backend
3. **Production Ready**: Battle-tested at scale (GLM-4.5/4.6)
4. **Rapid Innovation**: Active development, frequent releases

**Primary Focus Areas**:
- VLM + FSDP integration (highest priority)
- Agent-centric features (growing importance)
- Quantization & efficiency (production deployment)

**Monitoring Commitment**:
- Weekly checks: 30 minutes
- Monthly deep dive: 2 hours
- Immediate review: Major releases/breaking changes

---

**Next Review**: 2026-02-08
**Analysis Version**: 1.0
**Framework Version**: v0.2.1
