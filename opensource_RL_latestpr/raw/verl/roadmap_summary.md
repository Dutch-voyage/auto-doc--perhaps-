# verl Roadmap Summary

**Last Updated**: 2026-01-08
**Repository**: [volcengine/verl](https://github.com/volcengine/verl)
**Primary Roadmap Source**: [Q3 Roadmap Issue #2388](https://github.com/volcengine/verl/issues/2388)

---

## Repository Overview

**verl** (Volcano Engine Reinforcement Learning for LLMs) is a flexible, efficient and production-ready RL training library for large language models. It is the open-source version of the **HybridFlow** paper (EuroSys 2025).

**Key Capabilities**:
- Training backends: FSDP, FSDP2, Megatron-LM
- Rollout engines: vLLM, SGLang, HF Transformers
- RL algorithms: PPO, GRPO, GSPO, ReMax, REINFORCE++, RLOO, PRIME, DAPO, DrGRPO
- VLM support and multi-modal RL
- Scales up to 671B models with expert parallelism

---

## Q3 Development Roadmap

**Source**: [Issue #2388](https://github.com/volcengine/verl/issues/2388)
**Published**: 2025-07-07
**Theme**: "Make it a modular foundational library for the community to extend"

### 1. Composable Model Engines

**Status**: In Progress (WIP)
**Related PRs**: [#1560](https://github.com/volcengine/verl/pull/1560), [#1977](https://github.com/volcengine/verl/pull/1977)

**Goal**: Implement parallelism strategy at engine level, without exposing details to worker(role) level.

**Planned Features**:
- FSDP actor, critic, ref (focus on FSDP2)
- Megatron actor, critic, ref
- Torchtitan integration (call for contribution)
- Switch all recipe/examples from FSDP1 to FSDP2 by default
- Remove ill-maintained examples

**Dependencies**: None specified

---

### 2. Rollout Workers Optimization

**Status**: In Progress
**Related Issues**: [#2618](https://github.com/volcengine/verl/issues/2618), [#1882](https://github.com/volcengine/verl/issues/1882)

**Goal**: Optimize server mode rollout performance and modularize rollout workers.

**Planned Features**:
- Optimize server mode rollout performance
- Modular rollout workers: VllmRolloutWorker and SGLangRolloutWorker (exposing same APIs)
- Support model with random init weight
- Weight resharding: optimize TP x DP dispatch
- Support receiving weight from separate resource groups
- Agent RL infrastructure for multi-turn rollout and agent loop

**Related Roadmap Items**:
- Multi-turn rollout & agentic RL Status & Roadmap (see [zhaochenyang20/Awesome-ML-SYS-Tutorial#131](https://github.com/zhaochenyang20/Awesome-ML-SYS-Tutorial/issues/131))
- Rollout Module Development Progress & Roadmap [#1882](https://github.com/volcengine/verl/issues/1882)

---

### 3. Async & Disaggregated Architecture

**Status**: WIP
**Related PRs**: [#2231](https://github.com/volcengine/verl/pull/2231), [#2200](https://github.com/volcengine/verl/pull/2200)

**Goal**: Implement async pipeline and disaggregated resource allocation.

**Planned Features**:
- One-step off async pipeline (WIP in #2231)
- Streaming/partial rollout (WIP in #2200)
- Performance tuning and reference throughput benchmark
- Fully-async pipeline

**Benchmark Targets**: [model type, model size, seqlen, hardware, num accelerators, worker role]

---

### 4. Multi-turn, Data, Config Infrastructure

**Status**: Planned
**Related PRs**: [#2379](https://github.com/volcengine/verl/pull/2379), [#2539](https://github.com/volcengine/verl/pull/2539)

**Goal**: Improve message infrastructure and dataset schema for multi-turn RL.

**Planned Features**:
- Better message infra for multi-turn messages, dense reward
- Better dataset schema for train & rollout (documentation needed)
- Use tensordict and nested-tensor to remove padding and replace DataProto
- Replace omegaConf with read-only dataclass for config passing
- Distributed data pool (see [arXiv:2507.01663v1](https://arxiv.org/pdf/2507.01663v1))

**References**: TRL documentation for dataset formats

---

### 5. Streamline New Model Workflow

**Status**: Planned

**Goal**: Simplify adding new models and improve multi-modal support.

**Planned Features**:
- Document workflow to add new HF model to verl
- Better abstraction and registration system for multi-modal models
- Documentation page about latest status of model support
- Per-model related features (LoRA, sequence parallelism, megatron, etc)

---

### 6. High Quality Recipes and End-to-End Optimizations

**Status**: In Progress
**Related Issues**: [#2136](https://github.com/volcengine/verl/issues/2136)

**Planned Features**:
- ReTool recipe (code ready, in review)
- SOTA multimodal VLM RL recipe (call for contribution)
- Enhance DAPO recipe with larger models
- High training throughput scripts
- Community recipe contributions via RFC process

---

## Additional Ongoing Features

### DeepSeek 671B Optimizations
**Issue**: [#1033](https://github.com/volcengine/verl/issues/1033)
**Description**: verl+megatron development tracking for large MoE models

### NPU Support
**Issue**: [#2171](https://github.com/volcengine/verl/issues/2171)
**Description**: Features NPU will focus on supporting in Q3

---

## Breaking Changes

**Issue**: [#2270](https://github.com/volcengine/verl/issues/2270)
**Description**: List of breaking changes since v0.4

---

## Recent Major Updates (from README)

### 2026-01
- Recipe directory migrated to dedicated repository: `verl-recipe` (submodule)
- [#4795](https://github.com/volcengine/verl/pull/4795)
- Experimental features kept: `transfer_queue`, `fully_async_policy`, `one_step_off_policy`, `vla`

### 2025-12
- Mind Lab: GRPO LoRA training for trillion-parameter model on 64 H800

### 2025-10
- PyTorch Conference 2025 presentation

### 2025-08
- PyTorch Expert Exchange Webinar presentation

### 2025-07
- ReTool recipe fully open-sourced
- First verl meetup at ICML Vancouver

### 2025-06
- Megatron backend enables large MoE models (DeepSeek-671B, Qwen3-235B)

### 2025-03
- **DAPO**: Open-source SOTA RL algorithm achieving 50 points on AIME 2024
- v0.3.0.post1 release with ~1.4x speedup
- Doubao-1.5-pro release (OpenAI O1-level performance)

---

## Key Contributors

Roadmap tasks initiated by and credited to:
- @vermouth1992
- @SwordFaith
- @eric-haibin-lin

---

## Notes

- verl emphasizes **modularity** and **composability** as core design principles
- Strong focus on **FSDP2** migration and **async architecture**
- Active community involvement with RFC process for new features
- Production-ready with scaling to 671B parameters demonstrated
- Multi-modal and VLM support are key focus areas

---

**Sources**:
- GitHub: [volcengine/verl](https://github.com/volcengine/verl)
- Q3 Roadmap: [Issue #2388](https://github.com/volcengine/verl/issues/2388)
- Documentation: [verl.readthedocs.io](https://verl.readthedocs.io/)
