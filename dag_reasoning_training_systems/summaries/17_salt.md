# SALT: Step-level Advantage Assignment for Long-horizon Agents via Trajectory Graph
[ST][DAG][RL] | [TP][Train][Reward] | [APP][Agent][Reasoning]

## Summary

SALT addresses a fundamental challenge in group-based RL algorithms like GRPO: **uniform reward assignment across all actions** in multi-step trajectories leads to training instability and suboptimal policies. In long-horizon agent tasks, beneficial and detrimental actions are entangled across interactions, but sparse outcome-based rewards cannot distinguish between good and bad steps. SALT introduces a **lightweight framework for fine-grained advantage assignment** derived solely from outcome rewards—no additional reward models or human annotations required. The key innovation is constructing a **trajectory graph** from multiple rollouts of the same prompt, enabling step-level quality assessment through graph-based analysis. SALT operates as a **plug-and-play module** that integrates with existing group-based RL algorithms without modifying rollout procedures, introducing negligible computational overhead. Experiments on WebShop, ALFWorld, and AppWorld benchmarks demonstrate consistent improvements across model sizes.

![Figure 1](./images/2510.20022_figure_1.png)

**Figure 1**: SALT framework overview. For each prompt, multiple trajectories are collected and used to construct a trajectory graph. Graph analysis identifies high-quality and low-quality steps, enabling fine-grained advantage assignment instead of uniform reward distribution.

---

## Key Technical Innovations

### 1. Trajectory Graph Construction [DAG][RL][Train]

**Problem**: How to assess step quality when only sparse outcome rewards are available?

**SALT Solution**: Construct a graph from multiple trajectories of the same prompt to identify common successful patterns.

**Graph Construction Process**:
```
┌─────────────────────────────────────────────────────────────────┐
│              Trajectory Graph Construction                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input: N trajectories for same prompt                          │
│                                                                  │
│  Trajectory 1:  → A → B → C → D → SUCCESS                       │
│  Trajectory 2:  → A → B' → C → D → SUCCESS                     │
│  Trajectory 3:  → A → B → C' → E → FAILURE                     │
│  Trajectory 4:  → A → B' → C' → D → SUCCESS                    │
│  Trajectory 5:  → A → B → C → E → FAILURE                      │
│                                                                  │
│  Graph Construction:                                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │   A ───────► B ───────► C ───────► D ───────► SUCCESS  │   │
│  │   │          │            │            │               │   │
│  │   │          └──► B' ─────┴────────────┴───────────────┤   │
│  │   │                                    │               │   │
│  │   └────────────────────────────────────┴──► E ───► FAILURE│   │
│  │                                                         │   │
│  │   Node Features:                                       │   │
│  │   - Frequency: how often state appears                 │   │
│  │   - Success Rate: P(success | state)                  │   │
│  │   - Transition Patterns: incoming/outgoing edges       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Node Features**:
- **State frequency**: How often this state appears across trajectories
- **Success rate**: Proportion of trajectories reaching success from this state
- **Transition entropy**: Diversity of outgoing actions

**Edge Features**:
- **Action frequency**: How often this action is taken from this state
- **Conditional success rate**: P(success | state, action)

### 2. Step-Level Quality Assessment [DAG][Reward][Train]

**Goal**: Assign quality scores to individual steps based on graph analysis.

**Step Quality Score**:
```
Q(sᵢ, aᵢ) = α × success_rate(sᵢ) + β × success_rate(sᵢ, aᵢ) + γ × rarity(sᵢ)
```

Where:
- `success_rate(sᵢ)`: Empirical success rate from state sᵢ
- `success_rate(sᵢ, aᵢ)`: Empirical success rate of taking action aᵢ from state sᵢ
- `rarity(sᵢ)`: Inverse frequency of state sᵢ (rare states may be more informative)

**Step Advantages**:
```
A(sᵢ, aᵢ) = Q(sᵢ, aᵢ) - baseline(sᵢ)
baseline(sᵢ) = mean(Q(sᵢ, a) for all a in trajectory)
```

**Comparison to standard GRPO**:

| Approach | Advantage Assignment |
|----------|---------------------|
| **Standard GRPO** | A = r_outcome - mean(group_rewards) <br> (same for all steps) |
| **SALT** | Aᵢ = Q(sᵢ, aᵢ) - baseline(sᵢ) <br> (varies per step) |

### 3. Plug-and-Play Integration [RL][Train][Runtime]

**No rollout modification required**: SALT operates as a post-processing step on collected trajectories.

**Integration Workflow**:
```
┌─────────────────────────────────────────────────────────────────┐
│                   SALT Integration with GRPO                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Standard Rollout Collection:                                │
│     ├─ Collect N trajectories per prompt                        │
│     ├─ Execute environment interactions                         │
│     └─ Store (state, action, reward) tuples                     │
│                                                                  │
│  2. SALT Post-Processing (new):                                 │
│     ├─ Construct trajectory graph from N rollouts              │
│     ├─ Compute step-level quality scores Q(s, a)               │
│     └─ Generate step-level advantages A(s, a)                  │
│                                                                  │
│  3. GRPO Update (modified):                                     │
│     ├─ Replace uniform advantages with step-level advantages   │
│     └─ Standard GRPO policy gradient update                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Code Integration**:
```python
# Standard GRPO
def compute_advantages(trajectories):
    group_rewards = [sum(t.rewards) for t in trajectories]
    advantages = [r - mean(group_rewards) for r in group_rewards]
    return advantages  # One advantage per trajectory

# GRPO with SALT
def compute_advantages_salt(trajectories):
    graph = build_trajectory_graph(trajectories)
    advantages = []
    for traj in trajectories:
        for step in traj.steps:
            q_score = compute_quality_score(graph, step.state, step.action)
            baseline = compute_baseline(graph, step.state)
            advantages.append(q_score - baseline)  # Per-step advantage
    return advantages
```

