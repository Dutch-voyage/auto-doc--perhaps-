# AReaL PR Index

**Last Updated**: 2026-01-08
**Repository**: https://github.com/inclusionAI/AReaL
**Total PRs Documented**: 100+ (from v0.3.1 to v0.5.1)

---

## About This Index

This index provides metadata for major pull requests in AReaL from 2025. Full PR diffs are not included due to the large volume (100+ PRs). For detailed PR information, please refer to the official GitHub repository:

- **PR List**: https://github.com/inclusionAI/AReaL/pulls
- **Releases**: https://github.com/inclusionAI/AReaL/releases

---

## Release Timeline & Key PRs

### v0.5.1 (Latest - Dec 2025)
**Release Date**: ~2025-12-15
**Milestone**: Patch release with critical fixes

**Key PRs**:
- #711: Fix checkpoint cleanup in single-controller mode
- #653: Fix port overflow in vLLM server
- #652: Prevent zombie vLLM processes
- #698: VLM training support
- #721: Beam search support for vLLM
- #729: PPO critic model for Megatron

### v0.5.0 (Nov 2025)
**Release Date**: ~2025-11-15
**Milestone**: Single Controller Architecture & Seamless Agentic RL

**Key PRs**:
- #583: Rebuild step detection around global batches
- #614: Implement train controller for single controller
- #611: Implement rollout controller for single controller
- #666: Implement GRPO trainer for single-controller
- #607: Use Gloo group barriers for distributed synchronization
- #608: Add scheduled profiler tracing
- #621: Single LoRA for ascend-vLLM

### v0.4.1 (Oct 2025)
**Release Date**: ~2025-10-15
**Milestone**: Performance & Agent Improvements

**Key PRs**:
- #500: Support proxy server for OpenAI-compatible agents
- #557: Add Qwen3-VL model support
- #563: Pause/resume generation for vLLM
- #539: Session-centric tracing APIs
- #487: Performance tracing support
- #511: Experiment metadata tracking
- #564, #574: Docker CI pipeline

### v0.4.0 (Sep 2025)
**Release Date**: ~2025-09-15
**Milestone**: Stable MoE Training & Agent Framework Integration

**Key PRs**:
- #413: Support weights update from distributed sources (Megatron)
- #384: Refactor FSDP Engine for expert parallelism
- #501: Implement GSPO algorithm
- #470: Integrate openai-agents SDK
- #474: Integrate Camel-AI
- #510: Pipeline parallel support for vLLM
- #468: PR template and contribution guide

### v0.3.4 (Aug 2025)
**Release Date**: ~2025-08-15
**Milestone**: NPU Support & New Algorithms

**Key PRs**:
- #351: Support NPU and vLLM
- #397: Support RLOO algorithm
- #408: Support REINFORCE++ and REINFORCE++-baseline
- #392: Support PPO with critic models
- #331: Reward Model fine-tuning
- #391: Support LoRA with FSDP
- #350: Support Gemma3 models (multimodal)

### v0.3.3 (Jul 2025)
**Release Date**: ~2025-07-15
**Milestone**: Enhanced Parallelism & Algorithm Features

**Key PRs**:
- #309: Support tensor parallelism for FSDP
- #278: Support Ulysses sequence parallel for FSDP
- #285: Decoupled CLIP ratio (DAPO Trick-I)
- #294: Dynamic sampling (DAPO Trick-II)
- #295: Overlength reward penalty (DAPO Trick-III)
- #303: Decoupled mean/std advantage normalization

### v0.3.2 (Jun 2025)
**Release Date**: ~2025-06-15
**Milestone**: Documentation & Allocation Mode

**Key PRs**:
- #287: Best practices documentation (debugging, OOM)
- Intuitive allocation mode construction

### v0.3.1 (May 2025)
**Release Date**: ~2025-05-15
**Milestone**: Major Refactoring to `areal` Codebase

