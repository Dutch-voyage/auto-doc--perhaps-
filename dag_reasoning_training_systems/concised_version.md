# Technical Analysis: Multi-Level DAG Design for Agentic Reasoning Training Systems

## Executive Summary

This document synthesizes insights from 20 research papers on DAG-based training systems, analyzing the architecture through a 4-level framework: (1) Data as DAGs, (2) Training/Inference Pipelines, (3) Orchestration State Machine. The core insight is that **bubbles manifest differently** in inference vs. training engines—**inference bubbles are I/O-bound** (waiting for external tools), while **training bubbles are compute-bound** (waiting for gang-synchronized GPUs). Understanding this distinction enables targeted optimization strategies for each phase.

---

## Level 1: The Foundation (Data as DAGs)
![DAG_data](external/images/DAG_def.png)


**Objective**: Encode reasoning as structured dependencies rather than linear sequences.

Training data is not a flat sequence but a **subgraph extracted from a capability "super-graph"**—where the super-graph represents all available tools/agents, and a task activates only the relevant subset.

### Core Concepts

**Logical Closeness** (DAG-Math): Instead of binary pass/fail metrics, measures how well a trajectory follows valid derivation paths in the DAG. Models with similar PASS@k scores can have significantly different reasoning quality when evaluated by logical closeness.

**Step-Level Value**: Techniques like SALT and AgentPRM assign credit to individual nodes (steps) by analyzing their contribution to final success across multiple rollout attempts:
- **SALT**: Constructs trajectory graphs from multiple rollouts; step quality = f(success_rate, rarity, transition_patterns)
- **AgentPRM**: Defines **Promise** (expected value toward goal) and **Progress** (marginal contribution of action); TD-estimation with GAE enables 8× sample efficiency

**DAG Quality Dimensions**:
| Dimension | Metric | Purpose |
|-----------|--------|---------|
| **Structural Validity** | Logical closeness | Does trajectory follow valid edges? |
| **Node Quality** | Promise/Progress | How much does this step contribute? |
| **Edge Reliability** | Transition success rate | Is this action->state transition effective? |
| **Graph Efficiency** | Parallelizability score | Can sub-tasks execute concurrently? |

### DAG-Related Challenges at Data Level

**Challenge 1: Subgraph Extraction from Super-Graph**
- **Problem**: The capability super-graph may contain thousands of potential tools/agents; extracting the optimal subgraph for a specific query is non-trivial
- **Solutions**:
  - **GAP**: Learn to predict task graphs through SFT on annotated MHQA data → RL refinement
  - **TAMA/VITAL**: Agent dynamically decides which tools to invoke during execution
  - **Training Data**: Human-annotated dependency graphs (expensive but high-quality)

**Challenge 2: Multi-Modal Data Flow Through DAG Edges**
- **Problem**: DAG edges must carry heterogeneous data types—text, images, video embeddings, structured JSON
- **Solutions**:
  - **VerlTool**: Unified tool API with modality declarations; tools return structured outputs
  - **TAMA**: Multimedia-returning tools (images, bounding boxes) flow as edge data
  - **VITAL**: Visual toolbox for video—frame sampling tools return image sequences

**Challenge 3: Credit Assignment Across DAG Topology**
- **Problem**: How to assign credit when only final outcome is observable, not intermediate step quality?
- **Solutions**:
  - **SALT**: Trajectory graph analysis identifies high-quality steps through frequency/success_rate patterns
  - **CRM**: Multi-agent collaborative reward—specialist evaluators (factuality, helpfulness, safety) + centralized aggregator
  - **Advantage Shaping**: Surrogate reward optimization reveals hard-example up-weighting = reward-level regularization

**Challenge 4: Dynamic vs. Static DAG Construction**
- **Problem**: Should DAG be pre-computed (static) or constructed dynamically during execution?
- **Trade-offs**:
  - **Static DAG**: Faster execution, pre-computed dependencies; less flexible to novel queries
  - **Dynamic DAG**: Adapts to query complexity; introduces planning overhead
- **Current State**: GAP uses static task graphs from SFT; TAMA/VITAL use dynamic tool selection

---

## Level 2: Pipelines (Two Engines)

### Phase A: Inference & Rollout Engine
![DAG-rollout](external/images/partial_rollout.png)


**Constraint**: External Tool Latency (I/O Bound)
**Goal**: Maximize generation throughput while agents wait for tools.

**Critical Insight**: Inference bubbles are **I/O-bound**—caused by latency variance from external tools (e.g., video processing: 10s, code interpreter: 0.1s, web search: 2s).

