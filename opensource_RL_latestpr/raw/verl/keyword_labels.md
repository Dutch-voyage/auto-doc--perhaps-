# verl Keyword Labels

**Last Updated**: 2026-01-08
**Repository**: [volcengine/verl](https://github.com/volcengine/verl)
**Based on**: `task/global_keywords.md` v1.0

---

## Assigned Keywords

### 1. Training Infrastructure

| Keyword | Assigned | Rationale |
|---------|----------|-----------|
| `training-backend` | ✓ | Supports FSDP, FSDP2, Megatron-LM as training backends. Core architectural component. |
| `parallel-strategies` | ✓ | Implements tensor parallelism, pipeline parallelism, data parallelism, expert parallelism, sequence parallelism (DeepSpeed Ulysses). |
| `rollout-inference` | ✓ | Integrates vLLM, SGLang, HF Transformers for rollout generation. Key architectural component. |

**Relevant Terms**: backend, trainer, engine, distributed, sharding, parallelism, serving, inference, rollout

---

### 2. RL Algorithms

| Keyword | Assigned | Rationale |
|---------|----------|-----------|
| `rl-algorithms` | ✓ | Implements multiple RL algorithms: PPO, GRPO, GSPO, ReMax, REINFORCE++, RLOO, PRIME, DAPO, DrGRPO, KL_Cov, Clip_Cov, PF-PPO, VAPO. |
| `alignment` | ✓ | RLHF/RLAIF framework for model alignment with human feedback and preference optimization. |
| `verifier-guidance` | ✓ | Supports model-based reward and function-based reward (verifiable reward) for math and coding tasks. |

**Relevant Terms**: optimization, policy, reward, safety, preference optimization, search, verification, reward models

---

### 3. Model Architecture

| Keyword | Assigned | Rationale |
|---------|----------|-----------|
| `model-architecture` | ✓ | Compatible with Qwen-3, Qwen-2.5, Llama3.1, Gemma2, DeepSeek-LLM, DeepSeek-671B, Qwen3-235B, Kimi-VL. Supports dense and MoE architectures. |
| `multimodal` | ✓ | Supports vision-language models (VLMs) and multi-modal RL with Qwen2.5-vl, Kimi-VL. |
| `quantization` | ○ | Not explicitly mentioned in README, but likely supported through underlying frameworks (FSDP, vLLM, etc). |

**Relevant Terms**: architecture, model family, VLM, vision, cross-modal, compression, sparsity, pruning

---

### 4. Performance & Optimization

| Keyword | Assigned | Rationale |
|---------|----------|-----------|
| `performance-optimization` | ✓ | SOTA throughput with 3D-HybridEngine, eliminates memory redundancy, reduces communication overhead. ~1.4x speedup in v0.3.0.post1. |
| `memory-optimization` | ✓ | Efficient actor model resharding, LoRA support for memory savings, FSDP CPU offloading compatible with gradient accumulation. |
| `communication-optimization` | ✓ | 3D-HybridEngine reduces communication overhead during training/generation transitions. |

**Relevant Terms**: optimization, acceleration, memory, VRAM, host memory, communication, bandwidth, latency

---

### 5. Data Pipeline

| Keyword | Assigned | Rationale |
|---------|----------|-----------|
| `data-pipeline` | ✓ | Handles data generation, processing, and management for RL training. Supports multi-turn messages and dense rewards. |
| `experience-replay` | ○ | PF-PPO includes replay buffer. Q3 roadmap mentions distributed data pool for large-scale rollout data storage ([#2539](https://github.com/volcengine/verl/pull/2539)). |
| `synthetic-data` | ○ | Not explicitly mentioned, but may be used for training. |

**Relevant Terms**: data, dataset, preprocessing, buffer, storage, replay, synthetic, procedural, generated

---

### 6. Evaluation & Testing

| Keyword | Assigned | Rationale |
|---------|----------|-----------|
| `evaluation` | ✓ | RL performance on coding, math benchmarks. DAPO achieves 50 points on AIME 2024. Doubao-1.5-pro reaches OpenAI O1-level performance. |
| `reproducibility` | ✓ | Reproducible algorithm baselines for coding and math tasks. |
| `monitoring` | ✓ | Experiment tracking with wandb, swanlab, mlflow, tensorboard. |

**Relevant Terms**: benchmark, metrics, testing, deterministic, reproducible, stable, observability, debugging, profiling

---

### 7. Agent & Tool Use

| Keyword | Assigned | Rationale |
|---------|----------|-----------|
| `agent-framework` | ✓ | Agent RL infrastructure for multi-turn rollout and agent loop. Q3 roadmap emphasizes agentic RL. |
| `tool-integration` | ✓ | Multi-turn with tool calling, search tool integration, sandbox fusion integration. |
| `multi-agent` | ○ | Not explicitly mentioned, but multi-turn rollout and agent infrastructure suggests potential support. |

**Relevant Terms**: agents, tool use, autonomous, tools, APIs, external systems, multi-agent, coordination, collaboration

---

### 8. Deployment & Production

| Keyword | Assigned | Rationale |
|---------|----------|-----------|
| `deployment` | ✓ | Production-ready RL training library. Used by Bytedance for Doubao-1.5-pro (70.0 pass@1 on AIME). Deployment on AWS SageMaker supported. |
| `fault-tolerance` | ○ | Not explicitly mentioned, but production deployment suggests fault tolerance considerations. |
| `scalability` | ✓ | Scales up to 671B models and hundreds of GPUs with expert parallelism. Flexible device mapping for different cluster sizes. |

**Relevant Terms**: serving, production, deployment, resilience, robustness, reliability, scale, distributed, cluster

---

## Legend

- ✓ **Assigned**: Keyword is relevant and applies to this repository
- ○ **Potential**: Keyword may apply but needs verification
- [blank] **Not Applicable**: Keyword does not apply to this repository

---

## New Keyword Proposals

### Proposed: `async-architecture`
**Category**: Training Infrastructure
**Rationale**: Q3 roadmap emphasizes "one-step off async pipeline" and "fully-async pipeline" as key architectural features. Async/disaggregated architecture is a major development direction.
**Related Terms**: async, disaggregated, pipeline, streaming, partial rollout

### Proposed: `multi-turn-rl`
**Category**: Agent & Tool Use
**Rationale**: Multi-turn RL is a key focus area for verl, with dedicated roadmap items for multi-turn rollout and agentic RL. This is distinct from general agent-framework.
**Related Terms**: multi-turn, conversation, context, dialogue

**Status**: Pending review and addition to `global_keywords.md`

---

## Summary

**Total Keywords Assigned**: 17 out of 24
**Primary Strengths**: Training infrastructure, RL algorithms, performance optimization, VLM support
**Unique Features**: 3D-HybridEngine, async architecture, multi-turn agentic RL, 671B model support
**Production Readiness**: High - used by Bytedance for production models

---

## Keyword Usage for PR Search

When searching for PRs, use the following query patterns:

```
is:pr is:merged repo:volcengine/verl FSDP
is:pr is:merged repo:volcengine/verl Megatron
is:pr is:merged repo:volcengine/verl vLLM
is:pr is:merged repo:volcengine/verl SGLang
is:pr is:merged repo:volcengine/verl PPO
is:pr is:merged repo:volcengine/verl GRPO
is:pr is:merged repo:volcengine/verl DAPO
is:pr is:merged repo:volcengine/verl VLM
is:pr is:merged repo:volcengine/verl multi-turn
is:pr is:merged repo:volcengine/verl async
is:pr is:merged repo:volcengine/verl agent
```

---

**Next Step**: Proceed to Step 3 - PR Search & Filtering
