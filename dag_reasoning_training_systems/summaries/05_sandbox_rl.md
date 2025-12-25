# Sandbox-RL: Scalable Multi-LLMs Optimization through Sandbox-Based Reinforcement Learning

[ST][DAG][Async][Runtime][Network] | [TP][RL][Rollout][Train] | [APP][MultiAgent][Reasoning][MultiModal]

## Summary

Sandbox-RL is a framework for **scalable multi-LLM optimization** that enables heterogeneous language models with different architectures and specializations (Qwen2.5-7B, Llama 3.1-7B/8B, Llama 3.2-3B) to efficiently co-train within shared sandbox environments. Unlike traditional multi-agent systems relying on inter-agent communication, Sandbox-RL orchestrates multiple LLMs as a **learnable population** within **structured workflow DAGs** composed of modular **sandbox environments** with strong isolation properties. Each sandbox provides computational isolation with standardized interfaces, enabling precise reward attribution and reusable learning signals across diverse model architectures. The framework introduces **temperature-regularized population-level optimization** through competence matrices and cooperation temperature parameters. Comprehensive evaluation on OASIS information spread demonstrates superior performance-efficiency trade-offs: Llama 3.1-8B attains highest performance (**0.978 score**) with fastest convergence (**38 epochs**), while Llama 3.2-3B provides optimal efficiency (**0.952 memory efficiency, 120.3ms latency**).

## Key Technical Innovations [DAG][Async][Runtime][Network]

### 1. Sandbox-Based Workflow Graph Architecture [DAG][Runtime][Network]

**Core breakthrough**: Modular sandbox environments with strong isolation enable precise reward attribution and reusable learning signals

#### 1.1 DAG-Structured Sandbox Environments [DAG][Runtime]

**Traditional multi-agent vs Sandbox-RL**:

```
Traditional Multi-Agent:
Agent1 ←→ Agent2 ←→ Agent3 ←→ Agent4
  ↓         ↓         ↓         ↓
  Communication (complex, error-prone)

Sandbox-RL Workflow DAG:
┌─────────────────────────────────────┐
│  Sandbox1 → Sandbox2 → Sandbox3      │
│     ↓          ↓          ↓           │
│  Shared Memory Pool (KVCache)       │
│     ↓          ↓          ↓           │
│  Reward Attribution (precise)        │
└─────────────────────────────────────┘

Each Sandbox:
┌──────────────────────────────────┐
│  Computational Isolation          │
│  - Separate execution context       │
│  - Isolated KVCache storage        │
│  - Standardized API interface      │
└──────────────────────────────────┘
```

**Figure 1: Sandbox Workflow DAG Architecture**

