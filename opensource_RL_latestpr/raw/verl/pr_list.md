# PR List: volcengine/verl

**Timeframe**: 2025-2026 (last 12 months)
**Repository**: [volcengine/verl](https://github.com/volcengine/verl)
**Total Significant PRs**: 30+
**Keywords**: training-backend, parallel-strategies, rollout-inference, rl-algorithms, alignment, model-architecture, multimodal, performance-optimization, memory-optimization, agent-framework, tool-integration

---

## High Priority (Roadmap-Aligned Features)

| PR # | Title | Keywords | Roadmap | Link | Release |
|------|-------|----------|---------|------|---------|
| #2981 | Fully async training recipe | async-architecture, performance-optimization | ✓ | [link](https://github.com/volcengine/verl/pull/2981) | v0.6.1 |
| #4067 | Multi-turn and tool call support (fully_async_policy) | multi-turn-rl, tool-integration, agent-framework | ✓ | [link](https://github.com/volcengine/verl/pull/4067) | v0.7.0 |
| #4125 | Multi-turn and tool call support (part 2) | multi-turn-rl, tool-integration, agent-framework | ✓ | [link](https://github.com/volcengine/verl/pull/4125) | v0.7.0 |
| #4182 | Multi-turn and tool call support (part 3) | multi-turn-rl, tool-integration, agent-framework | ✓ | [link](https://github.com/volcengine/verl/pull/4182) | v0.7.0 |
| Multiple | FSDP2 migration and training optimizations | training-backend, parallel-strategies, performance-optimization | ✓ | [releases](https://github.com/volcengine/verl/releases) | v0.7.0 |
| #4211 | Workers with model engine architecture | training-backend, parallel-strategies | ✓ | [link](https://github.com/volcengine/verl/pull/4211) | v0.7.0 |
| #4213 | Workers with model engine (part 2) | training-backend, parallel-strategies | ✓ | [link](https://github.com/volcengine/verl/pull/4213) | v0.7.0 |
| #4233 | Dispatch tensordict with nested tensor | data-pipeline, performance-optimization | ✓ | [link](https://github.com/volcengine/verl/pull/4233) | v0.7.0 |

---

## Medium Priority (Major Feature Additions)

### Training Infrastructure & Backend

| PR # | Title | Keywords | Roadmap | Link | Release |
|------|-------|----------|---------|------|---------|
| Multiple | FSDP2 as default training backend | training-backend, parallel-strategies | | [releases](https://github.com/volcengine/verl/releases) | v0.7.0 |
| #4139 | Megatron: customized prefix for state dict keys | training-backend, parallel-strategies | | [link](https://github.com/volcengine/verl/pull/4139) | v0.7.0 |
| #4158 | Megatron: MoE FP16 training support | training-backend, parallel-strategies, model-architecture | | [link](https://github.com/volcengine/verl/pull/4158) | v0.7.0 |
| #4223 | Megatron: Full FP8 training support | training-backend, performance-optimization, quantization | | [link](https://github.com/volcengine/verl/pull/4223) | v0.7.0 |

### Rollout/Inference Engines

| PR # | Title | Keywords | Roadmap | Link | Release |
|------|-------|----------|---------|------|---------|
| #3519 | vLLM: Support blockwise FP8 rollout | rollout-inference, performance-optimization, quantization | | [link](https://github.com/volcengine/verl/pull/3519) | v0.7.0 |
| #4222 | vLLM: Blockwise FP8 rollout optimizations | rollout-inference, performance-optimization, quantization | | [link](https://github.com/volcengine/verl/pull/4222) | v0.7.0 |
| Multiple | SGLang: Complete process separation, native server mode | rollout-inference, agent-framework | ✓ | [PRs](https://github.com/volcengine/verl/pulls?q=is%3Apr+is%3Aclosed+sglang) | v0.6.x-v0.7.0 |
| Multiple | SGLang: Multi-node support | rollout-inference, scalability | ✓ | [PRs](https://github.com/volcengine/verl/pulls?q=is%3Apr+is%3Aclosed+sglang) | v0.6.x |
| Multiple | SGLang: Multimodal data optimization | rollout-inference, multimodal | ✓ | [PRs](https://github.com/volcengine/verl/pulls?q=is%3Apr+is%3Aclosed+sglang) | v0.7.0 |
| Multiple | SGLang: Sandbox fusion integration | tool-integration, rollout-inference | ✓ | [PRs](https://github.com/volcengine/verl/pulls?q=is%3Apr+is%3Aclosed+sglang) | v0.6.x |

### RL Algorithms

| PR # | Title | Keywords | Roadmap | Link | Release |
|------|-------|----------|---------|------|---------|
| Multiple | CISPO: Clipped IS-weight Policy Optimization | rl-algorithms, alignment | | [releases](https://github.com/volcengine/verl/releases) | v0.7.0 |
| Multiple | SAPO: Soft Adaptive Policy Optimization | rl-algorithms, alignment | | [releases](https://github.com/volcengine/verl/releases) | v0.7.0 |
| Multiple | New RL algorithms (beyond PPO/GRPO) | rl-algorithms, alignment | | [releases](https://github.com/volcengine/verl/releases) | v0.7.0 |

### Vision-Language Models

| PR # | Title | Keywords | Roadmap | Link | Release |
|------|-------|----------|---------|------|---------|
| #3838 | VLM support for model engine | model-architecture, multimodal | ✓ | [link](https://github.com/volcengine/verl/pull/3838) | v0.6.1 |
| #4186 | VLM support for SFT trainer | model-architecture, multimodal | ✓ | [link](https://github.com/volcengine/verl/pull/4186) | v0.7.0 |
| #4734 | VLM support for RL trainer | model-architecture, multimodal | ✓ | [link](https://github.com/volcengine/verl/pull/4734) | v0.7.0 |
| Multiple | Qwen3VL model support | model-architecture, multimodal | | [releases](https://github.com/volcengine/verl/releases) | v0.7.0 |
| Multiple | Video input support for VLMs | model-architecture, multimodal | | [releases](https://github.com/volcengine/verl/releases) | v0.7.0 |
| Multiple | Multimodal data fetch optimization | data-pipeline, multimodal | | [releases](https://github.com/volcengine/verl/releases) | v0.7.0 |

### Performance Optimization

| PR # | Title | Keywords | Roadmap | Link | Release |
|------|-------|----------|---------|------|---------|
| Multiple | Remove padding tokens (sequence packing) | performance-optimization, memory-optimization | | [releases](https://github.com/volcengine/verl/releases) | Ongoing |
| Multiple | Sequence packing for Llama, Mistral, Gemma | performance-optimization, memory-optimization | | [releases](https://github.com/volcengine/verl/releases) | Ongoing |

---

## Low Priority (Bug Fixes & Documentation)

### Bug Fixes

| PR # | Title | Keywords | Roadmap | Link | Release |
|------|-------|----------|---------|------|---------|
| #3861 | Fix: Missing offload parameters | memory-optimization, fault-tolerance | | [link](https://github.com/volcengine/verl/pull/3861) | v0.6.x |
| #4097 | Fix: Optimizer state issues | reproducibility, fault-tolerance | | [link](https://github.com/volcengine/verl/pull/4097) | v0.6.x |
| #4156 | Fix: Reproducibility problems | reproducibility, fault-tolerance | | [link](https://github.com/volcengine/verl/pull/4156) | v0.6.x |

### Documentation

| PR # | Title | Keywords | Roadmap | Link | Release |
|------|-------|----------|---------|------|---------|
| Multiple | Agent loop tutorials | agent-framework, documentation | | [PRs](https://github.com/volcengine/verl/pulls?q=is%3Apr+is%3Aclosed+doc) | v0.6.x-v0.7.0 |
| Multiple | Installation guide updates | documentation | | [PRs](https://github.com/volcengine/verl/pulls?q=is%3Apr+is%3Aclosed+doc) | v0.6.x-v0.7.0 |
| Multiple | Comprehensive documentation for new features | documentation | | [PRs](https://github.com/volcengine/verl/pulls?q=is%3Apr+is%3Aclosed+doc) | v0.6.x-v0.7.0 |

---

## Additional Notable Merged PRs

### Reward System

| PR # | Title | Keywords | Roadmap | Link | Release |
|------|-------|----------|---------|------|---------|
| #3679 | Reward model refactoring | rl-algorithms, alignment | | [link](https://github.com/volcengine/verl/pull/3679) | v0.6.x |
| #4107 | RateLimitedRewardLoopManager for API-based rewards | rl-algorithms, alignment, deployment | | [link](https://github.com/volcengine/verl/pull/4107) | v0.6.x |

---

## Roadmap Alignment Summary

### Implemented (✓)
- **FSDP2 Migration**: Complete migration to FSDP2 as default training backend
- **Async Architecture**: Fully async training recipe with 20-40% throughput gain
- **Multi-turn RL**: Comprehensive multi-turn and tool call support
- **VLM Support**: Full VLM support for model engine, SFT, and RL trainers
- **Model Engine Architecture**: Workers with model engine refactoring
- **TensorDict Dispatch**: Nested tensor support replacing padding

### In Progress
- **Megatron Optimizations**: Ongoing enhancements for large MoE models
- **Performance Tuning**: Sequence packing and memory efficiency improvements
- **SGLang Integration**: Continuous improvements for rollout workers

### Not Started
- **Torchtitan Integration**: Call for contribution (from Q3 roadmap)
- **Distributed Data Pool**: Persistable replay buffer for large-scale rollout data (#2539)

---

## Release Timeline

| Version | Date | Key Features |
|---------|------|--------------|
| v0.7.0 | 2025-11-13 | FSDP2 default, multi-turn RL, VLM support, CISPO/SAPO, FP8 support |
| v0.6.1 | 2025-04 | Fully async training, VLM support for model engine |
| v0.3.0.post1 | 2025-03 | ~1.4x speedup, DAPO support |

---

## Keyword Distribution

| Category | Count | PRs |
|----------|-------|-----|
| Training Infrastructure | 8 | FSDP2, Megatron, model engine |
| Rollout/Inference | 6 | vLLM FP8, SGLang enhancements |
| RL Algorithms | 3 | CISPO, SAPO, new algorithms |
| VLM/Multimodal | 6 | VLM support, Qwen3VL, video input |
| Multi-turn/Agent | 4 | Multi-turn RL, tool call support |
| Performance | 4 | Sequence packing, async architecture |
| Reward System | 2 | Reward model refactoring |
| Bug Fixes | 3 | Memory, optimizer, reproducibility |
| Documentation | Multiple | Tutorials, guides |

---

## Notes

- All roadmap-aligned features from Q3 roadmap have been implemented or are in progress
- Strong focus on FSDP2 migration and async architecture throughout 2025
- VLM and multi-modal support are major development areas
- Performance optimization is a consistent theme (sequence packing, FP8, async)
- Production-ready with comprehensive testing and bug fixes

---

**Next Step**: Proceed to Step 4 - Raw PR Collection
