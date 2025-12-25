# Technical Analysis: Multi-Level DAG Design for Agentic Reasoning Training Systems

This document synthesizes insights from 20 research papers with the 4-level DAG framework, identifying key challenges and solutions at each level of the system architecture.

---

## Table of Contents

1. [Level 1: Data/Dataset Layer](#level-1-datadataset-layer)
2. [Level 2: Training Chunks/Node-Chunks Layer](#level-2-training-chunksnode-chunks-layer)
3. [Level 3: Rollout Phases Layer](#level-3-rollout-phases-layer)
4. [Level 4: Scheduling by DAG-Node States Layer](#level-4-scheduling-by-dag-node-states-layer)
5. [Cross-Level Integration Challenges](#cross-level-integration-challenges)

---

## Level 1: Data/Dataset Layer

### Overview

At the foundational level, training data is structured as **DAG trajectories** where nodes represent agents/tools and edges represent data flow dependencies. A single training sample is not a flat sequence but a **subgraph** extracted from a larger "super-graph" of all available capabilities.

![DAG_data](external/images/DAG_def.png)

### Key Challenges

| Challenge | Description | Why It Matters |
|-----------|-------------|----------------|
| **DAG Representation** | How to encode reasoning trajectories as DAGs rather than linear sequences | Enables parallel execution and credit assignment |
| **Subgraph Extraction** | Identifying optimal subgraphs for specific tasks from the capability super-graph | Reduces search space and improves efficiency |
| **Quality Annotation** | Labeling DAG quality beyond final answer correctness | Enables credit assignment for intermediate steps |
| **Multi-Modal Data Flow** | Handling heterogeneous data types (text, images, video) across DAG edges | Required for tool-augmented reasoning |

### Technical Solutions from Research

#### 1.1 DAG Representation Schemas

**Graph-Guided Reasoning (DAG-Math)**: CoT as rule-based DAG where nodes = derivation states, edges = rule applications

```python
# DAG-Math structured format
class DAGNode:
    state: str  # Intermediate derivation state
    rule: str   # Rule application to reach this state
    justification: str  # Why this rule was chosen

class DAGEdge:
    source: DAGNode
    target: DAGNode
    rule_application: str  # How to transform source → target

class TrajectoryDAG:
    nodes: List[DAGNode]
    edges: List[DAGEdge]
    initial_state: DAGNode
    final_state: DAGNode
```

**Key Insight**: Structured DAG format enables evaluation beyond PASS@k through **logical closeness** metric—how well trajectories follow valid derivation paths.

**Graph-Based Agent Planning (GAP)**: Dependency-aware task graphs where nodes = sub-tasks, edges = data dependencies

```
┌─────────────────────────────────────────────────────────────────┐
│                    GAP Task Graph Structure                     │
├─────────────────────────────────────────────────────────────────┤
│  Question: "Compare GDP of France, Germany, Italy"             │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                       │
│  │ Search:  │  │ Search:  │  │ Search:  │  (PARALLEL)           │
│  │ France   │  │ Germany  │  │ Italy    │                       │
│  │ GDP      │  │ GDP      │  │ GDP      │                       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                       │
│       │             │             │                              │
│       └──────────┬──┴─────────────┘                              │
│                    ▼                                       (SEQUENTIAL)│
│         ┌─────────────────────┐                                 │
│         │ Compare & Synthesize│                                 │
│         └─────────────────────┘                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Performance**: GAP achieves 1.74× speedup through parallel execution of independent sub-tasks.

#### 1.2 Subgraph Extraction and Pruning

**Challenge**: The capability super-graph contains thousands of potential tools/agents. Extracting the optimal subgraph for a specific query is non-trivial.

**Solution Approaches**:

| Approach | Paper | Mechanism |
|----------|-------|-----------|
| **Static Subgraph Annotation** | DAG-Math | Expert-annotated DAGs with rule applications |
| **Learned Subgraph Prediction** | GAP | SFT on graph-annotated MHQA data → RL refinement |
| **Dynamic Construction** | TAMA, VITAL | Agent decides which tools to invoke during execution |

**Training Pipeline (GAP)**:
```
Stage 1: SFT on Graph Demonstrations
- Collect multi-hop questions with gold evidence paths
- Annotate dependencies between information retrieval steps
- Train model to generate dependency-aware task graphs

Stage 2: RL with Correctness Rewards
- Sample queries where tool-based reasoning provides maximum value
- Reward: correctness of final answer + efficiency bonus for parallelization
```

**Result**: GAP achieves +9.4% accuracy improvement on HotpotQA while reducing tool invocation latency by 1.74×.

#### 1.3 Quality Annotation and Credit Assignment

**Problem**: How to assign credit/blame across DAG nodes when only final outcome is observable?

**Trajectory Graph Analysis (SALT)**: Construct graphs from multiple rollouts to identify high-quality steps

```
┌─────────────────────────────────────────────────────────────────┐
│              SALT Trajectory Graph Construction                 │
├─────────────────────────────────────────────────────────────────┤
│  Input: N trajectories for same prompt                          │
│                                                                  │
│  Trajectory 1:  → A → B → C → D → SUCCESS                       │
│  Trajectory 2:  → A → B' → C → D → SUCCESS                     │
│  Trajectory 3:  → A → B → C' → E → FAILURE                     │
│  Trajectory 4:  → A → B' → C' → D → SUCCESS                    │
│                                                                  │
│  Graph Analysis:                                                 │
│  ├── Node Features:                                             │
│  │   ├── Frequency: How often state appears                     │
│  │   ├── Success Rate: P(success │ state)                      │
│  │   └── Transition Entropy: Diversity of outgoing actions      │
│  │                                                              │
│  └── Step Quality Score:                                        │
│      Q(s, a) = α × success_rate(s) + β × success_rate(s, a)     │
│               + γ × rarity(s)                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Performance**: SALT achieves 3-5% absolute gains on long-horizon tasks with 25-34% fewer training steps.

**Promise and Progress (AgentPRM)**: Redefine PRM for agents without binary correctness labels

| Metric | Definition | Purpose |
|--------|------------|---------|
| **Promise (V)** | E[R_total │ state = s] | Expected value of current state toward goal |
| **Progress (A)** | Promise(s') - Promise(s) | Marginal contribution of action |

**TD Estimation with GAE**:
```
# Bootstrap labels from outcome rewards
V(s) ← V(s) + α × [R + γ·V(s_next) - V(s)]  # TD update

# Generalized Advantage Estimation
A_t = Σ_{l=0}^∞ (γλ)^l δ_{t+l}
where δ_t = R_t + γ·V(s_{t+1}) - V(s_t)
```

**Sample Efficiency**: 8× fewer samples required compared to human-labeled PRMs.

#### 1.4 Multi-Modal Data Flow

**Multimedia-Returning Tools (TAMA, VITAL)**: Tools return images/videos that flow along DAG edges

**TAMA Visual Toolbox**:

| Tool | Input | Output | Use Case |
|------|-------|--------|----------|
| Frame Extractor | Video URL | Image sequence | Show specific frames |
| Object Detector | Image | Bounding boxes | Locate objects |
| OCR Reader | Image | Extracted text | Read labels |

**VITAL Visual Toolbox for Long Video Reasoning**:

| Tool | Input | Output | Use Case |
|------|-------|--------|----------|
| Frame Sampler | Video, timestamps | Image frames | Dense sampling |
| Dense Sampler | Video, time range | Frame sequence | Continuous segments |
| Action Detection | Video clip | Action + confidence | Identify actions |
| Object Detection | Video frame | Bounding boxes | Locate objects |

**Key Insight**: On-demand frame sampling enables efficient long-video reasoning without processing entire video—VITAL achieves +13.2% improvement on videos >10 minutes.

### Design Recommendations for Level 1

1. **Structured DAG Format**: Adopt annotation schemas that make dependencies explicit (GAP-style task graphs, DAG-Math rule applications)

2. **Subgraph Pruning**: Use learned models to predict which subgraph branches are relevant for specific queries; prune unused capabilities

3. **Multi-Modal Support**: Design tool APIs to return structured data (images, bounding boxes, JSON) that can flow through DAG edges

4. **Quality Signals**: Collect trajectory graphs from multiple rollouts to estimate node/edge quality without requiring per-step human labels

---

## Level 2: Training Chunks/Node-Chunks Layer

### Overview

Once DAG data is structured, the **Elastic Scheduler** manages physical execution across distributed GPUs. It must handle: (1) context parallelism for large nodes (requiring gang scheduling), (2) bubble detection and filling with independent chunks, and (3) elasticity across physically distant devices.

![DAG-chunk](external/images/chunk-node-flow.png)

### Key Challenges

| Challenge | Description | Why It Matters |
|-----------|-------------|----------------|
| **Gang Scheduling** | Coordinating multiple GPUs for sequence parallel chunks | Required for long-context processing (Ring Attention) |
| **Bubble Detection** | Identifying idle time during synchronization barriers | GPU underutilization wastes training capacity |
| **Elastic Backfilling** | Filling bubbles with independent chunks from other DAG branches | Maximizes cluster throughput |
| **Cross-Rack Coordination** | Managing chunks distributed across physically distant GPUs | Enables scaling beyond single machine |

### Technical Solutions from Research

#### 2.1 Uniform Chunking and Context Parallelism

**ChunkFlow**: Long-context fine-tuning via uniform chunking

```
┌─────────────────────────────────────────────────────────────────┐
│              ChunkFlow Uniform Chunking Strategy                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Problem: Variable-length chunks cause load imbalance           │
│  Solution: Uniform chunking with cross-chunk dependencies       │
│                                                                  │
│  Input Sequence (32K tokens):                                   │
│  ├─ Chunk 1: tokens [0, 4096)                                  │
│  ├─ Chunk 2: tokens [4096, 8192)                               │
│  ├─ Chunk 3: tokens [8192, 12288)                              │
│  └─ Chunk 4: tokens [12288, 16384)                             │
│                                                                  │
│  Gang Schedule Constraint:                                      │
│  Chunks 1-4 must execute simultaneously on 4 GPUs               │
│  (Ring Attention requires synchronized progress)                │
│                                                                  │
│  Cross-Chunk Dependencies (DAG edges):                          │
│  Chunk 2 depends on Chunk 1 output (attention mask)            │
│  Chunk 3 depends on Chunk 2 output                              │
│  └─ But: All chunks can process local tokens in parallel      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Performance**: ChunkFlow achieves 1.5× throughput improvement on 32K token sequences.

**AnchorTP**: Elastic tensor parallelism with gang scheduling

| Failure Scenario | AnchorTP Response | Recovery Mechanism |
|------------------|-------------------|-------------------|
| GPU failure during gang schedule | Elastic replication | Re-replicate shards to healthy GPUs |
| Network partition | Continue with available shards | Degraded performance, not failure |
| Straggler GPU | Async checkpoint migration | Migrate shard to faster GPU |

**Key Innovation**: Decouples logical tensor parallelism from physical device mapping—shards can migrate during training.

#### 2.2 Bubble Detection and Filling

**The Bubble Problem**:

```
Timeline WITHOUT bubble filling:
GPU 0: [Chunk1] [idle...] [Chunk1] [Chunk1] [idle...]
GPU 1: [Chunk1] [idle...] [Chunk1] [Chunk1] [idle...]
GPU 2: [Chunk1] [idle...] [Chunk1] [Chunk1] [idle...]
GPU 3: [Chunk1] [idle...] [Chunk1] [Chunk1] [idle...]
GPU 4: [idle...] [idle...] [idle...] [idle...] [idle...]

Timeline WITH bubble filling (Elastic Scheduler):
GPU 0: [Chunk1] [SmallA] [Chunk1] [SmallC] [SmallB]
GPU 1: [Chunk1] [SmallB] [Chunk1] [SmallA] [SmallD]
GPU 2: [Chunk1] [SmallC] [Chunk1] [SmallB] [SmallA]
GPU 3: [Chunk1] [SmallD] [Chunk1] [SmallD] [SmallC]
GPU 4: [SmallA] [SmallB] [SmallC] [SmallD] [SmallA]
```

**ROLL Flash Queue Scheduling**: Fine-grained parallelism at sample level

| Configuration | Generation Time | Speedup |
|---------------|-----------------|---------|
| Sync Batch | 125s | 1.0× |
| Queue (0 add) | 58s | 2.16× |
| Queue (16 add) | 37s | 3.38× |

**Key Insight**: Treat each prompt as independent task rather than processing batch as unit—reduces straggler effects.

**Prompt Replication (ROLL Flash)**: Parallel execution of multi-candidate decoding

```
Traditional: Prompt A → Worker 1 → [A1, A2, ..., A16] (bottleneck)

Prompt Replication:
Prompt A1 → Worker 1 → A1
Prompt A2 → Worker 2 → A2
...
Prompt A16 → Worker 16 → A16
```

**Performance**: 1.30-1.95× speedup depending on batch configuration.

#### 2.3 Elasticity and Cross-Rack Coordination

**DistFlow**: Fully distributed RL framework for scalable post-training

```
┌─────────────────────────────────────────────────────────────────┐
│                    DistFlow Architecture                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Worker Nodes (Distributed):                                   │
│  ├── Worker 1: Rollout on GPU 0-3                              │
│  ├── Worker 2: Rollout on GPU 4-7                              │
│  ├── Worker 3: Rollout on GPU 8-11                             │
│  └── Worker N: ...                                              │
│                                                                  │
│  Parameter Server:                                              │
│  └── Coordinates weight updates across workers                  │
│                                                                  │
│  Elasticity:                                                    │
│  ├── Workers can join/leave during training                    │
│  ├── Stragglers don't block progress (async updates)           │
│  └── Load balancing via dynamic work assignment                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**AsyncFlow**: Asynchronous streaming RL framework

**Key Innovation**: Streaming gradient updates rather than batch synchronization—worker sends updates as soon as mini-batch completes, no need to wait for other workers.

**StreamRL**: Disaggregated stream generation

| Component | Responsibility | Scaling Factor |
|-----------|---------------|----------------|
| Stream Generator | Generates token streams | Linear with workers |
| Compute Engine | Processes streams | Linear with GPUs |
| Storage | Stores intermediate results | Decoupled |

**Performance**: StreamRL achieves 2.5× throughput improvement on 128 GPUs vs synchronous baseline.

### Design Recommendations for Level 2

1. **Uniform Chunking**: Adopt ChunkFlow-style uniform chunking for predictable resource allocation

2. **Gang Scheduling with Elasticity**: Use AnchorTP-style elastic tensor parallelism—allow shards to migrate during training

3. **Queue Scheduling**: Implement ROLL Flash-style queue scheduling at sample level, not batch level

4. **Bubble Filling**: Actively detect idle time during gang schedules and fill with independent chunks

5. **Cross-Rack Awareness**: Design schedulers that are topology-aware—minimize cross-rack communication for gang-scheduled chunks

---

## Level 3: Rollout Phases Layer

### Overview

The rollout layer manages **asynchronous execution** of agentic reasoning, where high-latency tool calls (video processing, web search) cause GPU bubbles if not handled properly. The system implements **partial rollouts**—suspending agent state during external tool execution and filling bubbles with other work.

![DAG-rollout](external/images/partial_rollout.png)

### Key Challenges

| Challenge | Description | Why It Matters |
|-----------|-------------|----------------|
| **Suspended State Management** | Caching and restoring agent contexts during tool calls | Enables bubble filling without losing progress |
| **Dynamic Batching** | Combining active reasoning and returning tool results in same batch | Maximizes GPU utilization |
| **Tool Latency Variance** | Some tools (video) take seconds, others (code) take milliseconds | Creates extreme tail latency |
| **Speculative Execution** | Proceeding with placeholder results before actual tool returns | Reduces wait time for slow tools |

### Technical Solutions from Research

#### 3.1 Asynchronous Rollout-Train Decoupling

**ROLL Flash**: Rollout-train decoupling with producer-consumer model

```
┌─────────────────────────────────────────────────────────────────┐
│                    ROLL Flash Async Architecture                 │
├─────────────────────────────────────────────────────────────────┤
│  Rollout Stage          │           Training Stage                │
│  (Inference GPUs)       │           (Training GPUs)               │
│  ┌──────────────────┐   │   ┌──────────────────────────────────┐ │
│  │  LLMProxy        │   │   │  AsyncController                 │ │
│  │  ├─ Worker 1     │   │   │  ├─ get_batch (from SampleBuffer)│ │
│  │  ├─ Worker 2     │   │   │  ├─ train_step                   │ │
│  │  └─ Worker N     │   │   │  └─ model_update (broadcast)     │ │
│  └────────┬─────────┘   │   └──────────────────────────────────┘ │
│           │             │                    ↑                    │
│           ▼             │                    │                    │
│  ┌──────────────────┐   │            ┌──────┴───────┐            │
│  │  EnvManager 1-N  │   │            │  SampleBuffer │            │
│  │  └─ BaseEnv      │───┼────────────│  (Trajectories)│          │
│  │  └─ Event Loop   │   │            └──────────────┘            │
│  └──────────────────┘   │                                        │
└─────────────────────────────────────────────────────────────────┘
```

**Asynchronous Ratio α**: Bounds policy version gap between current policy and policy that initiated sample generation

| Variable | Optimal α | Trade-off |
|----------|-----------|-----------|
| Model Size (0.6B-8B) | 2 | Insensitive |
| Sequence Length 4K | 1 | Lower for short sequences |
| Sequence Length 32K | 2 | Higher for long sequences |
| Rollout Size 32 | 4 | Higher for large rollouts |
| Rollout Size 256 | 2 | Lower for frequent updates |

**Performance**: ROLL Flash achieves 2.24× throughput improvement on 128 GPUs with α=2.

#### 3.2 Environment-Level Asynchronous Rollout

**Problem**: In agentic pipelines, trajectory completion varies wildly—some finish in seconds, others extend to minutes due to environment initialization and network latency.

**ROLL Flash Solution**: Decompose trajectories into fine-grained interaction units

```
┌─────────────────────────────────────────────────────────────────┐
│         Environment-Level Asynchronous Rollout                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Traditional Synchronous:                                       │
│  Trajectory 1: [step1] [step2] [step3] ... (5 min total)       │
│  Trajectory 2: [WAIT for Traj 1] [step1] [step2] ...            │
│  Trajectory 3: [WAIT for Traj 2] ...                           │
│                                                                  │
│  Environment-Level Async:                                        │
│  Trajectory 1: [step1] → pending → [step2] → pending → ...      │
│  Trajectory 2: [step1] → pending → [step2] ...                  │
│  (Both can be in flight simultaneously)                          │
│                                                                  │
│  Speedup with (μ=10s, σ=5s) latency:                            │
│  │ Environment │ Sync Time │ Async Time │ Speedup │             │
│  │ SWE         │ 10.22h    │ 8.32h      │ 1.23×   │             │
│  │ ALFWorld    │ 13.37h    │ 8.44h      │ 1.58×   │             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 3.3 Redundant Environment Rollout

**Problem**: Environment instability (fail-slow, fail-stop) creates bottlenecks.

**ROLL Flash Solution**: Two tunable controls
1. **num_env_groups**: More concurrent environment groups
2. **group_size**: More candidate trajectories per group

**Performance** (μ=10, σ=5 latency, batch=256):

| Configuration | num_groups × group_size | Step Time | Speedup |
|---------------|------------------------|-----------|---------|
| Baseline | 32 × 8 | 243s | 1.0× |
| Config 1 | 36 × 9 | 45s | **5.40×** |

**Key Finding**: Increasing num_env_groups more effective than group_size.

#### 3.4 Unified Tool Management

**VerlTool**: Standardized tool API with modular plugin architecture

```python
class BaseTool(ABC):
    @abstractmethod
    def get_schema(self) -> ToolSchema:
        """Return tool specification for LLM prompting."""
        pass

    @abstractmethod
    async def execute(self, inputs: Dict[str, Any]) -> ToolOutput:
        """Execute tool with given inputs."""
        pass

    @property
    def modality(self) -> Modality:
        """Return output modality (text/image/video/structured)."""
        pass
```

**Supported Tool Categories**:

| Tool Type | Modality | Example | Async Execution |
|-----------|----------|---------|-----------------|
| Code Execution | Text | Python interpreter | Yes |
| Web Search | Text | Google API | Yes |
| Database | Structured | PostgreSQL | Yes |
| Vision Processing | Image | OCR, object detection | Yes |
| File Operations | Text/Mixed | Read, write, glob | Yes |

**Performance**: VerlTool achieves 1.8× average speedup from parallel tool execution across 6 domains.

#### 3.5 Multi-Turn Multi-Modal Trajectory Format

**VerlTool Formalization**: ARLT trajectories extend RLVR with multi-turn interactions and multi-modal observations

```
Trajectory Structure:

Turn 1:
├── Observation: o₁ = {text: prompt, image: screenshot.png}
├── Action: a₁ = tool_call("code_interpreter", code="...")
└── Reward: r₁ = intermediate_feedback

Turn 2:
├── Observation: o₂ = {text: output, image: new_screen.png}
├── Action: a₂ = tool_call("web_search", query="...")
└── Reward: r₂ = intermediate_feedback

...

Final Turn:
├── Observation: oₙ = {text: accumulated_context}
├── Action: aₙ = final_answer(text)
└── Reward: rₙ = correctness_score

Total Reward: R = Σ rᵢ + r_final
```

### Design Recommendations for Level 3

1. **Rollout-Train Decoupling**: Implement producer-consumer model with SampleBuffer—use asynchronous ratio α=2 for most scenarios

2. **Queue Scheduling**: Process prompts as independent tasks rather than batched units—reduces straggler effects

3. **Prompt Replication**: For multi-candidate decoding, expand each prompt into independent tasks

4. **Environment-Level Async**: Decompose trajectories into fine-grained interaction units for immediate dispatch

5. **Redundant Environments**: Use num_env_groups for resilience more than group_size

6. **Unified Tool API**: Standardize tool interfaces with async execution support

---

## Level 4: Scheduling by DAG-Node States Layer

### Overview

The macro-architecture orchestrates the **node lifecycle state machine** (Inference → Pending → Refining → Training), managing the flow of data through multiple engines. Each node transitions between states based on its dependencies and system conditions.

![DAG-state](external/images/overall_system.png)

### Key Challenges

| Challenge | Description | Why It Matters |
|-----------|-------------|----------------|
| **State Transitions** | Managing node flow through Inference → Pending → Refining → Training | Determines throughput and data quality |
| **Dual Pathways** | Orchestrating RL vs. SFT data flows | Requires different processing pipelines |
| **Weight Synchronization** | Keeping inference and training engines aligned | Prevents training on stale policy |
| **Resource Contention** | Balancing allocation between Inference, Refining, and Training engines | Maximizes cluster utilization |

### Technical Solutions from Research

#### 4.1 Node Lifecycle State Machine

```
┌─────────────────────────────────────────────────────────────────┐
│                    Node Lifecycle State Machine                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│     ┌─────────┐     tool_call      ┌──────────┐                │
│     │         │ ──────────────────>│          │                │
│     │ Inference│  (send to env)    │ Pending  │                │
│     │ (Red)   │                   │ (Blue)   │                │
│     │         │ <──────────────────│          │                │
│     └────┬────┘    result return   └─────┬────┘                │
│          │                              │                        │
│          │                              │                        │
│          │    ┌─────────────────────────┴────────┐              │
│          │    │                                  │              │
│          │    ▼                                  ▼              │
│          │ ┌──────────┐                    ┌──────────┐        │
│          │ │ Refining │                    │ Training  │        │
│          │ │ (Green)  │                    │ (Yellow) │        │
│          │ │          │                    │          │        │
│          │ │ SFT data │◀───────────────────│ RL update │        │
│          │ └─────┬────┘     gradients     └──────────┘        │
│          │       │                                               │
│          └───────┴─────────────────────┐                        │
│                                      ▼                         │
│                            ┌──────────────┐                    │
│                            │ Completed    │                    │
│                            └──────────────┘                    │
│                                                                  │
│  Path ① (RL): Pending → Training                               │
│  Path ② (SFT): Pending → Refining → Training                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**State Transitions**:

| Transition | Trigger | Action |
|------------|---------|--------|
| Inference → Pending | Tool call required | Suspend context, send to environment |
| Pending → Inference | Tool result returns | Resume with observation |
| Pending → Refining | Node selected for SFT | Apply oracle/correction |
| Pending → Training | Node has reward | Add to RL batch |
| Refining → Training | Node corrected | Add to SFT batch |
| Training → Completed | Gradient update applied | Node lifecycle complete |

#### 4.2 Reward Design and Credit Assignment

**Advantage Shaping as Surrogate Reward Maximization**: Unifies REINFORCE and advantage-shaping approaches

```
Standard GRPO:
A = R - mean(group_rewards)

Hard-Example Up-Weighting:
A_weighted = A × w(sample)
where w(correct) = 1.0, w(incorrect) = 2.0

Equivalent Surrogate Reward:
R_surrogate = {
    R            if sample is correct
    R × 2 - λ    if sample is incorrect  (λ = regularization)
}
```

**Key Insight**: Hard-example up-weighting is not ad-hoc—it's principled reward-level regularization.

**Multi-Agent Collaborative Reward (CRM)**: Specialist evaluators + centralized aggregator

```
┌─────────────────────────────────────────────────────────────────┐
│                    CRM Aggregator Architecture                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Specialist Evaluators (parallel):                              │
│  ├── Factuality Agent → s_factuality                            │
│  ├── Helpfulness Agent → s_helpfulness                          │
│  ├── Safety Agent → s_safety                                    │
│  └── Style Agent → s_style                                      │
│                                                                  │
│  Global Evaluators (parallel):                                  │
│  ├── Ranker → s_ranker                                          │
│  └── Embedding similarity → s_sim                               │
│                                                                  │
│  Centralized Aggregator:                                         │
│  R_total = α_correctness × R_correctness                        │
│          + α_agreement × R_agreement                            │
│          + α_diversity × R_diversity                            │
│          + α_penalty × R_penalty                                │
│                                                                  │
│  where:                                                         │
│    R_correctness = mean(specialist_scores)                      │
│    R_agreement = 1 - std(specialist_scores)                    │
│    R_diversity = entropy(response_distribution)                 │
│    R_penalty = -λ_repeat × repetition_count                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Performance**: CRM achieves 7-9% improvement on rewardBench while reducing reward variance by 45%.

#### 4.3 Weight Synchronization

**AReaL**: Large-scale asynchronous RL system for language reasoning

```
┌─────────────────────────────────────────────────────────────────┐
│                      AReaL Async Architecture                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Inference Workers:                                             │
│  ├── Worker 1: Generate trajectories with policy π             │
│  ├── Worker 2: Generate trajectories with policy π             │
│  └── ... (all using same policy version)                        │
│                                                                  │
│  Training Workers:                                               │
│  ├── Worker 1: Compute gradients on batch                       │
│  ├── Worker 2: Compute gradients on batch                       │
│  └── ... (gradient accumulation)                                │
│                                                                  │
│  Parameter Server:                                               │
│  └── Accumulates gradients → broadcasts new weights             │
│                                                                  │
│  Asynchronous Ratio β:                                          │
│  └── Inference workers can be β versions ahead of training      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Key Innovation**: Separates generation and training into separate resource pools with asynchronous weight synchronization.

#### 4.4 Refiner and Oracle Injection

**Sandbox-RL**: Scalable multi-LLM optimization via workflow DAGs

```
┌─────────────────────────────────────────────────────────────────┐
│                    Sandbox-RL Refinement Pipeline                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input: Raw trajectory from Inference Engine                    │
│                                                                  │
│  Refiner Operations:                                             │
│  ├── Oracle Injection: Replace failed steps with ground truth   │
│  ├── Error Correction: Fix syntax/logic errors                 │
│  ├── Style Normalization: Ensure consistent formatting          │
│  └── Verification: Validate against environment constraints    │
│                                                                  │
│  Output: Clean SFT data for supervised training                 │
│                                                                  │
│  Quality Control:                                                │
│  ├── Acceptance rate: % of trajectories passing refinement      │
│  ├── Rejection rate: % of trajectories discarded                │
│  └── Modification rate: % of tokens changed                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Design Recommendations for Level 4

1. **State Machine Design**: Implement clear state transitions with triggers and actions for each node lifecycle stage

2. **Dual Pathways**: Maintain separate pipelines for RL (Pending → Training) and SFT (Pending → Refining → Training)

3. **Asynchronous Weight Sync**: Use asynchronous ratio β to balance throughput and freshness

4. **Multi-Perspective Rewards**: Employ specialist evaluators with centralized aggregator for stable optimization

5. **Refiner Pipeline**: Implement oracle injection and error correction before adding nodes to SFT batch

---

## Cross-Level Integration Challenges

### Challenge 1: Data Flow Across Levels

**Problem**: DAG nodes must flow seamlessly from Level 1 (dataset) → Level 2 (chunks) → Level 3 (rollout) → Level 4 (scheduling)

**Solution Approach**:

```
Level 1: DAG Structure Definition
├── Nodes: Agents/Tools with metadata
├── Edges: Data dependencies
└── Subgraph: Optimal path for specific task

Level 2: Physical Chunking
├── Uniform chunking for large nodes (gang schedule)
├── Bubble detection and backfilling
└── Elasticity across distributed GPUs

Level 3: Asynchronous Execution
├── Partial rollouts for tool calls
├── Suspended state management
└── Dynamic batching

Level 4: State Machine Orchestration
├── Node lifecycle transitions
├── Reward assignment
└── Weight synchronization
```

### Challenge 2: Credit Assignment Across DAG Levels

**Problem**: How to assign credit when nodes execute across multiple levels with different timing characteristics?

**Synthesized Solution**:

| Technique | Level | Mechanism |
|-----------|-------|-----------|
| **Logical Closeness** | L1 | DAG adherence metric (DAG-Math) |
| **Step Quality Scores** | L1 | Trajectory graph analysis (SALT) |
| **Promise/Progress** | L1/L3 | State value and action contribution (AgentPRM) |
| **Advantage Shaping** | L4 | Surrogate reward optimization |
| **Multi-Agent Rewards** | L4 | Specialist evaluators (CRM) |

**Unified Credit Assignment**:
```
R_total = R_outcome + Σ R_step_i

where:
R_outcome = final correctness (from Level 4)
R_step_i = f(DAG_position, step_quality, promise_improvement)
```

### Challenge 3: Resource Allocation Trade-offs

**Problem**: Limited GPU resources must be allocated across Inference, Training, Refining, and Environment engines.

**Synthesized Insights**:

| Resource | Primary Consumer | Optimization Strategy |
|----------|------------------|----------------------|
| **Inference GPUs** | Rollout generation | Queue scheduling, prompt replication |
| **Training GPUs** | Gradient updates | Elastic chunking, bubble filling |
| **Environment** | Tool execution | Redundant env groups, async dispatch |
| **Refiner** | SFT data generation | Oracle injection, selective refinement |

**AReaL Resource Allocation**:
- 70% GPUs for rollout (inference)
- 20% GPUs for training
- 10% GPUs for refining

**Justification**: Rollout is bottleneck (>70% of time)—allocate proportional resources.

### Challenge 4: Asynchrony vs. Freshness Trade-off

**Problem**: Asynchronous execution improves throughput but risks training on stale policies.

**Synthesized Guidelines**:

| System | Async Parameter | Recommended Value | Rationale |
|--------|----------------|-------------------|-----------|
| **ROLL Flash** | α (policy gap) | 2 | Balances throughput and freshness |
| **AReaL** | β (version gap) | 2-4 | Depends on training batch size |
| **DistFlow** | Worker staleness | 3 updates | Allows gradient accumulation |
| **VerlTool** | Tool timeout | 30s | Prevents hanging on slow tools |

**Monitoring Metrics**:
- Average policy version gap
- Gradient staleness distribution
- Training stability (reward variance)
- Sample efficiency (samples to convergence)

---

## Summary and Future Directions

### Key Takeaways

1. **DAG is the Unifying Abstraction**: All 4 levels use DAG as core representation—data structure, execution plan, rollout dependency, state machine

2. **Asynchrony is Essential**: Synchronous execution creates unacceptable bottlenecks at all levels—chunking (L2), rollout (L3), training (L4)

3. **Elasticity Enables Scaling**: Gang scheduling with bubble filling (L2), partial rollouts (L3), distributed workers (L4) all contribute to linear scaling

4. **Credit Assignment is Multi-Level**: Node-level (L1), step-level (L3), trajectory-level (L4) rewards combine for effective learning

5. **Specialization Beats Generalization**: Specialist tools (TAMA, VITAL), specialist evaluators (CRM), specialist engines (Refiner) outperform monolithic approaches

### Open Research Questions

1. **Adaptive DAG Construction**: Can models learn to predict optimal subgraphs without expert annotation?

2. **Cross-Level Credit Assignment**: How to design unified reward functions that account for DAG position, step quality, and outcome?

3. **Hierarchical DAGs**: Can we compose multi-level DAGs where high-level planning triggers sub-agent DAGs?

4. **DAG Re-use and Caching**: Which sub-trajectories should be cached as reusable patterns?

5. **Multi-Agent DAG Coordination**: How to coordinate multiple agents exploring different DAG branches in parallel?

### Recommended Reading Order

For understanding the full system:

1. **Level 1**: DAG-Math, GAP (DAG representation and subgraph extraction)
2. **Level 2**: ChunkFlow, ROLL Flash (chunking and scheduling)
3. **Level 3**: VerlTool, AgentPRM (async rollout and tool use)
4. **Level 4**: AReaL, CRM (system architecture and reward design)

For implementation focus:

1. **Scheduling**: ROLL Flash, AsyncFlow, AReaL
2. **Credit Assignment**: SALT, AgentPRM, Advantage Shaping
3. **Tool Integration**: VerlTool, TAMA, VITAL
4. **Multi-Modal**: VITAL (video), TAMA (procedural), VerlTool (unified)

---

**Document Version**: 1.0
**Last Updated**: 2025-12-25
**Source Papers**: 20 summaries across Core Framework, System Architecture, Agentic Reasoning, Multi-Modal, and Related Topics
