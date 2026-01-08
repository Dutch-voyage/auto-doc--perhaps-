# AReaL Keyword Labels

**Repository**: https://github.com/inclusionAI/AReaL
**Last Updated**: 2026-01-08

---

## Assigned Keywords (from global_keywords.md)

### Training Infrastructure
| Keyword | Rationale |
|---------|-----------|
| `training-backend` | Supports Megatron and PyTorch FSDP training backends |
| `parallel-strategies` | Implements DP, TP, PP, EP, CP, and FSDP parallelism |
| `rollout-inference` | Integrates vLLM and SGLang for inference-based rollouts |

### RL Algorithms
| Keyword | Rationale |
|---------|-----------|
| `rl-algorithms` | Implements GRPO, GSPO, PPO, DAPO, LitePPO, Dr.GRPO, REINFORCE++, RLOO |
| `alignment` | Supports RLHF for LLM alignment |
| `verifier-guidance` | Includes reward modeling and critic models |

### Model Architecture
| Keyword | Rationale |
|---------|-----------|
| `model-architecture` | Supports Qwen2/3, Qwen-MoE, Qwen2.5-VL, Qwen3-VL, Gemma 3 families |
| `multimodal` | Supports vision-language models (Qwen2.5-VL, Qwen3-VL, Gemma 3) |

### Performance & Optimization
| Keyword | Rationale |
|---------|-----------|
| `performance-optimization` | Fully asynchronous RL training with 2.77× speedup (boba² release) |
| `memory-optimization` | Implements ZeRO-1 (Megatron) and FSDP2 for memory efficiency |
| `communication-optimization` | Cross-node vLLM pipeline/context parallelism |

### Data Pipeline
| Keyword | Rationale |
|---------|-----------|
| `data-pipeline` | Customizable multi-turn agentic rollout workflows |

### Evaluation & Testing
| Keyword | Rationale |
|---------|-----------|
| `evaluation` | Supports offline evaluation and benchmarking configurations |
| `reproducibility` | Provides deterministic training with mock data debugging capabilities |

### Agent & Tool Use
| Keyword | Rationale |
|---------|-----------|
| `agent-framework` | Multi-turn agentic rollout workflows for reasoning models |
| `tool-integration` | Tool-integrated reasoning (TIR) examples |
| `multi-agent` | Supports multi-agent training use cases |

### Deployment & Production
| Keyword | Rationale |
|---------|-----------|
| `scalability` | Scales from single node to 1,000+ GPUs with algorithm-system co-design |
| `deployment` | Production-ready with Docker image CI pipeline planned |

---

## Additional Keywords Not in Global Pool

**None** - All AReaL features map to existing keywords in `global_keywords.md`.

---

## Keyword Coverage Summary

**Total Keywords Assigned**: 19/24 from global pool
- Training Infrastructure: 3/3
- RL Algorithms: 3/3
- Model Architecture: 2/3
- Performance & Optimization: 3/3
- Data Pipeline: 1/3
- Evaluation & Testing: 2/3
- Agent & Tool Use: 3/3
- Deployment & Production: 2/3

**Unassigned Keywords**:
- `quantization` - No explicit quantization support mentioned
- `experience-replay` - Not applicable to this framework
- `synthetic-data` - Mock data for debugging only
- `monitoring` - Profiling planned but not yet implemented
- `fault-tolerance` - Not explicitly mentioned

---

## Notes

- AReaL is a comprehensive RL framework with strong coverage across most keyword categories
- Key differentiator: Fully asynchronous RL training architecture enabling industry-leading speed
- Specializes in reasoning and agentic models with multi-turn rollout workflows
- Strong support for both Megatron and FSDP backends with flexible parallelism strategies
- Active development with quarterly major releases and bi-weekly minor releases
