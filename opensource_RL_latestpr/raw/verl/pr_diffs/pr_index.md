# PR Index: volcengine/verl

**Last Updated**: 2026-01-08
**Repository**: [volcengine/verl](https://github.com/volcengine/verl)
**Directory**: `pr_diffs/`
**Total PRs Documented**: 30+

---

## Index Structure

```
pr_diffs/
├── pr_index.md (this file)
├── training_backend/
│   ├── fsdp2_migration.md
│   ├── megatron_optimizations.md
│   └── model_engine.md
├── rollout_inference/
│   ├── vllm_fp8.md
│   └── sglang_enhancements.md
├── rl_algorithms/
│   ├── ciso_sapo.md
│   └── reward_system.md
├── vlm_multimodal/
│   └── vlm_support.md
├── multi_turn_agent/
│   └── multi_turn_tool_support.md
└── performance/
    └── optimizations.md
```

---

## High Priority PRs

### #2981: Fully async training recipe

**Title**: Fully async training recipe
**PR Number**: #2981
**Link**: [https://github.com/volcengine/verl/pull/2981](https://github.com/volcengine/verl/pull/2981)
**Status**: Merged
**Release**: v0.6.1 (April 2025)
**Priority**: High (Roadmap-Aligned)
**Keywords**: async-architecture, performance-optimization, training-backend

**Description**:
- Fully asynchronous PPO training system
- Complete decoupling of Trainer and Rollouter
- Asynchronous sample generation and training
- 20-40% throughput gain
- Addresses Q3 roadmap: "one-step off async pipeline"

**Files Affected**: Training infrastructure, rollout workers, recipe files

**Breaking Changes**: None documented

**Dependencies**: None

---

### #4067, #4125, #4182: Multi-turn and tool call support

**Title**: Multi-turn and tool call support for recipe/fully_async_policy
**PR Numbers**: #4067, #4125, #4182
**Links**: [#4067](https://github.com/volcengine/verl/pull/4067), [#4125](https://github.com/volcengine/verl/pull/4125), [#4182](https://github.com/volcengine/verl/pull/4182)
**Status**: Merged
**Release**: v0.7.0 (November 2025)
**Priority**: High (Roadmap-Aligned)
**Keywords**: multi-turn-rl, tool-integration, agent-framework

**Description**:
- Multi-turn conversation support
- Tool calling capabilities
- Dynamic conversational feedback
- Iterative problem-solving scenarios
- Addresses Q3 roadmap: "Agent RL infrastructure"

**Files Affected**: Recipe files, agent infrastructure, tool integration

**Breaking Changes**: None documented

**Dependencies**: Fully async architecture (#2981)

---

### FSDP2 Migration (Multiple PRs)

**Title**: FSDP2 and training optimizations
**PR Numbers**: Multiple
**Link**: [Release Notes](https://github.com/volcengine/verl/releases)
**Status**: Merged
**Release**: v0.7.0 (November 13, 2025)
**Priority**: High (Roadmap-Aligned)
**Keywords**: training-backend, parallel-strategies, performance-optimization

**Description**:
- Complete migration to FSDP2 as default training backend
- Better throughput and memory usage
- Composable with other features (torch.compile)
- CPU offloading support
- Addresses Q3 roadmap: "switch all recipe/examples from fsdp1 to fsdp2"

**Files Affected**: Training backend, FSDP implementation, examples

**Breaking Changes**: Migration from FSDP1 to FSDP2

**Dependencies**: PyTorch FSDP2

---

### #4211, #4213, #4233: Model Engine Architecture

**Title**: Workers with model engine and dispatch tensordict
**PR Numbers**: #4211, #4213, #4233
**Links**: [#4211](https://github.com/volcengine/verl/pull/4211), [#4213](https://github.com/volcengine/verl/pull/4213), [#4233](https://github.com/volcengine/verl/pull/4233)
**Status**: Merged
**Release**: v0.7.0 (November 2025)
**Priority**: High (Roadmap-Aligned)
**Keywords**: training-backend, parallel-strategies, data-pipeline

**Description**:
- Refactoring workers with model engine architecture
- Supporting tensordict dispatch
- Nested tensor support replacing padding
- Colocate replicas support
- Addresses Q3 roadmap: "composable model engines"

**Files Affected**: Worker implementation, model engine, data pipeline

**Breaking Changes**: None documented

**Dependencies**: None

---

## Medium Priority PRs

### Training Infrastructure & Backend

#### #4139: Megatron customized prefix for state dict keys

**Title**: Megatron: customized prefix for state dict keys
**PR Number**: #4139
**Link**: [https://github.com/volcengine/verl/pull/4139](https://github.com/volcengine/verl/pull/4139)
**Status**: Merged
**Release**: v0.7.0
**Priority**: Medium
**Keywords**: training-backend, parallel-strategies

**Description**: Customized prefix for state dict keys in Megatron backend

**Files Affected**: Megatron backend

**Breaking Changes**: None documented

---

#### #4158: Megatron MoE FP16 training support

**Title**: Megatron: MoE FP16 training support
**PR Number**: #4158
**Link**: [https://github.com/volcengine/verl/pull/4158](https://github.com/volcengine/verl/pull/4158)
**Status**: Merged
**Release**: v0.7.0
**Priority**: Medium
**Keywords**: training-backend, parallel-strategies, model-architecture

**Description**: MoE FP16 training support for Megatron backend

**Files Affected**: Megatron backend

**Breaking Changes**: None documented

---

#### #4223: Megatron Full FP8 training support

**Title**: Megatron: Full FP8 training support
**PR Number**: #4223
**Link**: [https://github.com/volcengine/verl/pull/4223](https://github.com/volcengine/verl/pull/4223)
**Status**: Merged
**Release**: v0.7.0
**Priority**: Medium
**Keywords**: training-backend, performance-optimization, quantization

**Description**: Full FP8 training support for Megatron backend

**Files Affected**: Megatron backend

**Breaking Changes**: None documented

---

### Rollout/Inference Engines

#### #3519, #4222: vLLM Blockwise FP8 rollout

**Title**: vLLM: Support blockwise FP8 rollout
**PR Numbers**: #3519, #4222
**Links**: [#3519](https://github.com/volcengine/verl/pull/3519), [#4222](https://github.com/volcengine/verl/pull/4222)
**Status**: Merged
**Release**: v0.7.0
**Priority**: Medium
**Keywords**: rollout-inference, performance-optimization, quantization

**Description**:
- Blockwise FP8 inference in vLLM rollouts
- Performance optimizations for MoE RL models

**Files Affected**: vLLM rollout worker

**Breaking Changes**: None documented

---

### SGLang Enhancements (Multiple PRs)

**Title**: SGLang rollout enhancements
**PR Numbers**: Multiple
**Link**: [SGLang PRs](https://github.com/volcengine/verl/pulls?q=is%3Apr+is%3Aclosed+sglang)
**Status**: Merged
**Release**: v0.6.x-v0.7.0
**Priority**: Medium
**Keywords**: rollout-inference, agent-framework, tool-integration

**Description**:
- Complete separation of SGLang process from trainer process
- Migration to native server mode
- Multi-node support
- Multimodal data optimization
- Sandbox fusion integration
- Addresses Q3 roadmap: "modular rollout workers"

**Files Affected**: SGLang rollout worker, agent infrastructure

**Breaking Changes**: None documented

---

### RL Algorithms

#### CISPO & SAPO

**Title**: CISPO: Clipped IS-weight Policy Optimization, SAPO: Soft Adaptive Policy Optimization
**PR Numbers**: Multiple
**Link**: [Release Notes](https://github.com/volcengine/verl/releases)
**Status**: Merged
**Release**: v0.7.0 (November 13, 2025)
**Priority**: Medium
**Keywords**: rl-algorithms, alignment

**Description**: Addition of new RL algorithms expanding beyond PPO and GRPO

**Files Affected**: RL algorithm implementations

**Breaking Changes**: None documented

---

### Vision-Language Models

#### #3838, #4186, #4734: VLM Support

**Title**: VLM support for model engine, SFT and RL trainer
**PR Numbers**: #3838, #4186, #4734
**Links**: [#3838](https://github.com/volcengine/verl/pull/3838), [#4186](https://github.com/volcengine/verl/pull/4186), [#4734](https://github.com/volcengine/verl/pull/4734)
**Status**: Merged
**Release**: v0.6.1-v0.7.0
**Priority**: Medium
**Keywords**: model-architecture, multimodal

**Description**:
- Comprehensive VLM support
- Qwen3VL models
- Multimodal data fetch optimization
- Video input support
- Model engine integration

**Files Affected**: Model engine, SFT trainer, RL trainer

**Breaking Changes**: None documented

---

### Performance Optimization

#### Sequence Packing (Multiple PRs)

**Title**: Remove padding tokens (sequence packing)
**PR Numbers**: Multiple
**Link**: [Release Notes](https://github.com/volcengine/verl/releases)
**Status**: Ongoing
**Release**: Throughout 2025
**Priority**: Medium
**Keywords**: performance-optimization, memory-optimization

**Description**:
- Significant throughput increase
- Sequence packing for Llama, Mistral, Gemma models
- Memory efficiency improvements

**Files Affected**: Data pipeline, training loops

**Breaking Changes**: None documented

---

## Low Priority PRs

### Bug Fixes

#### #3861: Missing offload parameters

**Title**: Fix: Missing offload parameters
**PR Number**: #3861
**Link**: [https://github.com/volcengine/verl/pull/3861](https://github.com/volcengine/verl/pull/3861)
**Status**: Merged
**Release**: v0.6.x
**Priority**: Low
**Keywords**: memory-optimization, fault-tolerance

**Description**: Fix for missing offload parameters

---

#### #4097: Optimizer state issues

**Title**: Fix: Optimizer state issues
**PR Number**: #4097
**Link**: [https://github.com/volcengine/verl/pull/4097](https://github.com/volcengine/verl/pull/4097)
**Status**: Merged
**Release**: v0.6.x
**Priority**: Low
**Keywords**: reproducibility, fault-tolerance

**Description**: Fix for optimizer state issues

---

#### #4156: Reproducibility problems

**Title**: Fix: Reproducibility problems
**PR Number**: #4156
**Link**: [https://github.com/volcengine/verl/pull/4156](https://github.com/volcengine/verl/pull/4156)
**Status**: Merged
**Release**: v0.6.x
**Priority**: Low
**Keywords**: reproducibility, fault-tolerance

**Description**: Fix for reproducibility problems

---

### Documentation

#### Multiple: Documentation updates

**Title**: Documentation updates and examples
**PR Numbers**: Multiple
**Link**: [Documentation PRs](https://github.com/volcengine/verl/pulls?q=is%3Apr+is%3Aclosed+doc)
**Status**: Merged
**Release**: v0.6.x-v0.7.0
**Priority**: Low
**Keywords**: documentation

**Description**:
- Agent loop tutorials
- Installation guide updates
- Comprehensive documentation for new features

---

## Additional Notable PRs

### Reward System

#### #3679: Reward model refactoring

**Title**: Reward model refactoring
**PR Number**: #3679
**Link**: [https://github.com/volcengine/verl/pull/3679](https://github.com/volcengine/verl/pull/3679)
**Status**: Merged
**Release**: v0.6.x
**Priority**: Medium
**Keywords**: rl-algorithms, alignment

**Description**: More flexible and easy-to-use reward models

---

#### #4107: RateLimitedRewardLoopManager

**Title**: RateLimitedRewardLoopManager for API-based rewards
**PR Number**: #4107
**Link**: [https://github.com/volcengine/verl/pull/4107](https://github.com/volcengine/verl/pull/4107)
**Status**: Merged
**Release**: v0.6.x
**Priority**: Medium
**Keywords**: rl-algorithms, alignment, deployment

**Description**: Rate limiting for API-based reward models

---

## Summary Statistics

| Category | Count | PRs |
|----------|-------|-----|
| High Priority (Roadmap-Aligned) | 8 | Async, multi-turn, FSDP2, model engine |
| Training Infrastructure | 3 | Megatron optimizations |
| Rollout/Inference | 2 | vLLM FP8, SGLang |
| RL Algorithms | 2 | CISPO, SAPO |
| VLM/Multimodal | 3 | VLM support PRs |
| Performance | 1 | Sequence packing |
| Bug Fixes | 3 | Memory, optimizer, reproducibility |
| Documentation | Multiple | Tutorials, guides |
| **Total** | **30+** | |

---

## Collection Notes

- This index documents PRs identified from release notes and GitHub searches
- Raw patches would require cloning the repository (very large)
- For detailed analysis, refer to PR links on GitHub
- All PRs are merged and in released versions
- Roadmap alignment tracked based on Q3 roadmap [#2388](https://github.com/volcengine/verl/issues/2388)

---

## Next Steps

For detailed code analysis:
1. Clone repository: `git clone https://github.com/volcengine/verl.git`
2. Checkout specific PR: `git fetch origin pull/[PR_NUMBER]/head`
3. Export diff: `git format-patch [commit_range]`
4. Or use GitHub API to fetch PR diff directly

---

**Return to**: Step 5 - Keyword-Based Synthesis
