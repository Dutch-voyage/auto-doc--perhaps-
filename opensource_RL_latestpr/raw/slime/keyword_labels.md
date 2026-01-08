# slime Keyword Labels

**Repository**: THUDM/slime
**Assigned**: 2026-01-08
**Source**: task/global_keywords.md

---

## Assigned Keywords (from Global Pool)

### 1. Training Infrastructure
- ✅ **training-backend** - Core training systems (Megatron, FSDP, XTuner backends)
- ✅ **parallel-strategies** - Distributed training (TP, PP, EP, CP, FSDP, PD-disaggregation)
- ✅ **rollout-inference** - SGLang integration for data generation

### 2. RL Algorithms
- ✅ **rl-algorithms** - PPO, GSPO, TIS, Reinforce++, DPO support
- ✅ **alignment** - RLHF and preference optimization capabilities
- ✅ **verifier-guidance** - Reward models and verification-based training

### 3. Model Architecture
- ✅ **model-architecture** - Support for multiple model families (Qwen, DeepSeek, Llama)
- ✅ **multimodal** - VLM support (Qwen3-VL, Qwen2.5-VL)
- ✅ **quantization** - FP8 training/inference, Int4 QAT (in development)

### 4. Performance & Optimization
- ✅ **performance-optimization** - Speed improvements, CUDA graphs, speculative decoding
- ✅ **memory-optimization** - Offload strategies, memory-efficient training
- ✅ **communication-optimization** - Weight update optimization, distributed post

### 5. Data Pipeline
- ✅ **data-pipeline** - Custom data generation interfaces
- ✅ **experience-replay** - Routing Replay (R3, R2), rollout buffer
- ✅ **synthetic-data** - Procedural data generation capabilities

### 6. Evaluation & Testing
- ✅ **evaluation** - Benchmarking support (tau-bench, terminal bench)
- ✅ **reproducibility** - Deterministic rollout, fault tolerance
- ✅ **monitoring** - Training metrics and debugging capabilities

### 7. Agent & Tool Use
- ✅ **agent-framework** - Agentic RL training, multi-agent scenarios
- ✅ **tool-integration** - Tool call support, function calling
- ✅ **multi-agent** - Multi-agent training examples and support

### 8. Deployment & Production
- ✅ **deployment** - Production serving capabilities
- ✅ **fault-tolerance** - Fault tolerance for rollout engines
- ✅ **scalability** - Large-scale distributed training

---

## Rationale for Assignments

### Core Competencies (Primary Focus)
1. **Training Infrastructure** - slime's primary value proposition is connecting Megatron with SGLang for high-performance training
2. **Performance & Optimization** - Heavy emphasis on FP8, speculative decoding, memory optimization
3. **Scalability** - Designed for large-scale distributed training (powers GLM-4.5/4.6)

### Emerging Capabilities
1. **Multimodal** - Rapid development of VLM support (true on-policy training)
2. **Agent & Tool Use** - Growing support for agentic RL and tool integration
3. **Quantization** - Active development on Int4 QAT and FP8 optimizations

### Production Readiness
1. **Fault Tolerance** - Robustness features for production deployment
2. **Reproducibility** - Deterministic training capabilities
3. **Evaluation** - Comprehensive benchmarking integration

---

## Keyword-Specific Evidence

### training-backend
**Evidence**:
- FSDP backend (v0.2.0)
- Megatron integration
- XTuner backend support
- PRs: #282, #310, #342

### parallel-strategies
**Evidence**:
- All parallel strategies supported (TP, PP, EP, CP)
- PD-disaggregation (v0.2.1, PR #1080)
- FSDP integration

### multimodal
**Evidence**:
- VLM + FSDP integration (v0.2.1)
- Qwen3-VL, Qwen2.5-VL support
- True on-policy VLM training
- PRs: #501, #1056, #1079, #1210

### rl-algorithms
**Evidence**:
- PPO support (v0.2.0)
- GSPO, TIS, Reinforce++
- Off-policy sequence masking (DeepSeek v3.2)
- PRs: #342, #347, #999, #1004

### agent-framework
**Evidence**:
- Multi-agent RL examples
- Tool call support
- Strands-agents integration
- PRs: #269, #1159, #1359

### quantization
**Evidence**:
- FP8 full stack (v0.2.0)
- Int4 QAT support (PR #1172)
- FP8 weight updates

### fault-tolerance
**Evidence**:
- Rollout engine fault tolerance
- Deterministic rollout (v0.2.0)
- Fault tolerance improvements (PR #1311)

---

## Unique Keywords (slime-Specific)

None - all keywords mapped from global pool

---

## New Keyword Proposals

No new keywords proposed at this time.

**Rationale**: The existing global keyword taxonomy (8 primary categories, 24 keywords) comprehensively covers slime's capabilities.

---

## Cross-Repository Comparisons

### Similar Frameworks
- **veRL**: Similar training backend and algorithm support
- **OpenRLHF**: Overlap in RL algorithms (PPO, DPO)
- **mbridge**: Shared focus on performance optimization

### Differentiators
- **Unique**: SGLang + Megatron integration
- **Unique**: True on-policy VLM training with FSDP
- **Unique**: Python-based router for accessibility
- **Strong**: Production deployment experience (GLM-4.5/4.6)

---

## Priority Rankings

### High Priority (Active Development)
1. **multimodal** - Rapid VLM feature development
2. **quantization** - Int4 QAT, FP8 optimizations
3. **agent-framework** - Tool use and multi-agent support
4. **training-backend** - FSDP enhancements

### Medium Priority (Stable Features)
1. **rl-algorithms** - Core algorithms mature
2. **performance-optimization** - Continuous improvements
3. **fault-tolerance** - Production hardening

### Low Priority (Maintenance)
1. **data-pipeline** - Stable functionality
2. **evaluation** - Incremental additions

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-08 | Initial keyword assignment |

---

**Next Step**: Proceed to PR search and filtering (Step 3)