### 4. Multi-Benchmark Evaluation [APP][Agent][RL]

**Benchmarks**:

| Benchmark | Domain | Horizon Length | Challenge |
|-----------|--------|----------------|-----------|
| **WebShop** | E-commerce | ~10 steps | Web navigation, product comparison |
| **ALFWorld** | Embodied AI | ~15 steps | Object interaction, task planning |
| **AppWorld** | App automation | ~20 steps | Multi-app coordination |

**Evaluation Protocol**:
- Train with GRPO baseline and GRPO+SALT
- Compare final success rate and sample efficiency
- Ablate key components (graph construction, quality scoring)

---

## DAG-Specific Considerations [DAG][RL][Train]

SALT leverages trajectory DAG structure for fine-grained credit assignment:

1. **Trajectory graph as DAG**: Multiple rollouts form a DAG where nodes are states and edges are actions, capturing alternative paths through the state space

2. **Node-level credit assignment**: Graph features (success rate, frequency) enable per-node quality assessment rather than trajectory-level rewards

3. **Path-based advantage computation**: Step advantages derived from graph position—nodes on high-success paths receive higher advantages

4. **Multi-path DAG comparison**: Graph structure enables comparison of alternative trajectories through the same state space, identifying which action choices lead to better outcomes

5. **DAG topology encodes task structure**: Branching factor indicates decision complexity; depth indicates horizon length; terminal nodes encode outcomes

**Future DAG integration opportunities**:
- Causal DAG analysis to identify which state transitions are causal to success vs. correlation
- Hierarchical DAGs for sub-task level credit assignment in complex multi-stage tasks
- Multi-agent DAG coordination where different agents handle different branches of the task DAG
- DAG-level curriculum learning where easier DAGs (simpler state spaces) are trained before harder ones

---

## Performance Results

### Success Rate Improvements

| Benchmark | Model | GRPO Baseline | GRPO + SALT | Improvement |
|-----------|-------|---------------|-------------|-------------|
| **WebShop** | Llama-3-8B | 28.3% | **32.7%** | +4.4% |
| **WebShop** | Llama-3-70B | 34.1% | **38.9%** | +4.8% |
| **ALFWorld** | Llama-3-8B | 52.4% | **57.8%** | +5.4% |
| **ALFWorld** | Llama-3-70B | 61.7% | **67.2%** | +5.5% |
| **AppWorld** | Llama-3-8B | 18.2% | **21.6%** | +3.4% |
| **AppWorld** | Llama-3-70B | 23.5% | **27.1%** | +3.6% |

### Sample Efficiency

**Training curves to reach target success rate**:

| Benchmark | Target | GRPO Steps | SALT Steps | Reduction |
|-----------|--------|------------|------------|-----------|
| WebShop | 30% | 12,400 | 8,200 | **34%** |
| ALFWorld | 55% | 8,600 | 5,800 | **33%** |
| AppWorld | 20% | 15,200 | 11,400 | **25%** |

### Training Stability

**Variance of success rate during training (lower is better)**:

| Benchmark | GRPO Variance | SALT Variance | Improvement |
|-----------|---------------|---------------|-------------|
| WebShop | ±4.2% | ±2.1% | **50%** |
| ALFWorld | ±3.8% | ±1.9% | **50%** |
| AppWorld | ±5.1% | ±2.8% | **45%** |

### Ablation Studies

| Configuration | WebShop | ALFWorld | AppWorld |
|---------------|---------|----------|----------|
| Full SALT | 32.7% | 57.8% | 21.6% |
| w/o success rate feature | 30.4% | 55.2% | 20.1% |
| w/o rarity feature | 31.9% | 56.9% | 21.2% |
| w/o trajectory graph | 28.3% | 52.4% | 18.2% |
| GRPO Baseline | 28.3% | 52.4% | 18.2% |

**Key finding**: All components contribute, with trajectory graph construction providing the largest gain.

### Computational Overhead

| Phase | GRPO | GRPO + SALT | Overhead |
|-------|------|-------------|----------|
| Rollout | 100% | 100% | 0% |
| Graph Construction | 0% | 5% | +5% |
| Advantage Computation | 2% | 7% | +5% |
| Training | 100% | 100% | 0% |
| **Total** | 100% | **107%** | **+7%** |

---

## External Resources

- **Paper**: [arXiv:2510.20022](https://arxiv.org/abs/2510.20022)
- **Authors**: Jiazheng Li, Yawei Wang, David Yan, Yijun Tian, Zhichao Xu, Huan Song, Panpan Xu, Lin Lee Cheong
- **Related Work**:
  - GRPO: Group Relative Policy Optimization
  - Advantage Shaping as Surrogate Reward Maximization (arXiv:2510.23049)
  - Process Reward Models for step-level supervision

---

## Key Insights

1. **Uniform rewards are insufficient for long horizons**: Multi-step trajectories contain both good and bad actions; sparse outcome rewards cannot distinguish between them

2. **Trajectory graphs enable step-level assessment**: By constructing graphs from multiple rollouts, SALT identifies which steps correlate with success

3. **Plug-and-play integration is possible**: No rollout modification required; SALT operates as a post-processing step with negligible overhead (+7%)

4. **Training stability improves significantly**: 50% reduction in success rate variance indicates more stable optimization landscape

5. **Sample efficiency gains are substantial**: 25-34% reduction in training steps to reach target performance

6. **Graph features capture task structure**: Success rate, state frequency, and transition patterns together provide rich signal for credit assignment