#### 1. The "Inference Bubble" Problem

When an agent calls a slow tool, the GPU sits idle (a bubble) if it blocks for the return. This is fundamentally different from training bubbles:

| Bubble Type | Inference (Phase A) | Training (Phase B) |
|-------------|---------------------|-------------------|
| **Root Cause** | External tool latency (I/O wait) | Gang schedule synchronization (compute wait) |
| **Duration** | Highly variable (0.1s - 10s+) | More predictable (ms scale) |
| **Dependency** | Independent of other agents | Requires all GPUs in gang |
| **Solution Space** | Async execution, context swapping | Elastic backfilling, chunk packing |

**Solution**: Async Partial Rollouts (ROLL Flash)

The system uses a **Producer-Consumer model**. When an agent hits a tool call:
1. Its state (KV-cache) is offloaded to CPU ("frozen")
2. GPU immediately switches to a "Filler Task" from a global queue
3. When tool result returns, original state is reloaded and resumes

**Architecture**:
```
Rollout Stage (Inference GPUs)     Training Stage (Training GPUs)
┌──────────────────┐             ┌──────────────────────────────────┐
│  LLMProxy        │──trajectories→│  AsyncController                 │
│  ├─ Worker 1     │             │  ├─ get_batch (from SampleBuffer)│
│  ├─ Worker 2     │             │  ├─ train_step                   │
│  └─ Worker N     │             │  └─ model_update (broadcast)     │
└────────┬─────────┘             └──────────────────────────────────┘
         │
         ▼
┌──────────────────┐
│  EnvManager 1-N  │──tool_results──┐
│  └─ BaseEnv      │               │
│  └─ Event Loop   │               │
└──────────────────┘               │
                                   │
                           ┌───────┴────────┐
                           │ SampleBuffer   │
                           │ (freshness     │
                           │  constraint α) │
                           └────────────────┘
```

**Results**:
- **Environment-Level Async**: 1.23× - 1.58× speedup (SWE-bench, ALFWorld)
- **Queue Scheduling**: 2.16× over synchronous batching
- **Rollout-Train Decoupling**: 2.24× throughput on 128 GPUs

#### 2. DAG-Aware Scheduling: Dependency-Parallel Execution

**Problem**: Traditional ReAct processes tool calls sequentially, even when independent sub-tasks could execute in parallel.

**Solution** (GAP): Construct **dependency-aware task graphs** where:
- Nodes = sub-tasks with tool annotations
- Edges = data dependencies (output of A required as input to B)
- Scheduler launches all ready nodes (no pending dependencies) in parallel

**Example DAG**:
```
Question: "Compare GDP and population of France, Germany, and Italy"

[Search: France GDP] ─┐
[Search: Germany GDP]─┼──→ [Compare GDP] ─┐
[Search: Italy GDP] ─┘                    └──→ [Final Answer]
                                              ┌─────────────────────┘
[Search: France Pop] ─┐                     │
[Search: Germany Pop]─┼──→ [Compare Pop] ────┘
[Search: Italy Pop] ─┘
```

**Parallel execution**: Search tasks execute simultaneously (1.74× speedup); Compare tasks execute sequentially (dependency required).

**Performance**:
| Question Type | Independent Sub-tasks | Parallel Speedup |
|---------------|----------------------|------------------|
| Simple lookup | 1-2 | 1.2× |
| Multi-hop (3 entities) | 3 | 1.8× |
| Multi-hop (5+ entities) | 5+ | 2.3× |

#### 3. Prompt Replication for Intra-Rollout Parallelism

**Problem**: Multi-candidate decoding (num_return_sequences >> 1) forces single worker to decode all responses sequentially.

**Solution** (ROLL Flash): Expand each prompt into **n independent rollout tasks**:
```
Traditional: Prompt A → Worker 1 → [A1, A2, ..., A16] (sequential bottleneck)

Prompt Replication:
Prompt A1 → Worker 1 → A1
Prompt A2 → Worker 2 → A2
...
Prompt A16 → Worker 16 → A16
```

**Performance**: 1.30-1.95× speedup depending on batch configuration.

#### 4. Redundant Environment Rollout (Resilience)

**Problem**: Environment instability (fail-slow, fail-stop) creates bottlenecks.

**Solution** (ROLL Flash): Two tunable controls:
- **num_env_groups**: More concurrent environment groups
- **group_size**: More candidate trajectories per group

