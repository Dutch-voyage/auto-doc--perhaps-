# ROLL Keyword Labels

**Repository**: [alibaba/ROLL](https://github.com/alibaba/ROLL)
**Analysis Date**: 2026-01-08

---

## Assigned Keywords (from global taxonomy)

### Training Infrastructure
- **training-backend** ✅
  - **Rationale**: Supports Megatron-LM (mcore-adapter), DeepSpeed (ZeRO), FSDP (planned)
  - **Evidence**: README mentions "Training supports DeepSpeed (ZeRO), Megatron-LM 5D parallelism"

- **parallel-strategies** ✅
  - **Rationale**: 5D parallelism (dp/tp/pp/cp/ep) via Megatron-Core
  - **Evidence**: README mentions "Megatron-LM 5D parallelism (mcore-adapter, dp/tp/pp/cp/ep)"

- **rollout-inference** ✅
  - **Rationale**: Supports vLLM and SGLang for rollout generation
  - **Evidence**: README mentions "Inference/Generation supports vLLM, SGLang"

### RL Algorithms
- **rl-algorithms** ✅
  - **Rationale**: 20+ RL algorithms including PPO, GRPO, Reinforce++, TOPR, RAFT++, GSPO
  - **Evidence**: README lists "PPO, GRPO, Reinforce++, TOPR, RAFT++, GSPO"

- **alignment** ✅
  - **Rationale**: Supports RLHF, DPO, and reward-based training
  - **Evidence**: README mentions "RLHF training capabilities" and "DPO Pipeline"

- **verifier-guidance** ✅
  - **Rationale**: LLM-as-judge and reward model support
  - **Evidence**: README mentions "FP8 inference for LLM as judge"

### Model Architecture
- **model-architecture** ✅
  - **Rationale**: Supports Qwen3, Qwen3-MoE, Qwen2.5, Qwen3-VL, DeepSeek V3 (planned)
  - **Evidence**: README lists extensive model family support

- **multimodal** ✅
  - **Rationale**: Strong VLM support (Qwen3-VL), Agentic RL for VLM
  - **Evidence**: README mentions "Agentic RL LLM & VLM", "RLVR LLM & VLM"

- **quantization** ✅
  - **Rationale**: FP8 rollout support, FP8 inference for LLM-as-judge
  - **Evidence**: README mentions "FP8 rollout (FP8 inference for LLM as judge)"

### Performance & Optimization
- **performance-optimization** ✅
  - **Rationale**: Sequence packing, beam search, reference logprob caching
  - **Evidence**: v0.1.3 release mentions "sequence packing", "vLLM beam_search"

- **memory-optimization** ✅
  - **Rationale**: NCCL offload, LoRA training support
  - **Evidence**: v0.1.3 mentions "offload nccl to save gpu memory"

- **communication-optimization** ✅
  - **Rationale**: Asynchronous parallel rollout, distributed training
  - **Evidence**: README mentions "sample-level asynchronous parallel Rollout"

### Data Pipeline
- **data-pipeline** ✅
  - **Rationale**: Multi-domain RLVR with flexible domain_batch_size
  - **Evidence**: README mentions "Flexible `domain_batch_size` distribution control"

### Evaluation & Testing
- **monitoring** ✅
  - **Rationale**: Integrated with SwanLab/WandB/TensorBoard
  - **Evidence**: README mentions "Observability: Integrated with SwanLab / WandB / TensorBoard"

### Agent & Tool Use
- **agent-framework** ✅
  - **Rationale**: Agentic RL with multi-turn interaction, tool use
  - **Evidence**: README mentions "Agentic RL: Multi-turn interaction capabilities for... tool use"

- **tool-integration** ✅
  - **Rationale**: GEM environment alignment for tool use training
  - **Evidence**: News (09/23/2025) mentions "aligns with GEM environment definition"

### Deployment & Production
- **deployment** ✅
  - **Rationale**: Docker support for AMD GPUs, Ascend NPU
  - **Evidence**: README mentions "AMD GPUs with out-of-box image docker"

- **scalability** ✅
  - **Rationale**: Ray-based multi-role distributed architecture
  - **Evidence**: README mentions "Ray-based multi-role distributed architecture"

---

## Keyword Summary (for quick reference)

```
roll: training-backend, parallel-strategies, rollout-inference,
      rl-algorithms, alignment, verifier-guidance,
      model-architecture, multimodal, quantization,
      performance-optimization, memory-optimization, communication-optimization,
      data-pipeline,
      monitoring,
      agent-framework, tool-integration,
      deployment, scalability
```

**Total Keywords**: 17 out of 24 global categories

**Missing Keywords** (not applicable to ROLL):
- `experience-replay` - No explicit replay buffer mentioned
- `synthetic-data` - No synthetic data generation focus
- `evaluation` - Not a primary focus (though monitoring is supported)
- `reproducibility` - Not explicitly emphasized
- `fault-tolerance` - Not explicitly emphasized
- `multi-agent` - Single agent focus (though agentic RL supports multi-turn)

---

## Repository-Specific Labels

### ROLL-Unique Features (not in global taxonomy)

**Ray-Based Architecture**
- Multi-role distributed system
- Flexible resource allocation
- Heterogeneous task scheduling

**Asynchronous Training**
- Async parallel rollout (RLVR)
- Async training (Agentic)
- Dynamic sampling

**AutoDeviceMapping**
- Custom device mapping per role
- Colocated and disaggregated deployment support

**Domain-Specific Training**
- Multi-task RLVR (math, coding, reasoning, etc.)
- Per-domain tracking and metrics

---

## Keyword Assignment Rationale

ROLL is positioned as a **comprehensive RL training framework** similar to slime, with:
- Strong focus on **agentic RL** and **multi-turn interactions**
- Excellent **VLM support** for RL training
- Production-ready **deployment options** (Docker, AMD, Ascend)
- Flexible **backend abstraction** supporting multiple training engines

Compared to slime:
- **Similar breadth**: Supports most major keywords
- **Differentiating focus**: Agentic RL > VLM RL training > User-friendly API
- **Research alignment**: Strong paper publication track record

---

**Analysis Complete**: 2026-01-08
