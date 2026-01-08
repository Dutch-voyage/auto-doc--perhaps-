# AReaL Roadmap Summary

**Last Updated**: 2026-01-08
**Source**: https://raw.githubusercontent.com/inclusionAI/AReaL/main/ROADMAP.md
**Repository**: https://github.com/inclusionAI/AReaL

---

## 2025 Q4 Roadmap (due January 31, 2026)

**Tracking Issue**: [GitHub Issue #542](https://github.com/inclusionAI/AReaL/issues/542)

### Backends - On-going

| Feature | Status | Source |
|---------|--------|--------|
| Single-controller mode | On-going | [#260](https://github.com/inclusionAI/AReaL/issues/260) |
| Detailed profiling for optimal performance across different scales | On-going | - |
| RL training with cross-node vLLM pipeline/context parallelism | On-going | - |

### Backends - Planned but not in progress

| Feature | Status | Description |
|---------|--------|-------------|
| Multi-LLM training | Planned | Different agents with different parameters |
| Data transfer optimization in single-controller mode | Planned | - |
| Auto-scaling inference engines in single-controller mode | Planned | - |
| Elastic weight update setup and acceleration | Planned | - |
| Low-precision RL training | Planned | - |

### Usability - Planned but not in progress

| Feature | Status | Description |
|---------|--------|-------------|
| Wrap training scripts into trainers | Planned | - |
| Fully respect allocation mode in trainers/training scripts | Planned | - |
| Support distributed training and debugging in Jupyter notebooks | Planned | - |
| Refactor FSDP/Megatron engine/controller APIs to finer granularity | Planned | - |
| Add CI pipeline to build Docker images upon release | Planned | - |
| Example of using a generative or critic-like reward model | Planned | - |

### Documentation - Planned but not in progress

| Feature | Status |
|---------|--------|
| Tutorial on how to write efficient async rollout workflows | Planned |
| Benchmarking and profiling guide | Planned |
| Use case guides: offline inference, offline evaluation, multi-agent training | Planned |
| AReaL performance tuning guide | Planned |
| Device allocation strategies for training and inference | Planned |
| Parallelism strategy configuration for training and inference | Planned |

---

## Historical Roadmaps

### 2025 Q3 ([#257](https://github.com/inclusionAI/AReaL/issues/257))

#### Backends - Completed

| Feature | Status |
|---------|--------|
| Megatron training backend support | ✅ Completed |
| SGLang large expert parallelism (EP) inference support | ✅ Completed |
| Remote vLLM inference engine | ✅ Completed |
| Ulysses context parallelism & tensor parallelism for FSDP backend | ✅ Completed |
| End-to-end MoE RL training with large EP inference and Megatron expert parallelism | ✅ Completed |
| Distributed weight resharder for Megatron training backend | ✅ Completed |

#### Backends - Canceled

| Feature | Status |
|---------|--------|
| Local SGLang inference engine with inference/training colocation (hybrid engine) | ❌ Canceled |
| RL training with SGLang pipeline parallelism | ❌ Canceled |

#### Usability - Completed

| Feature | Status |
|---------|--------|
| OpenAI-compatible client support | ✅ Completed |
| Support RLOO | ✅ Completed |
| Benchmarking configuration examples (DAPO, Bradley-Terry, PPO with critic, REINFORCE++) | ✅ Completed |

#### Documentation - Completed

| Feature | Status |
|---------|--------|
| OpenAI-compatible client documentation | ✅ Completed |
| Out-of-memory (OOM) troubleshooting guide | ✅ Completed |
| AReaL debugging best practices | ✅ Completed |

---

## Long-Term Vision

AReaL aims to become the **go-to framework for training reasoning and agentic AI systems** with:

1. **Accessible**: Easy to get started for researchers and practitioners
2. **Scalable**: Scales from laptop to 1000+ GPU clusters seamlessly
3. **Flexible**: Supports diverse algorithms, models, and use cases
4. **Performant**: Industry-leading training speed and efficiency
5. **Open**: Fully open-source with transparent development

---

## Release Cycle

- **Minor Releases**: Bi-weekly (bug fixes, small improvements, new features)
- **Major Releases**: Quarterly (important milestones and significant changes)

---

## Notes

- The roadmap is organized into "On-going" features actively developed by core team, and "Planned but not in progress" features where community contributions are welcome
- Historical roadmaps show completed and canceled features from previous quarters
- The project values community input for shaping the roadmap through feature requests, discussions, and contributions