**Key Finding**: Increasing num_env_groups more effective than group_size (5.40× vs 5.28× speedup).

---

### Phase B: Training Engine

![DAG-chunk](external/images/chunk-node-flow.png)

**Constraint**: Synchronization Barriers (Compute Bound)
**Goal**: Maximize MFU (Model Flops Utilization) on ragged training data.

**Critical Insight**: Training bubbles are **compute-bound**—caused by ragged sequences and synchronization barriers required for distributed training (Ring Attention, Gang Scheduling).

#### 1. The "Training Bubble" Problem

Training requires **Gang Scheduling**: multiple GPUs must work on the same sequence chunks simultaneously to compute attention. If one GPU finishes early, it must wait for others (a bubble).

**This differs from inference bubbles**:
| Aspect | Inference Bubble | Training Bubble |
|--------|-----------------|-----------------|
| **Resource Waiting For** | External I/O (tool response) | Other GPUs (synchronization) |
| **Predictability** | Highly variable (0.1s - 10s+) | More predictable (ms scale) |
| **Mitigation** | Switch to another agent's work | Fill with independent chunk |
| **State Management** | Offload context to CPU | Keep activations in VRAM |

**Solution**: Elastic Backfilling (AnchorTP / Elastic Scheduler)

The scheduler detects idle gaps in the gang schedule and inserts small, independent chunks (from other samples) to fill the bubbles.

**Mechanism**:
```
Timeline WITHOUT bubble filling:
GPU 0: [Chunk1 Gang Schedule] [idle waiting...] [Chunk1 Gang Schedule]
GPU 1: [Chunk1 Gang Schedule] [idle waiting...] [Chunk1 Gang Schedule]
GPU 2: [Chunk1 Gang Schedule] [idle waiting...] [Chunk1 Gang Schedule]
GPU 3: [Chunk1 Gang Schedule] [idle waiting...] [Chunk1 Gang Schedule]

Timeline WITH bubble filling:
GPU 0: [Chunk1 Gang Schedule] [SmallChunk A] [Chunk1 Gang Schedule]
GPU 1: [Chunk1 Gang Schedule] [SmallChunk B] [Chunk1 Gang Schedule]
GPU 2: [Chunk1 Gang Schedule] [SmallChunk C] [Chunk1 Gang Schedule]
GPU 3: [Chunk1 Gang Schedule] [SmallChunk D] [Chunk1 Gang Schedule]
```

#### 2. DAG-Aware Chunk Scheduling: Uniform Chunking (ChunkFlow)

**Problem**: Variable-length agent trajectories (4k - 32k tokens) cause massive load imbalance and pipeline bubbles.

**Solution** (ChunkFlow): Chop all data into **uniform blocks** (e.g., 4096 tokens) while preserving logical DAG dependencies.

**Chunk Construction Algorithm**:
1. **Long sequences** (> ChunkSize): Split into multiple uniform chunks
2. **Short sequences** (< ChunkSize): Bin-pack together to fill a chunk
3. **Dependent chunks** (from split sequences): Maintain causal order through DAG edges

**State-Aware Scheduling**:
- **Standalone chunks**: Processed independently, no state sharing
- **Dependent chunks**: Share KV-cache via StateStore; execute in causal order (forward: 1→2→3, backward: 3→2→1)

**Performance**: Up to **4.53× speedup** over Megatron-LM baseline; memory scales with K×ChunkSize, not max sequence length.

**Pipeline Bubble Reduction**:
| Method | Bubble Ratio | Improvement |
|--------|--------------|-------------|
| Standard 1F1B (variable) | 57.14% | — |
| State-aware 1F1B (K=1) | 54.1% | 8% better |
| State-aware 1F1B (K=2) | 47.8% | 12% better |

#### 3. Elasticity & Recovery (AnchorTP)

**Problem**: If a specific chunk causes failure (OOM or hang), traditional systems kill entire training job.

**Solution** (AnchorTP): **Elastic Tensor Parallelism**—migrate failing shard to different physical GPU without killing job.

**Failure Recovery**:
| Failure Type | Traditional Approach | AnchorTP Approach |
|--------------|----------------------|-------------------|
| OOM | Kill job, restart from checkpoint | Migrate shard to larger GPU |
| Hang/Straggler | Wait indefinitely or timeout | Migrate shard to faster GPU |
| Network partition | Job fails | Continue with available shards |

#### 4. DAG-Level Credit Assignment

**Problem**: How to assign credit when nodes have complex dependencies and only final outcome is observable?

