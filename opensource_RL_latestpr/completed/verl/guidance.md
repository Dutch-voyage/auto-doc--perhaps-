# Guidance: Staying Current with verl

**Last Updated**: 2026-01-08
**Repository**: [volcengine/verl](https://github.com/volcengine/verl)
**Based on Analysis**: 2025-2026 developments

---

## Executive Summary

**verl** is a production-ready RL training library for LLMs that has undergone significant evolution in 2025-2026, focusing on modularity (FSDP2 migration), async architecture (20-40% throughput gains), multi-turn RL, and comprehensive VLM support. This guidance provides actionable recommendations for staying current with verl developments.

---

## Key Development Trends (2025-2026)

### 1. **FSDP2 Migration & Modularity**

**Trend**: Complete migration from FSDP1 to FSDP2 as default training backend

**Impact**:
- Better throughput and memory usage
- Composability with PyTorch features (torch.compile)
- CPU offloading support

**Evidence**:
- v0.7.0 release (November 2025): All recipes switched to FSDP2
- Q3 roadmap: "switch all recipe/examples from fsdp1 to fsdp2 by default"

**Monitoring Priority**: **HIGH**

---

### 2. **Async Architecture & Performance**

**Trend**: Implementation of fully async training pipeline for significant performance gains

**Impact**:
- 20-40% throughput improvement
- Better resource utilization
- Reduced idle time

**Evidence**:
- PR #2981: Fully async training recipe (v0.6.1)
- Q3 roadmap: "one-step off async pipeline" and "fully-async pipeline"

**Monitoring Priority**: **HIGH**

---

### 3. **Multi-turn RL & Agentic AI**

**Trend**: Comprehensive support for multi-turn conversations and tool calling

**Impact**:
- Dynamic conversational feedback
- Iterative problem-solving scenarios
- Tool integration (search, sandbox fusion)

**Evidence**:
- PRs #4067, #4125, #4182: Multi-turn and tool call support (v0.7.0)
- Q3 roadmap: "Agent RL infrastructure"

**Monitoring Priority**: **HIGH**

---

### 4. **Vision-Language Model Support**

**Trend**: Full VLM capabilities across model engine, SFT, and RL trainers

**Impact**:
- Comprehensive multimodal RL training
- Support for Qwen3VL, Qwen2.5-vl, Kimi-VL
- Video input support

**Evidence**:
- PRs #3838, #4186, #4734: VLM support (v0.6.1-v0.7.0)
- Q3 roadmap: "better abstraction and registration system for multi-modal models"

**Monitoring Priority**: **MEDIUM**

---

### 5. **New RL Algorithms**

**Trend**: Expansion beyond PPO/GRPO with advanced algorithms

**Impact**:
- CISPO (Clipped IS-weight Policy Optimization)
- SAPO (Soft Adaptive Policy Optimization)
- DAPO (SOTA on AIME 2024)
- VAPO, PF-PPO (ICML 2025)

**Evidence**:
- v0.7.0 release: CISPO and SAPO
- DAPO: 50 points on AIME 2024 (Qwen2.5-32B)

**Monitoring Priority**: **MEDIUM**

---

## High-Priority Repositories

### verl: Primary Focus

**Organization**: [volcengine](https://github.com/volcengine)
**Repository**: [verl](https://github.com/volcengine/verl)
**Activity Level**: **VERY HIGH**
**Release Frequency**: Quarterly major releases, frequent minor releases
**Production Maturity**: **HIGH**

**Why Monitor**:
1. Leading open-source RLHF framework (HybridFlow, EuroSys 2025)
2. Production-proven at scale (671B parameters)
3. Active development with significant quarterly releases
4. Strong community support and adoption
5. Used by major companies (Bytedance, Anyscale, LMSys.org)

---

### verl-recipe: Training Recipes

**Organization**: [volcengine](https://github.com/volcengine)
**Repository**: [verl-recipe](https://github.com/volcengine/verl-recipe)
**Status**: Submodule (migrated in January 2026)
**Activity Level**: **HIGH**

**Why Monitor**:
1. Contains production-ready training recipes
2. Includes DAPO, ReTool, and other advanced algorithms
3. Demonstrates best practices for verl usage
4. Regular updates with new recipes

**Access**: Use `git submodule update --init --recursive recipe`

---

### Related Projects

**HybridFlow Paper**:
- arXiv: [2409.19256](https://arxiv.org/abs/2409.19256)
- EuroSys 2025 acceptance

**Community Projects**:
- Various blog posts and tutorials (see verl README)

---

## Monitoring Strategy

### GitHub Notifications

**Watch Settings**:
- **Repository**: volcengine/verl
- **Notification Level**: "Custom" → select:
  - ✓ Releases
  - ✓ Issues
  - ✓ Pull Requests
  - ✗ Discussions (optional)

**How to Set Up**:
1. Go to https://github.com/volcengine/verl
2. Click "Watch" → "Custom"
3. Select notification preferences

---

### Key Contributors to Follow

**Core Team**:
- @eric-haibin-lin (maintainer, roadmap author)
- @vermouth1992 (core contributor, roadmap tasks)
- @SwordFaith (core contributor, multi-turn/infra)

**How to Follow**:
1. GitHub: Follow their profiles
2. Activity: Watch their PRs and issues
3. Updates: Monitor their comments and discussions

---

### Release Channels

**Official Releases**:
- **GitHub Releases**: [volcengine/verl/releases](https://github.com/volcengine/verl/releases)
- **Frequency**: Quarterly major releases (v0.7.0: Nov 2025, v0.6.1: Apr 2025)

**Release Notes Format**:
- Version number and date
- Key features and improvements
- Breaking changes
- Migration guides

**Monitoring Actions**:
- Star/fork the repository
- Enable email notifications for releases
- Review release notes within 1 week of release

---

### Roadmap Tracking

**Q3 Roadmap**:
- **Issue**: [#2388](https://github.com/volcengine/verl/issues/2388)
- **Status**: Active (published July 2025)
- **Focus**: Modular foundational library, async architecture, multi-turn RL

**How to Track**:
1. Bookmark the roadmap issue
2. Check for quarterly updates (Q4, Q1 2026)
3. Watch linked PRs for implementation progress

---

### Documentation Updates

**Official Documentation**:
- **URL**: [verl.readthedocs.io](https://verl.readthedocs.io/)
- **Sections**:
  - Installation guide
  - Quickstart tutorials
  - Programming guide
  - Performance tuning
  - Advanced usage (extension)

**Monitoring Actions**:
- Check documentation monthly for new sections
- Review "What's New" or "Changelog" pages
- Follow blog posts and community tutorials

---

## Quick Reference Links

### Repository & Documentation

| Resource | URL | Purpose |
|----------|-----|---------|
| **GitHub Repository** | [github.com/volcengine/verl](https://github.com/volcengine/verl) | Source code, issues, PRs |
| **Documentation** | [verl.readthedocs.io](https://verl.readthedocs.io/) | Official docs, tutorials |
| **Releases** | [github.com/volcengine/verl/releases](https://github.com/volcengine/verl/releases) | Release notes, versions |
| **Q3 Roadmap** | [Issue #2388](https://github.com/volcengine/verl/issues/2388) | Development priorities |
| **Recipe Submodule** | [github.com/volcengine/verl-recipe](https://github.com/volcengine/verl-recipe) | Training recipes |

---

### Key PRs & Issues

| Topic | URL | Status |
|-------|-----|--------|
| **Fully Async Training** | [#2981](https://github.com/volcengine/verl/pull/2981) | Merged (v0.6.1) |
| **Multi-turn Support** | [#4067](https://github.com/volcengine/verl/pull/4067), [#4125](https://github.com/volcengine/verl/pull/4125), [#4182](https://github.com/volcengine/verl/pull/4182) | Merged (v0.7.0) |
| **Model Engine** | [#4211](https://github.com/volcengine/verl/pull/4211), [#4213](https://github.com/volcengine/verl/pull/4213), [#4233](https://github.com/volcengine/verl/pull/4233) | Merged (v0.7.0) |
| **VLM Support** | [#3838](https://github.com/volcengine/verl/pull/3838), [#4186](https://github.com/volcengine/verl/pull/4186), [#4734](https://github.com/volcengine/verl/pull/4734) | Merged (v0.6.1-v0.7.0) |
| **Breaking Changes** | [#2270](https://github.com/volcengine/verl/issues/2270) | Active |

---

### Performance Benchmarks

| Benchmark | Score | Model | Reference |
|-----------|-------|-------|-----------|
| **DAPO on AIME 2024** | 50 points | Qwen2.5-32B | README |
| **Doubao-1.5-pro on AIME** | 70.0 pass@1 | - | README |
| **VAPO on AIME 2024** | 60.4 | Qwen-32B-base | README |
| **Async Throughput Gain** | 20-40% | - | PR #2981 |
| **FSDP2 Speedup** | ~1.4x | - | v0.3.0.post1 |

---

### Papers & Research

| Paper | Venue | URL |
|-------|-------|-----|
| **HybridFlow** | EuroSys 2025 | [arXiv:2409.19256](https://arxiv.org/abs/2409.19256) |
| **VAPO** | - | [arXiv:2504.05118](https://arxiv.org/abs/2504.05118) |
| **PF-PPO** | ICML 2025 | [arXiv:2409.06957](https://arxiv.org/abs/2409.06957) |
| **DAPO** | - | recipe/dapo |

---

### Community & Support

| Resource | URL | Purpose |
|----------|-----|---------|
| **GitHub Issues** | [github.com/volcengine/verl/issues](https://github.com/volcengine/verl/issues) | Bug reports, feature requests |
| **GitHub Discussions** | [github.com/volcengine/verl/discussions](https://github.com/volcengine/verl/discussions) | Community Q&A |
| **Performance Tuning** | [verl.readthedocs.io/perf/perf_tuning](https://verl.readthedocs.io/en/latest/perf/perf_tuning.html) | Optimization guide |
| **Blog Posts** | See README "Blogs from the community" | Community tutorials |

---

## Actionable Monitoring Recommendations

### Daily/Weekly

1. **Check GitHub Notifications** (for watched repos)
   - Review new issues and PRs
   - Monitor discussions in followed threads

2. **Monitor Twitter/X** (optional)
   - Follow @ByteDanceSeedTeam
   - Track #verl, #RLHF hashtags

---

### Monthly

1. **Review Release Notes**
   - Check for new releases
   - Review breaking changes
   - Plan migration if needed

2. **Check Documentation**
   - Review "What's New" sections
   - Check for new tutorials or guides

3. **Scan GitHub Issues**
   - Look for roadmap discussions
   - Check for RFCs (Request for Comments)

---

### Quarterly

1. **Review Roadmap Updates**
   - Check Q3 roadmap [#2388](https://github.com/volcengine/verl/issues/2388) for updates
   - Look for Q4, Q1 2026 roadmap discussions

2. **Analyze Major Releases**
   - Review comprehensive release notes
   - Plan migration for breaking changes
   - Test new features in development environment

3. **Evaluate Community Recipes**
   - Check verl-recipe submodule for new recipes
   - Review community contributions

---

### Semi-Annually

1. **Comprehensive Update**
   - Review all developments since last update
   - Plan migration to latest stable version
   - Evaluate new features for adoption

2. **Performance Benchmarking**
   - Run performance benchmarks on new versions
   - Compare with previous versions
   - Update infrastructure if beneficial

---

## Integration with Workflow

### For Developers

**When Using verl**:
1. Start with latest stable release
2. Follow official documentation
3. Monitor issues for known problems
4. Update quarterly for bug fixes and features

**When Extending verl**:
1. Review source code on GitHub
2. Follow contribution guidelines
3. Submit RFCs for major features
4. Engage with community via discussions

---

### For Researchers

**When Citing verl**:
1. Cite HybridFlow paper (EuroSys 2025)
2. Reference GitHub repository
3. Note version number used
4. Check for algorithm-specific papers (DAPO, VAPO, etc.)

**When Comparing Frameworks**:
1. Review latest performance benchmarks
2. Check for new algorithms
3. Compare feature sets
4. Monitor community adoption

---

### For Production Teams

**When Deploying verl**:
1. Use stable releases (not main branch)
2. Monitor breaking changes issue [#2270](https://github.com/volcengine/verl/issues/2270)
3. Test upgrades in staging environment
4. Follow performance tuning guide

**When Scaling**:
1. Review Megatron backend for large models
2. Consider async architecture for throughput
3. Evaluate FSDP2 for memory efficiency
4. Monitor Q3 roadmap for scalability improvements

---

## Conclusion

verl is a rapidly evolving, production-ready RL training framework with strong community support and regular significant releases. To stay current:

1. **Watch the repository** for releases and issues
2. **Follow core contributors** for insights
3. **Review quarterly roadmaps** for direction
4. **Monitor documentation** for new features
5. **Engage with community** via discussions and issues

**Key Focus Areas for 2026**:
- FSDP2 optimization and advanced features
- Async pipeline improvements
- Multi-turn RL and agent capabilities
- VLM/multimodal enhancements
- Performance tuning and scalability

---

**Guidance Document Complete**

For detailed analysis, see: [verl_analysis.md](./verl_analysis.md)
For raw materials, see: `../../raw/verl/`