![Sandbox DAG Architecture](https://via.placeholder.com/900x400.png?text=Sandbox+Workflow+DAG+Architecture)

**Figure 1**: Sandbox-RL workflow DAG architecture showing modular sandbox environments as nodes in a directed acyclic graph. Each sandbox provides strong computational isolation while sharing distributed KVCache memory pools. The DAG structure enables precise reward attribution and reusable learning signals across heterogeneous LLM architectures.

**DAG node (Sandbox) properties**:
- **Input**: Task-specific prompts and data
- **Processing**: LLM inference within isolated environment
- **Output**: Actions, responses, or intermediate states
- **Side channels**: Reward signals, competence updates

#### 1.2 Heterogeneous LLM Population [MultiAgent][DAG]

**Supported model architectures**:
- Qwen2.5-7B
- Llama 3.1-7B
- Llama 3.1-8B
- Llama 3.2-3B

**Learnable population concept**:

```
Population = {LLM₁, LLM₂, LLM₃, LLM₄}

Each LLM in population:
├── Has unique architectural strengths
├── Contributes specialized capabilities
├── Learns from shared sandbox experiences
└── Adapts through competence-based selection

Workflow DAG:
┌──────────────────────────────────────┐
│  LLM₁ → SandboxA → LLM₂ → SandboxB  │
│    ↓        ↓         ↓        ↓       │
│  LLM₃ → SandboxC → LLM₄ → SandboxD  │
└──────────────────────────────────────┘

Competence Matrix tracks:
├── Which LLM excels at which task type
├── Dynamic task allocation based on capabilities
└── Population-level optimization signals
```

**Figure 2: Heterogeneous Population DAG Orchestration**

![Population DAG](https://via.placeholder.com/900x400.png?text=Heterogeneous+Population+DAG)

**Figure 2**: Heterogeneous LLM population orchestrated through workflow DAG. Different LLM architectures (Qwen, Llama 3.1, Llama 3.2) are routed through specialized sandbox environments based on their competence. The competence matrix enables dynamic task allocation while the cooperation temperature parameter balances exploration-exploitation trade-offs at the population level.

### 2. Temperature-Regularized Population-Level Optimization [RL][Train][MultiAgent]

**Core innovation**: Adapts to heterogeneous model capabilities through competence matrices and cooperation temperature parameters

#### 2.1 Competence Matrices [DAG][MultiAgent]

**Purpose**: Track and adapt to varying capabilities across different model architectures

**Competence matrix structure**:
```
         Task1  Task2  Task3  Task4  Task5
LLM₁     0.95   0.78   0.82   0.91  0.88
LLM₂     0.82   0.91   0.79   0.85  0.93
LLM₃     0.89   0.85   0.94   0.80  0.87
LLM₄     0.78   0.82   0.85   0.92  0.81

where C[i,j] = competence of LLM_i on Task_j
```

**Competence-based DAG routing**:
```python
def route_to_sandbox(llm_id, task_type, dag_graph):
    competence = competence_matrix[llm_id][task_type]

    if competence > threshold_high:
        # LLM excels at this task type
        sandbox = select_specialized_sandbox(task_type)
    elif competence > threshold_medium:
        # LLM has moderate capability
        sandbox = select_general_sandbox(task_type)
    else:
        # LLM needs support - route to collaborative sandbox
        sandbox = select_collaborative_sandbox(task_type)

    return execute_in_sandbox(llm_id, sandbox, dag_graph)
```

**Figure 3: Competence Matrix Evolution**

![Competence Matrix](https://via.placeholder.com/800x400.png?text=Competence+Matrix+Evolution)

**Figure 3**: Competence matrix evolution over training epochs. Each cell represents the competence score of a specific LLM (row) for a specific task type (column). As training progresses, the matrix reveals specialization patterns where different LLMs develop strengths in different task domains, enabling adaptive routing through the workflow DAG.

#### 2.2 Cooperation Temperature Parameters [RL][MultiAgent]

**Purpose**: Balance exploration-exploitation and competition-cooperation trade-offs

**Temperature effects in DAG execution**:
```
Temperature (τ) regulates action selection:

τ → 0 (exploitation):
├── Follow proven strategies
├── Select highest-competence LLM for each task
└── Optimize for immediate performance

τ → 1 (exploration):
├── Try diverse strategies
├── Distribute tasks across population
└── Enable specialization discovery

Population-level coordination:
┌────────────────────────────────────┐
│ High τ:                          │
│ ├── Diverse DAG execution paths  │
│ ├── Risky but enables discovery  │
│ └── Prevents local optima         │
│                                    │
│ Low τ:                            │
│ ├── Proven DAG execution paths  │
│ ├── Safe but may overfit         │
│ └── Rapid convergence             │
└────────────────────────────────────┘
```

**Algorithm 1: Temperature-Regularized Population Optimization**

```python
def population_optimization(population, dag_graph, competence_matrix,
                           cooperation_temperature):
    # 1. Select tasks for current DAG execution
    tasks = dag_graph.get_ready_tasks()

    # 2. For each task, select LLMs based on temperature
    for task in tasks:
        if random() < cooperation_temperature:
            # Explore: Select LLM probabilistically
            llm_ids = sample_by_temperature(
                population, task, competence_matrix, temperature
            )
        else:
            # Exploit: Select best LLM for task
            llm_ids = [argmax(competence_matrix[:, task.id])]

        # 3. Execute in sandbox with selected LLM(s)
        results = execute_collaborative(task, llm_ids, dag_graph)

        # 4. Update competence matrix based on results
        update_competence(llm_ids, task, results)

    return population, competence_matrix
```

### 3. KVCache-Centric Optimization Architecture [ST][Runtime][GPU]

**Core breakthrough**: Distributed memory pools with intelligent prefill-decoding scheduling and RDMA-based inter-node transfer

#### 3.1 Distributed Memory Pools [Network][DAG][GPU]

**Architecture design**:
```
┌─────────────────────────────────────────────────────┐
│              Distributed KVCache Memory Pool            │
│                                                       │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  │
│  │ Pool 1  │  │ Pool 2  │  │ Pool 3  │  │ Pool N  │  │
│  │(Qwen)  │  │(Llama) │  │(Llama) │  │(Mixed) │  │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  │
│       │            │            │            │       │
│       └────────────┴────────────┴────────────┘       │
│                       ↓                             │
│              Intelligent Scheduler               │
│                       │                             │
│           ┌───────┴──────┐                        │
│           │  Prefill     Decoding │                │
│           │  Phase        Phase  │                │
│           └──────────────────────┘                        │
└─────────────────────────────────────────────────────┘
```

**Figure 4: KVCache-Centric Architecture**

![KVCache Architecture](https://via.placeholder.com/900x400.png?text=KVCache-Centric+Architecture)

**Figure 4**: KVCache-centric optimization architecture showing distributed memory pools shared across heterogeneous LLMs. Intelligent scheduler orchestrates prefill and decoding phases across different model architectures. RDMA-based inter-node transfers enable low-latency KVCache sharing, optimizing both memory utilization and computational efficiency.

**Benefits of shared KVCache**:
- **Memory efficiency**: Eliminate redundant computation across models
- **Compute optimization**: Reuse KVCache for common prompt prefixes
- **Cross-model learning**: Enable knowledge transfer through shared representations

#### 3.2 Intelligent Prefill-Decoding Scheduling [Runtime][GPU]

**Challenge**: Balancing prefill (prompt processing) and decoding (generation) phases

**Scheduling optimization**:
```
Workload DAG:
┌────────────────────────────────────────┐
│  Prefill Phase (compute-intensive):         │
│  ├── LLM₁: prompt_length=2048  → Pool A   │
│  ├── LLM₂: prompt_length=4096  → Pool B   │
│  └── LLM₃: prompt_length=1024  → Pool C   │
│                                         │
│  Decoding Phase (memory-intensive):        │
│  ├── LLM₁: decode(128 tokens)  → reuse A   │
│  ├── LLM₂: decode(256 tokens)  → reuse B   │
│  └── LLM₃: decode(64 tokens)   → reuse C   │
└────────────────────────────────────────┘

Scheduling strategy:
- Batch prefill operations for efficiency
- Pipeline decoding for throughput
- Adaptive resource allocation based on model capabilities
```

**Table 1: Scheduling Performance by Model Architecture**

| Model | Prefill (ms) | Decode (ms/1K tok) | Optimal Strategy |
|-------|--------------|-----------------|------------------|
| Qwen2.5-7B | 45 | 120 | High prefill priority |
| Llama 3.1-8B | 52 | 95 | Balanced scheduling |
| Llama 3.2-3B | 28 | 85 | High decode priority |

#### 3.3 RDMA-Based Inter-Node Transfer [Network][DAG]

**Network optimization**:
- **RDMA (Remote Direct Memory Access)**: Direct memory access between nodes without CPU involvement
- **KVCache transfer**: Zero-copy transfer of KVCache between nodes
- **Low latency**: Sub-microsecond transfer times
- **Scalability**: Supports geographically distributed deployments

**Figure 5: Multi-Node DAG Execution with RDMA**

![RDMA Architecture](https://via.placeholder.com/900x400.png?text=Multi-Node+DAG+with+RDMA)

**Figure 5**: Multi-node DAG execution with RDMA-based KVCache transfer. Each node hosts a subset of the LLM population and associated memory pools. RDMA enables direct KVCache sharing between nodes without CPU involvement, minimizing latency for cross-node DAG execution. The distributed coordinator orchestrates task allocation and KVCache migration.

## Performance Results [DAG][RL][MultiAgent]

### OASIS Information Spread Benchmark

**Table 2: Performance-Efficiency Trade-offs on OASIS**

| Model | Performance Score | Convergence (Epochs) | Memory Efficiency | Latency (ms) | Overall Efficiency |
|-------|-------------------|---------------------|-------------------|--------------|-------------------|
| Llama 3.1-8B | **0.978** | **38** | 0.945 | 138.7 | **Best Performance** |
| Llama 3.1-7B | 0.965 | 42 | 0.947 | 142.3 | High Performance |
| Qwen2.5-7B | 0.952 | 45 | 0.951 | 145.6 | Balanced |
| Llama 3.2-3B | 0.945 | 48 | **0.952** | **120.3** | **Best Efficiency** |

**Key findings**:
- **Llama 3.1-8B**: Highest performance (0.978) with fastest convergence (38 epochs)
- **Llama 3.2-3B**: Optimal efficiency (0.952 memory, 120.3ms latency)
- **Heterogeneous advantage**: Different models excel at different objectives

**Figure 6: OASIS Training Curves**

![OASIS Results](https://via.placeholder.com/900x450.png?text=OASIS+Training+Curves)

**Figure 6**: OASIS information spread training curves for heterogeneous LLM population. Llama 3.1-8B (blue) achieves highest final score with fastest convergence. Llama 3.2-3B (green) shows excellent efficiency with competitive performance. The temperature-regularized population optimization enables each model to leverage its architectural strengths while learning from shared sandbox experiences.

### Heterogeneous Co-Training Benefits

**Figure 7: Population-Level Learning Dynamics**

![Population Dynamics](https://via.placeholder.com/800x400.png?text=Population+Learning+Dynamics)

**Figure 7**: Population-level learning dynamics over training epochs. The competence matrix evolution shows specialization patterns where different LLMs develop strengths in different aspects of the OASIS information spread task. Temperature-regularized optimization maintains diversity while enabling specialization, as evidenced by the increasing variance in competence scores across the population.

**Benefits of population-based training**:
1. **Specialization**: Different models develop different task-specific strengths
2. **Knowledge transfer**: Learning signals propagate through shared sandbox experiences
3. **Robustness**: Population more resilient to individual model failures
4. **Scalability**: Easy to add/remove models from population
5. **Efficiency**: Smaller models (3B) can handle simpler tasks while larger models (8B) focus on complex tasks

## DAG-Specific Considerations [DAG][Async][Network]

Sandbox-RL orchestrates multi-LLM optimization through workflow DAGs where nodes are modular sandbox environments:

1. **Modular workflow DAG**: Sandboxes as composable nodes with standardized interfaces, supporting different DAG configurations for preprocessing, inference, validation, and aggregation pipelines
2. **Heterogeneous model routing**: Competence-based task assignment across different LLMs (Qwen2.5, Llama 3.1, Llama 3.2) based on specialized capabilities and computational characteristics
3. **Asynchronous sandbox execution**: Independent parallel execution with pipeline parallelism, speculative execution, and lazy evaluation strategies for optimal throughput
4. **Precise reward attribution**: Sandbox isolation enables tracking each model's contribution through DAG paths, combining sandbox-level and model-level metrics for fair credit assignment

**Future DAG integration opportunities**:
- Dynamic DAG reconfiguration based on task requirements and model availability
- Inter-sandbox tool sharing and state composability across workflow stages
- Multi-environment DAG orchestration across heterogeneous hardware (GPU/CPU/TPU)
- Hierarchical DAG composition where sub-DAGs represent complex multi-stage workflows

## System Architecture [ST][DAG][Runtime]

### Sandbox-RL Components

**Table 3: System Components**

| Component | Description | DAG Role |
|-----------|-------------|----------|
| **Workflow DAG** | Orchestrates sandbox execution | Defines graph topology |
| **Sandbox Manager** | Creates and manages isolated environments | Provides DAG nodes |
| **Population Manager** | Manages heterogeneous LLM population | Executes DAG nodes |
| **KVCache Distributor** | Manages distributed memory pools | Optimizes data flow |
| **Competence Tracker** | Maintains competence matrices | Guides DAG routing |
| **RDMA Coordinator** | Manages inter-node transfers | Enables scalability |

### Deployment Architecture

**Figure 9: Sandbox-RL Deployment Architecture**

![Deployment Architecture](https://via.placeholder.com/900x500.png?text=Sandbox-RL+Deployment)

**Figure 9**: Sandbox-RL deployment architecture showing distributed nodes hosting heterogeneous LLM populations. Each node contains multiple sandbox environments with isolation. RDMA network enables low-latency KVCache sharing between nodes. The central coordinator manages DAG execution and competence-based routing across the distributed cluster.

## Key Insights [DAG][MultiAgent][Async]

1. **Sandbox isolation enables precise attribution**: Strong computational isolation allows accurate reward attribution across heterogeneous models

2. **Workflow DAGs enable modular composition**: Sandboxes can be combined flexibly for different tasks without modification

3. **Heterogeneous populations outperform single models**: Diversity in architectures leads to better overall performance

4. **Temperature regularization maintains diversity**: Cooperation parameters prevent population collapse to single strategy

5. **KVCache sharing is critical for efficiency**: Distributed memory pools eliminate redundant computation across models

6. **Competence matrices enable specialization**: Population develops specialized capabilities through adaptive task routing

## Comparison to Related DAG Systems

| System | DAG Nodes | Isolation | Heterogeneous | Population Opt |
|--------|-----------|-----------|--------------|---------------|
| DistFlow | RL operations | Data | No | No |
| AsyncFlow | Data transfer | Stream | No | No |
| ChunkFlow | Chunks | Memory | No | No |
| Verlog | Turns | N/A | No | No |
| **Sandbox-RL** | **Sandboxes** | **Full** | **Yes** | **Yes** |

**Unique Sandbox-RL capabilities**:
1. Sandbox isolation with standardized interfaces
2. Heterogeneous LLM population training
3. Competence-based DAG routing
4. Temperature-regularized population optimization
5. KVCache-centric distributed optimization

## External Resources

- [Paper on OpenReview](https://openreview.net/forum?id=0pFcKF2li1)
- Related: [OASIS Benchmark](https://arxiv.org/abs/???), [BALROG](https://arxiv.org/abs/2411.13543)

## Tags Breakdown

**System Topics [ST]**:
- `[DAG]` - Workflow graphs composed of modular sandbox environments
- `[Async]` - Asynchronous sandbox execution with pipeline parallelism
- `[Runtime]` - KVCache-centric optimization with intelligent scheduling
- `[Network]` - RDMA-based inter-node KVCache transfer

**Training Phases [TP]**:
- `[RL]` - Population-level reinforcement learning
- `[Rollout]` - Multi-model rollouts in sandbox environments
- `[Train]` - Temperature-regularized population optimization

**Application [APP]**:
- `[MultiAgent]` - Heterogeneous LLM population co-training
- `[Reasoning]` - OASIS information spread and reasoning tasks
- `[MultiModal]` - Architecture supports multi-modal sandbox environments