**Solutions**:
- **SALT**: Trajectory graph analysis—step quality = f(success_rate(state), success_rate(state,action), rarity(state))
- **AgentPRM**: Promise (expected value) + Progress (marginal contribution); TD bootstrapping eliminates need for human labels
- **CRM**: Multi-agent collaborative reward—specialist evaluators + centralized aggregator; 45% reward variance reduction

**Performance**:
| Technique | Sample Efficiency | Gain |
|------------|-------------------|------|
| SALT | 25-34% fewer training steps | 3-5% absolute accuracy |
| AgentPRM | 8× fewer samples | Comparable to human-labeled PRM |
| CRM | 45% variance reduction | 7-9% rewardBench improvement |

---

### Comparison: Bubbles & Scheduling by Phase

| Feature | Phase A: Inference (Rollout) | Phase B: Training |
|---------|------------------------------|------------------|
| **Primary Bottleneck** | External Tool Latency (I/O Bound) | Compute/Sync Barriers (Compute Bound) |
| **"Bubble" Cause** | Waiting for environment/tool response | Waiting for other GPUs (Gang Schedule) |
| **Bubble Duration** | Highly variable (0.1s - 10s+) | Predictable (ms scale) |
| **Scheduling Unit** | Sample/Prompt (Queue Scheduling) | Chunk/Tensor (Gang Scheduling) |
| **State Management** | Frozen Context (Offloaded to CPU) | Active VRAM (Context Parallelism) |
| **Key Algorithm** | ROLL Flash (Async Producer-Consumer) | AnchorTP (Elastic Tensor Parallelism) |
| **Parallelism Driver** | Tool independence (GAP task graphs) | Gang schedule constraints (ChunkFlow) |
| **Primary Paper** | ROLL Flash (arXiv:2510.11345) | ChunkFlow (arXiv:2503.02356) |
| **Speedup Achieved** | 2.24× (128 GPUs) | 4.53× (7B, 256K context) |

---

## Level 3: Orchestration (The State Machine)

![DAG-state](external/images/overall_system.png)

**Objective**: Manage the lifecycle flow between Phase A (Inference) and Phase B (Training).

### Node Lifecycle State Machine

The macro-scheduler treats the entire system as a **DAG Node Lifecycle State Machine**:

```
     ┌─────────┐     tool_call      ┌──────────┐
     │         │ ──────────────────>│          │
     │ Inference│  (send to env)    │ Pending  │
     │ (Red)   │                   │ (Blue)   │
     │         │ <──────────────────│          │
     └────┬────┘    result return   └─────┬────┘
          │                              │
          │                              │
          │    ┌─────────────────────────┴────────┐
          │    │                                  │
          │    ▼                                  ▼
          │ ┌──────────┐                    ┌──────────┐
          │ │ Refining │                    │ Training  │
          │ │ (Green)  │                    │ (Yellow) │
          │ │          │◀────────────────────│          │
          │ └─────┬────┘     gradients     └──────────┘
          │       │
          └───────┴─────────────────────┐
                                ▼
                          ┌──────────────┐
                          │ Completed    │
                          └──────────────┘

Path ① (RL): Pending → Training
Path ② (SFT): Pending → Refining → Training
```

### State Transitions and DAG Implications

| Transition | Trigger | DAG Implication |
|------------|---------|-----------------|
| Inference → Pending | Tool call required | DAG node becomes blocked on external dependency |
| Pending → Inference | Tool result returns | DAG node unblocked; execution continues |
| Pending → Refining | Node selected for SFT | DAG trajectory modified (oracle injection) |
| Pending → Training | Node has reward | DAG edge weighted by reward signal |
| Refining → Training | Node corrected | DAG node becomes training example |

### Integration Challenge: Asynchrony vs. Freshness

**Problem**: The Inference Engine (Phase A) generates data using Policy π. The Training Engine (Phase B) updates Policy π to π'. If Inference gets too far ahead, it generates stale data from old policy.

**Solution** (AReaL, ROLL Flash): **Asynchronous Ratio** bounds policy version gap.

**Asynchronous Ratio Formulations**:
| System | Parameter | Definition | Optimal Value |
|---------|-----------|------------|---------------|
| **ROLL Flash** | α | Current policy version n - sample initiation version ≥ (n-α) | 2 (insensitive to model size) |
| **AReaL** | β | Inference can be β versions ahead of training | 2-4 (depends on batch size) |

