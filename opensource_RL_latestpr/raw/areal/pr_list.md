# AReaL PR List

**Timeframe**: 2025-01-01 to 2026-01-08 (approx. 1 year)
**Repository**: https://github.com/inclusionAI/AReaL
**Total PRs Analyzed**: 100+ major PRs across releases v0.3.1 to v0.5.1

---

## High Priority (Major Features & Roadmap-Aligned)

### Training Infrastructure

| PR # | Title | Keywords | Roadmap | Link |
|------|-------|----------|---------|------|
| #583 | Rebuild step detection around global batches | training-backend, performance-optimization | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/583) |
| #614 | Implement train controller for single controller | training-backend, scalability | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/614) |
| #611 | Implement rollout controller for single controller | rollout-inference, scalability | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/611) |
| #666 | Implement GRPO trainer and weight exchange for single-controller | training-backend, rl-algorithms | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/666) |
| #413 | Support weights update from distributed sources for Megatron | training-backend, parallel-strategies | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/413) |
| #384 | Refactor FSDP Engine for expert parallelism | training-backend, parallel-strategies | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/384) |
| #590 | Add train/rollout offload support | memory-optimization, training-backend | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/590) |
| #309 | Support tensor parallelism for FSDP engine | parallel-strategies, training-backend | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/309) |
| #278 | Support Ulysses sequence parallel for FSDP | parallel-strategies, memory-optimization | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/278) |
| #277 | Support SGLang cross-node EP and DP attention | parallel-strategies, rollout-inference | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/277) |

### RL Algorithms

| PR # | Title | Keywords | Roadmap | Link |
|------|-------|----------|---------|------|
| #501 | Implement GSPO (Group-level Sequential Policy Optimization) | rl-algorithms, alignment | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/501) |
| #480 | Implement M2PO algorithm | rl-algorithms, alignment | - | [link](https://github.com/inclusionAI/AReaL/pull/480) |
| #408 | Support REINFORCE++ and REINFORCE++-baseline | rl-algorithms, alignment | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/408) |
| #397 | Support RLOO algorithm using leave_one_out norm | rl-algorithms, alignment | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/397) |
| #331 | Add support for Reward Model fine-tuning | rl-algorithms, verifier-guidance | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/331) |
| #392 | Support PPO training with critic models | rl-algorithms, verifier-guidance | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/392) |
| #372 | Unifying normalization for rewards and advantages in PPO | rl-algorithms, evaluation | - | [link](https://github.com/inclusionAI/AReaL/pull/372) |

### Agent & Tool Integration

| PR # | Title | Keywords | Roadmap | Link |
|------|-------|----------|---------|------|
| #500 | Support proxy server and client for OpenAI-compatible agents | agent-framework, tool-integration | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/500) |
| #470 | Integrate openai-agents SDK | agent-framework, tool-integration | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/470) |
| #474 | Integrate Camel-AI | agent-framework, tool-integration | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/474) |
| #657 | Simplify OpenAI agent integration | agent-framework, deployment | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/657) |
| #248 | Support OpenAI-compatible rollout | agent-framework, tool-integration | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/248) |
| #507 | Extract tool output from openai-agents SDK | tool-integration, agent-framework | - | [link](https://github.com/inclusionAI/AReaL/pull/507) |

### Model Architecture Support

| PR # | Title | Keywords | Roadmap | Link |
|------|-------|----------|---------|------|
| #557 | Add Qwen3-VL model support for FSDP | model-architecture, multimodal | - | [link](https://github.com/inclusionAI/AReaL/pull/557) |
| #350 | Support Gemma3 models (multimodal) | model-architecture, multimodal | - | [link](https://github.com/inclusionAI/AReaL/pull/350) |
| #244 | Support variable shape of multi-modal inputs for VLM | model-architecture, multimodal | - | [link](https://github.com/inclusionAI/AReaL/pull/244) |
| #351 | Support NPU and vLLM | deployment, scalability | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/351) |
| #621 | Single LoRA functionality for ascend-vLLM | training-backend, deployment | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/621) |
| #391 | Support LoRA with FSDP training | training-backend, memory-optimization | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/391) |

### Performance & Optimization

| PR # | Title | Keywords | Roadmap | Link |
|------|-------|----------|---------|------|
| #563 | Add pause/resume generation for vLLM server | performance-optimization, rollout-inference | - | [link](https://github.com/inclusionAI/AReaL/pull/563) |
| #607 | Use Gloo group barriers for distributed synchronization | communication-optimization, scalability | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/607) |
| #600 | Implement proximal log-probability approximation for decoupled PPO | performance-optimization, rl-algorithms | - | [link](https://github.com/inclusionAI/AReaL/pull/600) |
| #584 | Streamline step assignment logic | performance-optimization, training-backend | - | [link](https://github.com/inclusionAI/AReaL/pull/584) |
| #510 | Add pipeline parallel support for vLLM inference engine | parallel-strategies, rollout-inference | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/510) |
| #324 | Add patch to accelerate SGLang weight loading | performance-optimization, rollout-inference | - | [link](https://github.com/inclusionAI/AReaL/pull/324) |

### Data Pipeline & Evaluation

| PR # | Title | Keywords | Roadmap | Link |
|------|-------|----------|---------|------|
| #456 | Use DistributedSampler for dataloader | data-pipeline, scalability | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/456) |
| #426 | Fix FSDP tensor parallelism for PPO | training-backend, parallel-strategies | - | [link](https://github.com/inclusionAI/AReaL/pull/426) |
| #624 | Improve workflow batching safeguards | data-pipeline, performance-optimization | - | [link](https://github.com/inclusionAI/AReaL/pull/624) |
| #582 | Support concat export completions in proxy mode | data-pipeline, agent-framework | - | [link](https://github.com/inclusionAI/AReaL/pull/582) |

