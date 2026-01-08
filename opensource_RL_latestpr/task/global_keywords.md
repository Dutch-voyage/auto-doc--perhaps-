# Global Keyword Taxonomy

**Last Updated**: 2026-01-08
**Version**: 1.0

---

## Purpose
Maintain a consistent, evolving keyword pool for categorizing RL framework developments across all repositories.

---

## Primary Categories

### Training Infrastructure
| Keyword | Description | Related Terms |
|---------|-------------|---------------|
| `training-backend` | Core training systems (Megatron, FSDP, Deepspeed) | backend, trainer, engine |
| `parallel-strategies` | Distributed training methods (TP, PP, EP, CP, FSDP) | distributed, sharding, parallelism |
| `rollout-inference` | Inference engines for data generation (SGLang, vLLM) | serving, inference, rollout |

### RL Algorithms
| Keyword | Description | Related Terms |
|---------|-------------|---------------|
| `rl-algorithms` | RL optimization methods (PPO, DPO, REINFORCE) | optimization, policy, reward |
| `alignment` | Model alignment techniques (RLHF, RLAIF, DPO) | safety, preference optimization |
| `verifier-guidance` | Verification-based training (Monte Carlo, Q-learning) | search, verification, reward models |

### Model Architecture
| Keyword | Description | Related Terms |
|---------|-------------|---------------|
| `model-architecture` | Model types (VLM, MoE, Dense, Transformer) | architecture, model family |
| `multimodal` | Vision-language and multi-modal capabilities | VLM, vision, cross-modal |
| `quantization` | Model compression (Int4, Int8, FP8, QAT) | compression, sparsity, pruning |

### Performance & Optimization
| Keyword | Description | Related Terms |
|---------|-------------|---------------|
| `performance-optimization` | Efficiency improvements (speed, memory, throughput) | optimization, acceleration |
| `memory-optimization` | Memory management (offload, sharding, checkpointing) | memory, VRAM, host memory |
| `communication-optimization` | Network/computation overlap (gradient compression, comms) | communication, bandwidth, latency |

### Data Pipeline
| Keyword | Description | Related Terms |
|---------|-------------|---------------|
| `data-pipeline` | Data generation, processing, and management | data, dataset, preprocessing |
| `experience-replay` | Replay buffers and data management (R2, R3, replay) | buffer, storage, replay |
| `synthetic-data` | Synthetic and procedural data generation | synthetic, procedural, generated |

### Evaluation & Testing
| Keyword | Description | Related Terms |
|---------|-------------|---------------|
| `evaluation` | Benchmarks and metrics (accuracy, efficiency, quality) | benchmark, metrics, testing |
| `reproducibility` | Deterministic training and fault tolerance | deterministic, reproducible, stable |
| `monitoring` | Training monitoring and debugging (logging, profiling) | observability, debugging, profiling |

### Agent & Tool Use
| Keyword | Description | Related Terms |
|---------|-------------|---------------|
| `agent-framework` | Agentic RL and tool-using models | agents, tool use, autonomous |
| `tool-integration` | Tool and API integration (function calling, RAG) | tools, APIs, external systems |
| `multi-agent` | Multi-agent systems and coordination | multi-agent, coordination, collaboration |

### Deployment & Production
| Keyword | Description | Related Terms |
|---------|-------------|---------------|
| `deployment` | Production deployment and serving | serving, production, deployment |
| `fault-tolerance` | Fault handling and recovery | resilience, robustness, reliability |
| `scalability` | System scaling capabilities | scale, distributed, cluster |

---

## Repository-Specific Labels

### slime (THUDM)
```
training-backend, parallel-strategies, rollout-inference, rl-algorithms,
model-architecture, multimodal, performance-optimization, memory-optimization,
data-pipeline, experience-replay, evaluation, reproducibility, agent-framework,
tool-integration, fault-tolerance, scalability
```

---

## Usage Guidelines

### Adding New Keywords
1. **Check existing categories** first
2. **Add to appropriate category** with description
3. **Update version number** and date
4. **Consider cross-repo consistency** before adding

### Querying Keywords
- Use for **PR categorization** in analysis
- Use for **feature indexing** across repos
- Use for **trend identification** over time

### Updating Keywords
- **Deprecate** (don't delete) unused keywords
- **Add aliases** for related terms
- **Document rationale** for significant changes

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-08 | Initial taxonomy with 8 primary categories |

---

## Notes

- Keywords are **case-insensitive** in queries
- Use **primary category** as main tag
- Add **repository-specific labels** as needed
- Maintain **backward compatibility** when possible