**Trade-offs**:
| Value | Pros | Cons |
|-------|------|------|
| α=1 (synchronous) | Maximum freshness | Generation bottlenecks training |
| α=2 (recommended) | Near-maximal throughput, minimal staleness | Small off-policy penalty |
| α=4+ | Maximum throughput | Significant off-policy degradation |

**Training Stability**: Off-policy algorithms (GRPO, Decoupled PPO, TOPR) effectively compensate for staleness—async achieves comparable accuracy to sync with 2.24× throughput.

### DAG-Related Orchestration Challenges

**Challenge 1: Multi-Agent DAG Coordination**
- **Problem**: Multiple agents executing different DAG branches simultaneously; how to coordinate their progress?
- **Solution** (VerlTool): Unified tool API with standardized modality declarations; scheduler handles diverse tools uniformly
- **Result**: Near 2× speedup from parallel tool execution across 6 domains

**Challenge 2: Reward Propagation Through DAG**
- **Problem**: Final reward must be propagated back through DAG edges to credit all contributing nodes
- **Solutions**:
  - **AgentPRM**: Promise/Progress metrics with TD estimation—signals flow backward through trajectory DAG
  - **CRM**: Parallel evaluators feed aggregator—multi-perspective rewards capture DAG structure
  - **SALT**: Trajectory graph construction—step quality derived from graph position and outcome correlation

**Challenge 3: Dynamic DAG Topology Adaptation**
- **Problem**: DAG structure varies per query complexity; simple queries yield shallow DAGs, complex queries yield deeper DAGs
- **Solution** (GAP): Two-stage training—SFT on static graph demonstrations → RL refinement for dynamic construction
- **Open Question**: Can models learn to predict optimal DAG topology without human annotation?

---

## References