### Monitoring & Debugging

| PR # | Title | Keywords | Roadmap | Link |
|------|-------|----------|---------|------|
| #608 | Add scheduled profiler tracing | monitoring, performance-optimization | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/608) |
| #539 | Introduce session-centric tracing APIs | monitoring, evaluation | - | [link](https://github.com/inclusionAI/AReaL/pull/539) |
| #487 | Add performance tracing support | monitoring, performance-optimization | - | [link](https://github.com/inclusionAI/AReaL/pull/487) |
| #511 | Add experiment metadata tracking | reproducibility, monitoring | - | [link](https://github.com/inclusionAI/AReaL/pull/511) |

---

## Medium Priority (Bug Fixes & Improvements)

### Bug Fixes

| PR # | Title | Keywords | Roadmap | Link |
|------|-------|----------|---------|------|
| #711 | Fix checkpoint cleanup flag in single-controller mode | training-backend, fault-tolerance | - | [link](https://github.com/inclusionAI/AReaL/pull/711) |
| #653 | Fix port overflow in vLLM server with high DP | deployment, scalability | - | [link](https://github.com/inclusionAI/AReaL/pull/653) |
| #652 | Prevent zombie vLLM processes when Ray kills tasks | deployment, fault-tolerance | - | [link](https://github.com/inclusionAI/AReaL/pull/652) |
| #640 | Tune NCCL IB settings | communication-optimization, performance-optimization | - | [link](https://github.com/inclusionAI/AReaL/pull/640) |
| #598 | Extend NCCL group timeout coverage | fault-tolerance, scalability | - | [link](https://github.com/inclusionAI/AReaL/pull/598) |

### Code Refactoring

| PR # | Title | Keywords | Roadmap | Link |
|------|-------|----------|---------|------|
| #619 | Redesign TrainEngine API with cleaner abstractions | training-backend, deployment | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/619) |
| #663 | Move logprob and value computation into TrainEngine | training-backend, rl-algorithms | - | [link](https://github.com/inclusionAI/AReaL/pull/663) |
| #650 | Refine PPO/GRPO loss | rl-algorithms, training-backend | - | [link](https://github.com/inclusionAI/AReaL/pull/650) |
| #648 | Merge duplicate process termination functions | deployment, fault-tolerance | - | [link](https://github.com/inclusionAI/AReaL/pull/648) |
| #629 | Merge base_hf_engine with fsdp_engine | training-backend, performance-optimization | - | [link](https://github.com/inclusionAI/AReaL/pull/629) |

---

## Low Priority (Documentation & Minor Fixes)

| PR # | Title | Keywords | Roadmap | Link |
|------|-------|----------|---------|------|
| #468 | Add pull request template and contribution guide | deployment, reproducibility | ✓ | [link](https://github.com/inclusionAI/AReaL/pull/468) |
| #445 | Merge duplicate codes in SGLang/vLLM engines | training-backend, performance-optimization | - | [link](https://github.com/inclusionAI/AReaL/pull/445) |
| #478 | Update import paths for math_parser | training-backend, reproducibility | - | [link](https://github.com/inclusionAI/AReaL/pull/478) |
| #499 | Add auto CI on GCP and fix tests | deployment, reproducibility | - | [link](https://github.com/inclusionAI/AReaL/pull/499) |

---

## Roadmap Alignment Summary

### Implemented Roadmap Features (from ROADMAP.md)

| Feature | Status | PRs |
|---------|--------|-----|
| **Single-controller mode** | ✅ Implemented | #614, #611, #666 |
| **Megatron training backend** | ✅ Implemented | #413, #384, #263 |
| **SGLang EP/DP inference** | ✅ Implemented | #277, #274 |
| **Remote vLLM inference** | ✅ Implemented | #318, #563 |
| **Ulysses CP/TP for FSDP** | ✅ Implemented | #278, #309 |
| **End-to-end MoE training** | ✅ Implemented | #413, #384 |
| **OpenAI-compatible client** | ✅ Implemented | #500, #248 |
| **RLOO support** | ✅ Implemented | #397 |
| **NPU/Ascend support** | ✅ Implemented | #351, #621 |

### In Progress / Planned (from ROADMAP.md)

| Feature | Status | Notes |
|---------|--------|-------|
| Multi-LLM training | Planned | Not yet implemented |
| Auto-scaling inference engines | Planned | Not yet implemented |
| Low-precision RL training | Planned | Not yet implemented |
| Wrap training scripts into trainers | Planned | Partially in #660 |
| Docker CI pipeline | Implemented | #564, #574 |

---

## Release Timeline

- **v0.5.1** (Latest): Patch fixes, PPO critic support, VLM training, beam search
- **v0.5.0**: Single Controller Architecture, Seamless Agentic RL
- **v0.4.1**: Proxy mode, performance tracing, pause/resume generation
- **v0.4.0**: Stable MoE training, Agent framework integration (openai-agents, Camel)
- **v0.3.4**: NPU training, RLOO, REINFORCE++, LoRA support, multi-turn math
- **v0.3.3**: Enhanced parallelism (FSDP TP, Ulysses SP), DAPO tricks
- **v0.3.2**: Documentation improvements, allocation mode construction
- **v0.3.1**: Major refactoring, Megatron 5D parallelism, OpenAI client support

---

## Notes

- Most high-priority PRs align with roadmap items from 2025 Q3
- Single Controller architecture is the major focus of v0.5.0
- Agent framework integration (openai-agents, Camel) completed in v0.4.0
- MoE training stability achieved in v0.4.0 with comprehensive Megatron support
- Active development on NPU/Ascend support (ongoing in ascend branch)
- Strong focus on debugging, monitoring, and reproducibility features
