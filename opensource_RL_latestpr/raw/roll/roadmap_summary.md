# ROLL Roadmap Summary

**Repository**: [alibaba/ROLL](https://github.com/alibaba/ROLL)
**Analysis Date**: 2026-01-08
**Latest Release**: v0.1.3 (2025-12-08)

---

## Official Roadmap Items

### Upcoming Features (from README)

#### 1. Async RLVR Pipeline
- **Status**: Planned/Under Development
- **Description**: For even more efficient and streamlined asynchronous operations
- **Timeline**: TBD

#### 2. FSDP2 Integration
- **Status**: Planned
- **Description**: Integrating the latest Fully Sharded Data Parallel techniques
- **Timeline**: TBD
- **Note**: Currently supports DeepSpeed (ZeRO), Megatron-LM 5D parallelism, FSDP "under implementation"

#### 3. DeepSeek V3 Support
- **Status**: Planned
- **Description**: Adding compatibility for the newest Deepseek models
- **Timeline**: TBD

---

## Recent Development Directions (Inferred from News/Releases)

### v0.1.3 Release Highlights (2025-12-08)

**Major Features Added:**
- Qwen3VL support with mcore_adapter and examples
- vLLM beam search support
- Qwen-3-next AMD GPU support
- SGLang 0.5.4, vLLM 0.11.1, PyTorch 2.8.0 support
- Sequence packing for SFT and Distill pipelines

**Agentic RL Enhancements:**
- Agentic-spec actor worker
- Agentic validation improvements
- Agentic normalization refactoring (like LitePPO)
- Agentic profile metrics

**Model & Backend Updates:**
- NCCL offload support for GPU memory savings
- SGLang DP-attention support
- Enable reference option (#250)
- Enable old_logprobs optimization via cache

**Bug Fixes:**
- Math rule reward worker updates with thinking (#281)
- Various fixes for tokenizer, vLLM, SGLang compatibility

---

## Strategic Development Themes

### 1. Multi-Modal Expansion
- Heavy investment in VLM capabilities
- Qwen3-VL support with full examples
- Agentic VLM training (RLVR + Agentic)

### 2. Hardware Ecosystem Support
- AMD GPU support (docker + examples)
- Ascend NPU support (announced 2025-09-28)
- PyTorch 2.8.0 compatibility

### 3. Performance Optimization
- Sequence packing for memory efficiency
- Reference logprob caching
- NCCL offload for GPU memory savings
- Beam search support in vLLM

### 4. Production Readiness
- Continuous bug fixes and compatibility updates
- Docker support for multiple hardware platforms
- Validation improvements across pipelines

---

## Research Paper Releases (indicating research focus)

### Recent Papers (2025)
1. **"Let It Flow: Agentic Crafting on Rock and Roll"** (01/01/2026)
   - Introduces ALE ecosystem and ROME
   - Novel IPA algorithm

2. **"AMAP Agentic Planning Technical Report"** (01/01/2026)

3. **"Asymmetric Proximal Policy Optimization"** (10/23/2025)
   - Mini-critics boost LLM reasoning

4. **"Attention Illuminates LLM Reasoning"** (10/23/2025)
   - Preplan-and-Anchor Rhythm for fine-grained policy optimization

5. **"ROLL Flash Part II"** (10/14/2025)
   - Accelerating RLVR and Agentic Training with Asynchrony

6. **"RollPacker"** (09/25/2025)
   - Mitigating Long-Tail Rollouts for fast, synchronous RL post-training

7. **"Tricks or Traps? A Deep Dive into RL for LLM Reasoning"** (08/11/2025)
   - Part I technical deep dive

8. **"Reinforcement Learning Optimization for Large-Scale Learning"** (06/09/2025)
   - Technical report (arXiv:2506.06122)

---

## Key Infrastructure Investments

### Backend Support
- **Megatron-LM**: 5D parallelism (dp/tp/pp/cp/ep) via mcore-adapter
- **DeepSpeed**: ZeRO optimization
- **vLLM**: Inference engine with beam search
- **SGLang**: Rollout engine with DP-attention
- **FSDP**: Planned (FSDP2 on roadmap)

### Model Family Support
- **Qwen**: Qwen3, Qwen3-Next, Qwen3-MoE, Qwen3-VL, Qwen2.5
- **DeepSeek**: V3, V3.1 (planned)
- **Llama**: Supported (inferred from docs)

### Algorithm Support
- PPO, Lite PPO, GRPO, GSPO
- Reinforce++, TOPR, RAFT++, StarPO
- RewardFL
- GiGPO (stepwise agentic learning)

---

## Sources

- **Repository**: https://github.com/alibaba/ROLL
- **Documentation**: https://alibaba.github.io/ROLL/
- **Releases**: https://github.com/alibaba/ROLL/releases
- **Technical Report**: https://arxiv.org/abs/2506.06122
- **Latest Release (v0.1.3)**: https://github.com/alibaba/ROLL/releases/tag/v0.1.3

---

**Analysis Complete**: 2026-01-08
**Next Review**: 2026-02-08
