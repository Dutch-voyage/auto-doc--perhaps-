# DAG-Based Reasoning Training Systems: Materials Checklist

This document tracks the collection and processing of materials related to **DAG-based training systems** for multi-modal agentic reasoning and reinforcement learning.

---

## [Core Framework Papers](#core-framework-papers)

- [x] [DistFlow: A Fully Distributed RL Framework for Scalable and Efficient LLM Post-Training](https://arxiv.org/abs/2507.13833)
- [x] [AsyncFlow: An Asynchronous Streaming RL Framework for Efficient LLM Post-Training](https://arxiv.org/abs/2507.01663)
- [x] [ChunkFlow: Efficient Long Context Fine-tuning via Uniform Chunking](https://arxiv.org/abs/2503.02356)
- [x] [Verlog: Efficient Multi-Turn Reinforcement Learning with LLM Agents](https://openreview.net/forum?id=49c7a127d)
- [x] [Sandbox-RL: Scalable Multi-LLM Optimization via Workflow DAGs](https://openreview.net/forum?id=0pFcKF2li1)

---

## [System Architecture & Optimization](#system-architecture--optimization)

- [x] [AnchorTP: Resilient LLM Inference with Elastic Tensor Parallelism](https://arxiv.org/abs/2511.11617)
- [x] [AReaL: A Large-Scale Asynchronous Reinforcement Learning System for Language Reasoning](https://arxiv.org/abs/2505.24298)
- [x] [StreamRL: Scalable, Heterogeneous, and Elastic RL for LLMs with Disaggregated Stream Generation](https://arxiv.org/abs/2504.15930)

---

## [Agentic Reasoning & Tool Use](#agentic-reasoning--tool-use)

- [x] [Tricks or Traps? A Deep Dive into RL for LLM Reasoning](https://arxiv.org/abs/2508.08221)
- [x] [ROLL Flash -- Accelerating RLVR and Agentic Training with Asynchrony](https://arxiv.org/abs/2510.11345)
- [x] [Reinforcement Learning with Verifiable yet Noisy Rewards under Imperfect Verifiers](https://arxiv.org/abs/2510.00915)

---

## [Multi-Modal & Vision-Language](#multi-modal--vision-language)

- [x] [TAMA: Tool-Augmented Multimodal Agent for Procedural Activity Understanding](https://arxiv.org/abs/2510.00161)
- [x] [Thinking With Videos: Multimodal Tool-Augmented RL for Long Video Reasoning](https://arxiv.org/abs/2508.04416)

---

<!-- ## [GitHub Repositories & Frameworks](#github-repositories--frameworks)

- [ ] [volcengine/verl: Volcano Engine Reinforcement Learning for LLMs](https://github.com/volcengine/verl)
- [ ] [inclusionAI/AReaL: Lightning-Fast RL for LLM Reasoning and Agents](https://github.com/inclusionAI/AReaL)
- [ ] [alibaba/ROLL: Efficient and User-Friendly Scaling Library for RL with LLMs](https://github.com/alibaba/ROLL)
- [ ] [NVIDIA-NeMo/RL: Scalable Toolkit for Efficient Model Reinforcement](https://github.com/NVIDIA-NeMo/RL)
- [ ] [huggingface/trl: Train Transformer Language Models with RL](https://github.com/huggingface/trl)

--- -->

## [Related Topics](#related-topics)

### Graph-Based Training
- [x] [DAG-Math: Graph-Guided Mathematical Reasoning in LLMs](https://arxiv.org/abs/2510.19842)
- [x] [GAP: Graph-Based Agent Planning with Parallel Tool Use and Reinforcement Learning](https://arxiv.org/abs/2510.25320)
- [x] [SALT: Step-level Advantage Assignment via Trajectory Graph](https://arxiv.org/abs/2510.20022)

### Asynchronous Training
- [x] [VerlTool: Towards Holistic Agentic Reinforcement Learning with Tool Use](https://arxiv.org/abs/2509.01055)

### Reward Design
- [x] [Advantage Shaping as Surrogate Reward Maximization: Unifying Pass@K Policy Gradients](https://arxiv.org/abs/2510.23049)
- [x] [AgentPRM: Process Reward Models for LLM Agents via Step-Wise Promise and Progress](https://arxiv.org/abs/2511.08325)
- [x] [Multi-Agent Collaborative Reward Design for Enhancing Reasoning in RL](https://arxiv.org/abs/2511.16202)

---

## Legend

| Status | Description |
|--------|-------------|
| [ ] | Not started |
| [x] | Completed (summary created) |
| [~] | In progress |

---

## Tag Categories

See `Tags.md` for complete taxonomy.

| Category | Symbol | Tags |
|----------|--------|------|
| **System Topics** | [ST] | DAG, Async, Batch, Shard, Runtime, Network, GPU |
| **Training Phases** | [TP] | SFT, RL, Rollout, Train, Chunk, Reward, Oracle, Sync |
| **Application** | [APP] | Reasoning, MultiModal, Agent, Verifier, MultiAgent, Alignment, Coding, Math |