**Key PRs**:
- #263: Megatron 5D parallel forward
- #274: SGLang cross-node TP and dp-attention
- #278: Ulysses sequence parallel for FSDP
- #277: SGLang cross-node EP and dp_attn
- #248: OpenAI-compatible rollout
- #244: Variable shape multi-modal inputs for VLM
- #234: Fault recovery and rollout-only evaluation

---

## PR Categories

### Training Infrastructure (35+ PRs)
- Single Controller Architecture: #614, #611, #666, #583
- Megatron Backend: #413, #384, #263, #275
- FSDP Engine: #309, #278, #384, #426
- Parallelism: #277, #274, #510
- Memory Optimization: #590, #391

### RL Algorithms (20+ PRs)
- GSPO: #501
- M2PO: #480
- RLOO: #397
- REINFORCE++: #408
- PPO with Critic: #392
- Reward Modeling: #331
- DAPO Tricks: #285, #294, #295, #303

### Agent & Tool Integration (15+ PRs)
- OpenAI-Compatible: #500, #248, #657
- openai-agents SDK: #470, #507
- Camel-AI: #474
- Tool Output Extraction: #507
- Proxy Mode: #500

### Model Architecture (12+ PRs)
- VLM Support: #557, #350, #244, #698
- Qwen3-VL: #557
- Gemma3: #350
- NPU Support: #351, #621

### Performance & Optimization (18+ PRs)
- Tracing: #487, #539, #608, #511
- SGLang Optimization: #324
- vLLM Features: #563, #510, #721
- Distributed Training: #607, #456

### Documentation & CI (15+ PRs)
- Best Practices: #287, #538
- Contribution Guide: #468
- Megatron Tutorial: #521
- Docker CI: #564, #574

---

## Statistics

| Category | Count |
|----------|-------|
| Training Infrastructure | 35+ |
| RL Algorithms | 20+ |
| Agent Integration | 15+ |
| Model Architecture | 12+ |
| Performance & Optimization | 18+ |
| Documentation & CI | 15+ |
| Bug Fixes | 40+ |
| **Total** | **155+** |

---

## Roadmap Alignment

### ✅ Completed Roadmap Items
| Feature | PRs | Status |
|---------|-----|--------|
| Single-controller mode | #614, #611, #666 | ✅ Complete |
| Megatron training backend | #413, #384, #263 | ✅ Complete |
| SGLang EP/DP inference | #277, #274 | ✅ Complete |
| Remote vLLM inference | #318, #563 | ✅ Complete |
| Ulysses CP/TP for FSDP | #278, #309 | ✅ Complete |
| End-to-end MoE training | #413, #384 | ✅ Complete |
| OpenAI-compatible client | #500, #248 | ✅ Complete |
| RLOO support | #397 | ✅ Complete |
| NPU/Ascend support | #351, #621 | ✅ Complete |

---

## Notable Contributors

Based on PR merge frequency:
- @garrett4wade - Documentation, refactoring, CI/CD
- @rchardx - Training engine, parallelism, FSDP
- @dhh1995 - Algorithms (PPO, GRPO, RLOO)
- @nuzant - Megatron backend, testing
- @fishcrap - Distributed training, FSDP
- @dingzhiqiang - Single controller architecture
- @zhshgmail - Performance optimization
- @HwVanICI - NPU support, VLM, vLLM

---

## Accessing Full PR Details

For complete PR information including code changes, comments, and review discussions:

1. **GitHub PR Page**: https://github.com/inclusionAI/AReaL/pulls
2. **Specific PR**: https://github.com/inclusionAI/AReaL/pull/[PR_NUMBER]
3. **Git Clone**:
   ```bash
   git clone https://github.com/inclusionAI/AReaL.git
   cd AReaL
   git log --merges --oneline
   git show [PR_COMMIT_HASH]
   ```

---

## Notes

- This index covers PRs from major releases v0.3.1 to v0.5.1 (May - December 2025)
- PR numbers are approximate and may not represent exact chronological order
- Some PRs may span multiple releases
- For detailed analysis of specific features, refer to individual PR pages
