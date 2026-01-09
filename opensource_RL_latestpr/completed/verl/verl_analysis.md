# verl Analysis: Comprehensive Synthesis

**Repository**: [volcengine/verl](https://github.com/volcengine/verl)
**Analysis Date**: 2026-01-08
**Timeframe**: 2025-2026 (last 12 months)
**Based on**: Q3 Roadmap [#2388](https://github.com/volcengine/verl/issues/2388)

---

## Executive Summary

**verl** (Volcano Engine Reinforcement Learning for LLMs) is a production-ready RL training library for large language models, representing the open-source implementation of the HybridFlow paper (EuroSys 2025). Over the past year, verl has undergone significant architectural evolution focused on modularity, async execution, and multi-modal support.

**Key Developments (2025-2026)**:
- Complete migration to **FSDP2** as default training backend
- Implementation of **fully async architecture** with 20-40% throughput gains
- Comprehensive **multi-turn RL** and **tool calling** support
- Full **VLM/multimodal** capabilities
- Introduction of new RL algorithms (**CISPO, SAPO**)
- Enhanced performance optimizations (**sequence packing, FP8 support**)

**Production Maturity**: High - used by Bytedance for Doubao-1.5-pro (70.0 pass@1 on AIME, OpenAI O1-level performance)

---

## Thematic Analysis by Keyword Category

### 1. Training Infrastructure

#### Overview

verl has made significant strides in training infrastructure, focusing on modularity and composability. The major architectural shift is the complete migration to **FSDP2** as the default training backend, replacing FSDP1.

#### Key Changes

**FSDP2 Migration** (v0.7.0, November 2025)
- **Impact**: Complete replacement of FSDP1 with FSDP2 across all recipes and examples
- **Benefits**:
  - Better throughput and memory usage
  - Composability with other PyTorch features (e.g., `torch.compile`)
  - CPU offloading compatible with gradient accumulation
- **Roadmap Alignment**: ✓ Q3 roadmap - "switch all recipe/examples from fsdp1 to fsdp2 by default"
- **References**: [Release v0.7.0](https://github.com/volcengine/verl/releases)

**Model Engine Architecture** (PRs #4211, #4213, #4233)
- **Impact**: Refactored workers with composable model engine architecture
- **Benefits**:
  - Parallelism strategy implemented at engine level (not worker level)
  - FSDP/Megatron engines created and run standalone
  - Reusable across different roles (actor, critic, ref)
  - Support for tensordict dispatch with nested tensor
- **Roadmap Alignment**: ✓ Q3 roadmap - "composable model engines"
- **References**: [#4211](https://github.com/volcengine/verl/pull/4211), [#4213](https://github.com/volcengine/verl/pull/4213), [#4233](https://github.com/volcengine/verl/pull/4233)

**Megatron Backend Enhancements** (PRs #4139, #4158, #4223)
- **Impact**: Improved Megatron-LM integration for large-scale training
- **Features**:
  - Customized prefix for state dict keys
  - MoE FP16 training support
  - Full FP8 training support
- **Benefits**: Better support for 671B parameter models with expert parallelism
- **References**: [#4139](https://github.com/volcengine/verl/pull/4139), [#4158](https://github.com/volcengine/verl/pull/4158), [#4223](https://github.com/volcengine/verl/pull/4223)

#### Technical Insights

1. **Architectural Pattern**: verl has adopted a hybrid-controller programming model that decouples computation and data dependencies, enabling flexible representation of complex post-training dataflows.

2. **Scalability**: The system scales to 671B parameters with expert parallelism, demonstrated through DeepSeek-671B and Qwen3-235B training.

3. **Hardware Support**: Comprehensive support across NVIDIA, AMD (ROCm), and Ascend (NPU) platforms.

---

### 2. Parallel Strategies

#### Overview

verl implements sophisticated parallelism strategies optimized for different training phases and model architectures.

#### Key Features

**3D-HybridEngine** (Core Architecture)
- **Purpose**: Eliminates memory redundancy and reduces communication overhead
- **Impact**: Significant performance improvement during training/generation transitions
- **Features**:
  - Efficient actor model resharding
  - TP x DP dispatch optimization
  - Weight reception from separate resource groups

**Parallelism Support**:
- **Tensor Parallelism (TP)**: For model sharding
- **Pipeline Parallelism (PP)**: For large models
- **Data Parallelism (DP)**: For scaling
- **Expert Parallelism**: For MoE models (671B parameters)
- **Sequence Parallelism**: Via DeepSpeed Ulysses

**FSDP2-Specific Features**:
- CPU offloading with gradient accumulation compatibility
- Better memory usage compared to FSDP1
- Composable with `torch.compile`

---

### 3. Rollout Inference

#### Overview

verl integrates multiple inference engines for rollout generation, with significant enhancements in 2025.

#### Key Developments

**vLLM Integration** (PRs #3519, #4222)
- **Features**:
  - Blockwise FP8 rollout support
  - Performance optimizations for MoE RL models
  - Support for vLLM >= v0.8.2
- **Benefits**: Improved inference efficiency and memory usage
- **References**: [#3519](https://github.com/volcengine/verl/pull/3519), [#4222](https://github.com/volcengine/verl/pull/4222)

**SGLang Enhancements** (Multiple PRs)
- **Features**:
  - Complete process separation from trainer
  - Migration to native server mode
  - Multi-node support
  - Multimodal data optimization
  - Sandbox fusion integration
  - Modular rollout workers (VllmRolloutWorker, SGLangRolloutWorker)
- **Roadmap Alignment**: ✓ Q3 roadmap - "modular rollout workers"
- **Benefits**: Better resource isolation, scalability, and performance

**Rollout Optimizations**:
- Server mode rollout performance improvements
- Support for models with random init weight
- Streaming/partial rollout capabilities (WIP: [#2200](https://github.com/volcengine/verl/pull/2200))

---

### 4. RL Algorithms

#### Overview

verl has expanded its RL algorithm portfolio beyond the initial PPO/GRPO implementations.

#### New Algorithms (v0.7.0)

**CISPO** (Clipped IS-weight Policy Optimization)
- **Purpose**: Advanced policy optimization technique
- **Features**: Clipped importance sampling for stable training
- **Reference**: [Release v0.7.0](https://github.com/volcengine/verl/releases)

**SAPO** (Soft Adaptive Policy Optimization)
- **Purpose**: Adaptive policy optimization with soft constraints
- **Features**: Better handling of reward signal variability
- **Reference**: [Release v0.7.0](https://github.com/volcengine/verl/releases)

**Existing Algorithms**:
- PPO (Proximal Policy Optimization)
- GRPO (Group Relative Policy Optimization)
- GSPO, ReMax, REINFORCE++, RLOO, PRIME
- DAPO (SOTA on AIME 2024 with Qwen2.5-32B)
- DrGRPO, KL_Cov, Clip_Cov
- PF-PPO (ICML 2025)
- VAPO (value-based augmented PPO)

#### Reward System Enhancements

**Reward Model Refactoring** (PR #3679)
- **Impact**: More flexible and easy-to-use reward models
- **Benefits**: Simplified integration of custom reward functions
- **Reference**: [#3679](https://github.com/volcengine/verl/pull/3679)

**RateLimitedRewardLoopManager** (PR #4107)
- **Purpose**: Rate limiting for API-based rewards
- **Benefits**: Cost control and API quota management
- **Reference**: [#4107](https://github.com/volcengine/verl/pull/4107)

**Verifier Guidance**:
- Model-based reward support
- Function-based reward (verifiable reward) for math and coding
- Dense reward support for multi-turn scenarios

---

### 5. Async Architecture

#### Overview

The implementation of fully async architecture represents a major performance milestone for verl.

#### Key Implementation

**Fully Async Training Recipe** (PR #2981, v0.6.1, April 2025)
- **Impact**: 20-40% throughput gain
- **Architecture**:
  - Complete decoupling of Trainer and Rollouter
  - Asynchronous sample generation
  - Asynchronous training
- **Roadmap Alignment**: ✓ Q3 roadmap - "one-step off async pipeline"
- **Benefits**:
  - Better resource utilization
  - Reduced idle time
  - Improved scalability
- **Reference**: [#2981](https://github.com/volcengine/verl/pull/2981)

**Additional Async Features** (WIP):
- Streaming/partial rollout ([#2200](https://github.com/volcengine/verl/pull/2200))
- Fully-async pipeline (ongoing optimization)

#### Technical Insights

1. **Performance Gain**: 20-40% throughput improvement demonstrates the effectiveness of async architecture
2. **Roadmap Progress**: This addresses the Q3 roadmap's focus on async & disaggregated architecture
3. **Future Work**: Continued optimization and profiling for better disaggregated resource allocation

---

### 6. Model Architecture & Multimodal

#### Overview

verl has comprehensive support for various model architectures, with significant enhancements in VLM/multimodal capabilities.

#### Supported Models

**Text Models**:
- Qwen-3, Qwen-2.5
- Llama3.1
- Gemma2
- DeepSeek-LLM, DeepSeek-671B, Qwen3-235B
- HuggingFace Transformers and Modelscope Hub

**Vision-Language Models**:
- Qwen2.5-vl
- Kimi-VL
- Qwen3VL (new in v0.7.0)

#### VLM Support Implementation (PRs #3838, #4186, #4734)

**Model Engine VLM Support** (#3838, v0.6.1)
- **Impact**: VLM support integrated into model engine
- **Reference**: [#3838](https://github.com/volcengine/verl/pull/3838)

**SFT Trainer VLM Support** (#4186, v0.7.0)
- **Impact**: VLM support for supervised fine-tuning
- **Reference**: [#4186](https://github.com/volcengine/verl/pull/4186)

**RL Trainer VLM Support** (#4734, v0.7.0)
- **Impact**: VLM support for RL training
- **Reference**: [#4734](https://github.com/volcengine/verl/pull/4734)

**Additional Features**:
- Multimodal data fetch optimization
- Video input support
- Better abstraction for multi-modal models

**Roadmap Alignment**: ✓ Q3 roadmap - "better abstraction and registration system for multi-modal models"

---

### 7. Multi-turn RL & Agent Framework

#### Overview

Multi-turn RL and agent capabilities represent a major focus area for verl in 2025.

#### Multi-turn Implementation (PRs #4067, #4125, #4182)

**Features**:
- Multi-turn conversation support
- Tool calling capabilities
- Dynamic conversational feedback
- Iterative problem-solving scenarios
- Better message infrastructure for multi-turn messages
- Dense reward support for multi-turn scenarios

**Roadmap Alignment**: ✓ Q3 roadmap - "Agent RL infrastructure"

**Agent Infrastructure**:
- Agent loop development tracking ([#2618](https://github.com/volcengine/verl/issues/2618))
- Multi-turn rollout & agentic RL status
- Tool integration (search tools, sandbox fusion)

**Tool Integration**:
- Multi-turn with tool calling
- Search tool integration
- Sandbox fusion integration
- Modular rollout worker APIs

---

### 8. Performance Optimization

#### Overview

Performance optimization is a consistent theme across all verl developments in 2025.

#### Key Optimizations

**Sequence Packing** (Ongoing throughout 2025)
- **Impact**: Significant throughput increase (expected for Llama, Mistral, Gemma)
- **Benefits**:
  - Removal of padding tokens
  - Better memory utilization
  - Improved training efficiency
- **Implementation**: Uses tensordict and nested-tensor to replace DataProto

**FP8 Support** (PRs #3519, #4222, #4223)
- **vLLM**: Blockwise FP8 rollout
- **Megatron**: Full FP8 training support
- **Benefits**: Reduced memory usage, faster computation

**FSDP2 Performance** (v0.7.0)
- **Benefits**:
  - ~1.4x speedup compared to previous versions
  - Better throughput and memory usage
  - CPU offloading support

**Memory Optimization**:
- Efficient actor model resharding with 3D-HybridEngine
- LoRA support for memory savings
- Multi-gpu LoRA RL support
- FSDP2 CPU offloading compatible with gradient accumulation

**Performance Benchmarks**:
- DAPO: 50 points on AIME 2024 (Qwen2.5-32B)
- Doubao-1.5-pro: 70.0 pass@1 on AIME (OpenAI O1-level)
- Throughput gains of 20-40% from async architecture

---

### 9. Data Pipeline

#### Overview

verl has implemented significant improvements to its data pipeline infrastructure.

#### Key Developments

**TensorDict Dispatch** (PR #4233)
- **Purpose**: Replace DataProto with tensordict and nested-tensor
- **Benefits**:
  - Remove padding
  - Better memory efficiency
  - Improved data handling
- **Roadmap Alignment**: ✓ Q3 roadmap - "use tensordict and nested-tensor to remove padding and replace DataProto"

**Dataset Schema Improvements**:
- Better dataset schema for train & rollout
- Documentation improvements (referencing TRL's documentation)
- Multi-turn message infrastructure

**Planned Features** (Q3 Roadmap):
- Distributed data pool ([RFC #2539](https://github.com/volcengine/verl/pull/2539))
- Persistable replay buffer for large-scale rollout data storage

---

### 10. Deployment & Production

#### Overview

verl is production-ready with extensive deployment capabilities.

#### Production Features

**Scalability**:
- Scales up to 671B models
- Hundreds of GPUs with expert parallelism
- Flexible device mapping for different cluster sizes
- Multi-node support

**Hardware Support**:
- NVIDIA GPUs
- AMD GPUs (ROCm kernel)
- Ascend (NPU)

**Deployment Examples**:
- AWS SageMaker deployment support
- Bytedance production usage (Doubao-1.5-pro)
- Mind Lab: GRPO LoRA for trillion-parameter model on 64 H800

**Fault Tolerance**:
- Experiment tracking (wandb, swanlab, mlflow, tensorboard)
- Checkpoint fixes and improvements
- Reproducibility enhancements

---

### 11. Evaluation & Monitoring

#### Overview

verl provides comprehensive evaluation and monitoring capabilities.

#### Benchmarks

**Math Performance**:
- DAPO: 50 points on AIME 2024 (Qwen2.5-32B)
- Doubao-1.5-pro: 70.0 pass@1 on AIME
- VAPO: 60.4 on AIME 2024 (Qwen-32B-base)

**Reproducibility**:
- Reproducible algorithm baselines for coding and math tasks
- Deterministic training options

**Monitoring**:
- Experiment tracking with wandb, swanlab, mlflow, tensorboard
- Performance tuning guide for optimization
- Comprehensive logging and profiling

---

## Cross-Repository Dependencies

### Integration with External Projects

**HuggingFace Ecosystem**:
- Transformers integration
- Modelscope Hub compatibility
- Model registration system

**Training Frameworks**:
- PyTorch FSDP/FSDP2
- Megatron-LM
- DeepSpeed (partial support)
- Torchtitan (planned)

**Inference Engines**:
- vLLM (>= v0.8.2)
- SGLang (native server mode)
- HF Transformers

**Hardware Platforms**:
- NVIDIA CUDA
- AMD ROCm
- Ascend NPU

**Community Contributions**:
- Bytedance, Anyscale, LMSys.org
- Alibaba Qwen team, Shanghai AI Lab
- Tsinghua University, UC Berkeley, UCLA
- Many others (see README acknowledgements)

---

## Breaking Changes

### Version Migration

**From FSDP1 to FSDP2** (v0.7.0)
- **Impact**: All recipes and examples switched to FSDP2 by default
- **Migration**: Update config to use `strategy=fsdp2`
- **Benefits**: Better performance and memory usage
- **Documentation**: See [#1156](https://github.com/volcengine/verl/issues/1156) for migration guide

**Recipe Directory Migration** (2026-01)
- **Impact**: Recipe directory moved to dedicated repository `verl-recipe`
- **Action**: Use `git submodule update --init --recursive recipe`
- **Kept in Main**: `transfer_queue`, `fully_async_policy`, `one_step_off_policy`, `vla`

**List of Breaking Changes**:
- See issue [#2270](https://github.com/volcengine/verl/issues/2270) for complete list

---

## Future Directions

### Q3 Roadmap Status

**Completed (✓)**:
- Composable model engines
- FSDP2 migration
- Async architecture (one-step off)
- Multi-turn rollout and tool support
- VLM support improvements
- Sequence packing

**In Progress**:
- Fully-async pipeline optimization
- Performance tuning and benchmarking
- Torchtitan integration (call for contribution)
- Better multi-modal abstraction

**Not Started**:
- Distributed data pool/persistable replay buffer ([#2539](https://github.com/volcengine/verl/pull/2539))
- Documentation for model support status

**Planned**:
- Better documentation for adding new models
- Per-model feature documentation (LoRA, sequence parallelism, etc.)
- High-quality recipes from community

---

## Technical Assessment

### Strengths

1. **Modularity**: Composable architecture enabling flexible extension
2. **Performance**: State-of-the-art throughput with async architecture
3. **Scalability**: Proven at 671B parameters
4. **Production-Ready**: Used by major companies for production models
5. **Community**: Large, active community with extensive contributions
6. **Multi-modal**: Comprehensive VLM support
7. **Algorithm Portfolio**: Wide range of RL algorithms
8. **Hardware Support**: Cross-platform compatibility (NVIDIA, AMD, Ascend)

### Areas for Improvement

1. **Documentation**: Some areas need better documentation (model support status, new model workflow)
2. **Torchtitan Integration**: Still planned, not implemented
3. **Distributed Data Pool**: Not yet implemented (RFC open)
4. **Breaking Changes**: Migration path could be smoother

---

## Strategic Insights

### Market Position

verl occupies a unique position as:
1. **Open-source implementation of HybridFlow** (EuroSys 2025)
2. **Production-ready** with proven scalability
3. **Community-driven** with extensive adoption
4. **Multi-modal capable** with comprehensive VLM support

### Competitive Advantages

1. **Async Architecture**: 20-40% throughput gain over synchronous systems
2. **Modular Design**: Easy to extend and customize
3. **Comprehensive Backend Support**: FSDP2, Megatron-LM, vLLM, SGLang
4. **Proven at Scale**: 671B parameter models
5. **Active Development**: Regular releases with significant features

### Development Trends

1. **FSDP2 Adoption**: Complete migration from FSDP1
2. **Async Execution**: Major performance optimization direction
3. **Multi-turn RL**: Growing focus on agentic AI
4. **Multi-modal**: VLM support becoming standard
5. **Performance**: Continuous optimization (FP8, sequence packing)
6. **Community Recipes**: Growing ecosystem of training recipes

---

## References

### Core Documentation
- **GitHub Repository**: [volcengine/verl](https://github.com/volcengine/verl)
- **Documentation**: [verl.readthedocs.io](https://verl.readthedocs.io/)
- **Q3 Roadmap**: [Issue #2388](https://github.com/volcengine/verl/issues/2388)

### Key Papers
- **HybridFlow**: [arXiv:2409.19256](https://arxiv.org/abs/2409.19256) (EuroSys 2025)
- **VAPO**: [arXiv:2504.05118](https://arxiv.org/abs/2504.05118)
- **PF-PPO**: [arXiv:2409.06957](https://arxiv.org/abs/2409.06957) (ICML 2025)

### Release Notes
- **v0.7.0**: 2025-11-13 (FSDP2, multi-turn, VLM, CISPO/SAPO)
- **v0.6.1**: 2025-04 (Fully async, VLM support)
- **v0.3.0.post1**: 2025-03 (~1.4x speedup, DAPO)

### Key PRs
- Async Training: [#2981](https://github.com/volcengine/verl/pull/2981)
- Multi-turn Support: [#4067](https://github.com/volcengine/verl/pull/4067), [#4125](https://github.com/volcengine/verl/pull/4125), [#4182](https://github.com/volcengine/verl/pull/4182)
- Model Engine: [#4211](https://github.com/volcengine/verl/pull/4211), [#4213](https://github.com/volcengine/verl/pull/4213), [#4233](https://github.com/volcengine/verl/pull/4233)
- VLM Support: [#3838](https://github.com/volcengine/verl/pull/3838), [#4186](https://github.com/volcengine/verl/pull/4186), [#4734](https://github.com/volcengine/verl/pull/4734)

### Related Materials
- **Performance Tuning Guide**: [verl.readthedocs.io](https://verl.readthedocs.io/en/latest/perf/perf_tuning.html)
- **Installation Guides**: [verl.readthedocs.io](https://verl.readthedocs.io/)
- **Community Tutorials**: Various blog posts and tutorials (see README)

---

## Conclusion

verl has established itself as a mature, production-ready RL training library with comprehensive capabilities for large-scale language model post-training. The developments in 2025-2026 demonstrate a clear focus on:

1. **Modularity and Composability** (FSDP2, model engine architecture)
2. **Performance Optimization** (async architecture, FP8, sequence packing)
3. **Multi-modal Support** (comprehensive VLM capabilities)
4. **Agentic AI** (multi-turn RL, tool calling)
5. **Scalability** (671B parameter models)

The project's strong community support, regular releases, and proven production usage position it as a leading choice for RLHF and RL post-training of large language models.

---

**Analysis Complete**

**Next**: Proceed to Step 6 - Guidance Documentation
