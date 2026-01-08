# slime Roadmap Summary

**Repository**: THUDM/slime
**Last Updated**: 2026-01-08
**Source**: https://github.com/THUDM/slime

---

## Official Roadmap Items

### From GitHub Issues (Roadmap Label)

**Query**: https://github.com/THUDM/slime/issues?q=is%3Aissue+state%3Aopen+label%3Aroadmap

No explicit roadmap issues found with "roadmap" label.

### From Release Notes & Blog Posts

#### Version 0.2.1 (Current) - Released 2026-01-08
**Status**: ✅ Implemented
**Key Features**:
- VLM + FSDP: True on-policy training on Qwen3-VL (dense)
- PD-disaggregation support during rollout
- DP-attention support in rollout routing replay (R3)
- Upgraded to SGLang v0.5.6

**Target**: Enhanced multi-modal training and distributed training capabilities

#### Version 0.2.0 - Major Release
**Status**: ✅ Implemented
**Key Features**:
- FSDP Backend: Fully Sharded Data Parallel training
- PPO Support: Proximal Policy Optimization
- MTP Training: Multi-Token Prediction during RL
- FP8 Full Stack: FP8 training and inference
- Train-Inference Mismatch Solutions:
  - Importance Sampling (MIS)
  - Routing Replay (R3, R2)
  - True On-Policy Training
- Performance Optimizations
- Python-based Router
- Fault Tolerance

**Target**: Production-ready RL training framework

#### Version 0.1.0 - Initial Release
**Status**: ✅ Implemented
**Key Features**:
- SGLang integration (FP8 + DeepEP + speculative decoding)
- Megatron integration (all parallel strategies + DeepEP + CPU Adam)
- Algorithm Support: GSPO, TIS, Reinforce++, Reinforce++ base

**Target**: Foundation for high-performance RL training

---

## Future Enhancements (from Blog Posts & Documentation)

### 1. Extended Optimization Methods
**Source**: Blog posts and releases
**Description**: Extending support to more optimization methods beyond PPO, DPO, REINFORCE
**Status**: In progress
**Related**: Open PRs for new algorithm integrations

### 2. Enhanced Multi-Modal Support
**Source**: Recent PR activity (#1210, #1215, #1155)
**Description**: Megatron VLM support for Qwen2.5-VL series and other VLM architectures
**Status**: Active development (3/N series)
**Target**: Comprehensive VLM training capabilities

### 3. Quantization Support
**Source**: PRs #1172, #1173
**Description**: Int4 QAT support, FP8 weight updates from Megatron
**Status**: In development
**Target**: Efficient model compression and training

### 4. Tool Use & Agentic Features
**Source**: PRs #1159, #1203
**Description**: Tool call support for multi-turn SFT, OAI interface for router
**Status**: Active development
**Target**: Enhanced agent capabilities

### 5. LoRA Training Support
**Source**: PR #1140
**Description**: FSDP backend LoRA training
**Status**: In development (1/N)
**Target**: Efficient parameter-efficient fine-tuning

### 6. Advanced Benchmarking
**Source**: PRs #1156, #1154, #1158
**Description**: Tau2-bench, Terminal Bench evaluation integration
**Status**: In development
**Target**: Comprehensive evaluation framework

### 7. Fault Tolerance Improvements
**Source**: PR #1311 (WIP)
**Description**: Enhanced fault tolerance for production deployments
**Status**: Work in progress
**Target**: Improved reliability and resilience

---

## Architectural Trends

### 1. Multi-Modal First
- Heavy investment in VLM support
- True on-policy training for vision-language models
- Integration with Qwen3-VL, Qwen2.5-VL

### 2. Distributed Training Evolution
- FSDP backend becoming primary training method
- PD-disaggregation for better resource utilization
- DP-attention optimizations

### 3. Production Readiness
- Fault tolerance improvements
- Reproducibility features (deterministic rollout)
- Performance optimization (FP8, speculative decoding)

### 4. Agent-Centric Development
- Tool use and integration
- Multi-agent scenarios
- Agentic RL training patterns

---

## Version Information

**Current Version**: v0.2.1
**Release Cadence**: Rapid (v0.1.0 → v0.2.0 → v0.2.1 in quick succession)
**Development Velocity**: High (1,100+ merged PRs, 55 open PRs)
**Maturity**: Production-ready (powers GLM-4.5 and GLM-4.6)

---

## Dependencies

### Core Dependencies
- **Megatron-LM**: Training backend
- **SGLang**: Rollout/inference engine
- **PyTorch**: Base framework

### Integration Points
- Supports: Qwen3 series, DeepSeek V3 series, Llama 3
- Hardware: NVIDIA GPUs (including GB200, B200)
- Backends: FSDP, Megatron, XTuner

---

## Notes

- slime is the RL framework behind Zhipu AI's GLM-4.5 and GLM-4.6
- Strong focus on production deployment and scalability
- Active community with regular contributions
- Roadmap driven by real-world production requirements

---

**Next Step**: Proceed to keyword assignment (Step 2)