### Core Framework Papers
| Paper | URL | Summary |
|-------|-----|---------|
| **ROLL Flash** | [arXiv:2510.11345](https://arxiv.org/abs/2510.11345) | [summary](./summaries/10_roll_flash.md) - Asynchronous RL training—2.24× throughput via rollout-train decoupling |
| **ChunkFlow** | [arXiv:2503.02356](https://arxiv.org/abs/2503.02356) | [summary](./summaries/03_chunkflow.md) - Uniform chunking—4.53× speedup via state-aware scheduling |
| **AReaL** | [arXiv:2505.24298](https://arxiv.org/abs/2505.24298) | [summary](./summaries/07_areal.md) - Asynchronous RL system—η/β staleness ratios for freshness vs. throughput |
| **AnchorTP** | [arXiv:2511.11617](https://arxiv.org/abs/2511.11617) | [summary](./summaries/06_anchortp.md) - Elastic tensor parallelism—shard migration for resilience |
| **AsyncFlow** | [arXiv:2507.01663](https://arxiv.org/abs/2507.01663) | [summary](./summaries/02_asyncflow.md) - Asynchronous streaming RL framework with TransferQueue |
| **DistFlow** | [arXiv:2507.13833](https://arxiv.org/abs/2507.13833) | [summary](./summaries/01_distflow.md) - Fully distributed RL framework with multi-controller paradigm |
| **StreamRL** | [arXiv:2504.15930](https://arxiv.org/abs/2504.15930) | [summary](./summaries/08_streamrl.md) - Disaggregated stream generation with skewness-aware scheduling |
| **Verlog** | [OpenReview](https://openreview.net/forum?id=U3yTQonq10) | [summary](./summaries/04_verlog.md) - Synchronized multi-turn RL framework for long-horizon tasks |
| **Sandbox-RL** | [OpenReview](https://openreview.net/forum?id=0pFcKF2li1) | [summary](./summaries/05_sandbox_rl.md) - Multi-LLM optimization via workflow DAGs |

### DAG-Based Training
| Paper | URL | Summary |
|-------|-----|---------|
| **DAG-Math** | [arXiv:2510.19842](https://arxiv.org/abs/2510.19842) | [summary](./summaries/14_dag_math.md) - Graph-guided mathematical reasoning—logical closeness metric |
| **GAP** | [arXiv:2510.25320](https://arxiv.org/abs/2510.25320) | [summary](./summaries/15_gap.md) - Graph-based agent planning—1.74× via parallel tool execution |
| **SALT** | [arXiv:2510.20022](https://arxiv.org/abs/2510.20022) | [summary](./summaries/17_salt.md) - Step-level advantage assignment—trajectory graph analysis |

### Agentic Reasoning & Tool Use
| Paper | URL | Summary |
|-------|-----|---------|
| **VerlTool** | [arXiv:2509.01055](https://arxiv.org/abs/2509.01055) | [summary](./summaries/16_verltool.md) - Holistic agentic RL—unified tool API, near 2× speedup |
| **TAMA** | [arXiv:2510.00161](https://arxiv.org/abs/2510.00161) | [summary](./summaries/12_tama.md) - Tool-augmented multimodal agent—training-free framework |
| **VITAL** | [arXiv:2508.04416](https://arxiv.org/abs/2508.04416) | [summary](./summaries/13_thinking_with_videos.md) - Long video reasoning—visual toolbox, +13.2% on >10min videos |
| **Tricks or Traps?** | [arXiv:2508.08221](https://arxiv.org/abs/2508.08221) | [summary](./summaries/09_tricks_or_traps.md) - Deep dive into RL for LLM reasoning |

### Reward Design
| Paper | URL | Summary |
|-------|-----|---------|
| **CRM** | [arXiv:2511.16202](https://arxiv.org/abs/2511.16202) | [summary](./summaries/20_crm.md) - Multi-agent collaborative reward—specialist evaluators + aggregator |
| **AgentPRM** | [arXiv:2511.08325](https://arxiv.org/abs/2511.08325) | [summary](./summaries/19_agentprm.md) - Process reward models for agents—Promise + Progress, 8× efficiency |
| **Advantage Shaping** | [arXiv:2510.23049](https://arxiv.org/abs/2510.23049) | [summary](./summaries/18_advantage_shaping.md) - Surrogate reward maximization—unifies REINFORCE and GRPO |
| **RLVR** | [arXiv:2510.00915](https://arxiv.org/abs/2510.00915) | [summary](./summaries/11_rlvr.md) - Reinforcement learning with verifiable yet noisy rewards |

### Related Work
- **ReAct**: Synergizing Reasoning and Acting in Language Models
- **GRPO**: Group Relative Policy Optimization (DeepSeekMath)
- **GAE**: Generalized Advantage Estimation (Schulman et al., 2018)
- **MHQA Benchmarks**: HotpotQA, 2WikiMultiHopQA, Bamboogle

---

## Key Takeaways

### 1. Bubbles Are Fundamentally Different

| Aspect | Inference Bubbles | Training Bubbles |
|--------|-------------------|------------------|
| **Nature** | I/O-bound (external tools) | Compute-bound (GPU sync) |
| **Duration** | Highly variable (100× variance) | Predictable (uniform scale) |
| **Solution** | Async execution, context swapping | Elastic backfilling, chunk packing |

### 2. Asynchrony Requires Freshness Management

- **Small async ratio suffices**: α=2 achieves near-maximal throughput with minimal off-policy degradation
- **Off-policy algorithms compensate**: GRPO, Decoupled PPO, TOPR effectively handle staleness
- **Resource allocation**: 70% GPUs for rollout (bottleneck), 20% for training, 10% for refining

### 3. DAG Structure Enables Optimization

- **Dependency-aware planning** (GAP): 1.74× speedup from parallel independent sub-tasks
- **Trajectory graph analysis** (SALT): 25-34% sample efficiency gain
- **Multi-agent rewards** (CRM): 45% variance reduction through specialist evaluators

### 4. Uniform Chunking is Transformative

- **Memory predictability**: Scales with K×ChunkSize, not max sequence length
- **Pipeline efficiency**: 12% bubble reduction via state-aware 1F1B
- **Load balancing**: 4.53× speedup for long-context fine-tuning

### 5. Tool Integration Requires Standardization

- **Unified API** (VerlTool): Async capability + modality declarations enable parallel execution
- **Multimedia support**: Tools return images/video/text—DAG edges carry heterogeneous data
- **Near 2× speedup**: Parallel tool execution across 6 domains

---

## Open Research Questions

1. **Adaptive DAG Construction**: Can models learn to predict optimal subgraphs without expert annotation?
2. **Cross-Level Credit Assignment**: How to design unified reward functions accounting for DAG position, step quality, outcome?
3. **Hierarchical DAGs**: Can we compose multi-level DAGs where high-level planning triggers sub-agent DAGs?
4. **DAG Re-use**: Which sub-trajectories should be cached as reusable patterns?
5. **Multi-Agent DAG Coordination**: How to coordinate multiple agents exploring different DAG branches?

---

**Document Version**: 2.0 (Enhanced with References)
**Last Updated**: 2025-12-25
**Source Papers**: 20 summaries across Core Framework, System Architecture, Agentic Reasoning, Multi-Modal, and Related Topics
