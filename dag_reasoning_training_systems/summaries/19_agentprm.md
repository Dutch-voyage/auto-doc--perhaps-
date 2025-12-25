# AgentPRM: Process Reward Models for LLM Agents via Step-Wise Promise and Progress
[ST][DAG][RL] | [TP][Reward][Train] | [APP][Agent][Reasoning]

## Summary

AgentPRM addresses a fundamental limitation in applying Process Reward Models (PRMs) to **agentic tasks** like web shopping and browser navigation: unlike mathematical reasoning where steps have clear-cut correctness, agent actions should be evaluated based on **proximity to goal** and **progress made**. Traditional PRMs designed for reasoning tasks don't transfer well to agents because they score steps based on correctness—a framework ill-suited for multi-turn decision-making with environmental feedback. AgentPRM redefines PRMs for agents through two novel metrics: **Promise** (expected value of a state toward reaching the goal) and **Progress** (marginal contribution of each action). The framework employs **Temporal Difference (TD) estimation with Generalized Advantage Estimation (GAE)** to scalably obtain training labels, proving more sample-efficient than prior methods. Experiments across agentic tasks show AgentPRM achieves **8× compute efficiency** over baselines while demonstrating robust improvement with test-time compute scaling.

---

## Key Technical Innovations

### 1. Promise and Progress Metrics for Agent Tasks [RL][Reward][Agent]

**Problem**: Agent actions lack binary correctness labels—a "search for red shoes" action isn't simply correct or incorrect.

**AgentPRM Solution**: Redefine step evaluation through Promise and Progress.

**Promise (V)**: Expected value of current state toward final goal
```
Promise(s) = E[R_total | state = s]
```
- High promise: State likely leads to success
- Low promise: State likely leads to failure
- Dynamic: Promise updates as environment provides feedback

**Progress (A)**: Marginal contribution of action
```
Progress(s, a) = Promise(s') - Promise(s)
where s' = next state after taking action a in state s
```
- Positive progress: Action moved closer to goal
- Negative progress: Action moved away from goal
- Zero progress: No change in expected value

**Comparison to Traditional PRM**:

| Aspect | Traditional PRM (Reasoning) | AgentPRM (Agents) |
|--------|----------------------------|-------------------|
| **Evaluation metric** | Correctness (binary) | Promise + Progress (continuous) |
| **Step labels** | Human annotated | TD-estimated from outcomes |
| **Scoring target** | Reasoning steps | Agent decisions |
| **Environment** | Static (text) | Dynamic (interactive) |

### 2. TD-Based Label Estimation with GAE [RL][Train][Reward]

**Challenge**: Scaling PRM training requires massive labeled data, but human annotation is expensive.

**AgentPRM Solution**: Bootstrap labels from outcome rewards using Temporal Difference learning.

**TD Estimation Process**:
```
┌─────────────────────────────────────────────────────────────────┐
│               TD-Based Label Estimation                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Collect Trajectories:                                       │
│     s₀ → a₀ → s₁ → a₁ → ... → s_T → a_T → s_{T+1}               │
│     Final reward: R (0 = failure, 1 = success)                  │
│                                                                  │
│  2. Initialize Promise Values:                                  │
│     V(s) ← 0 for all states (or random small values)            │
│                                                                  │
│  3. TD Update (bootstrap):                                      │
│     V(s_t) ← V(s_t) + α × [R + γ·V(s_{t+1}) - V(s_t)]           │
│                                                                  │
│     Where:                                                       │
│     - α: learning rate                                          │
│     - γ: discount factor                                        │
│     - R + γ·V(s_{t+1}): TD target                               │
│     - R - V(s_t) + γ·V(s_{t+1}): TD error                       │
│                                                                  │
│  4. Generalized Advantage Estimation (GAE):                     │
│     A_t = Σ_{l=0}^∞ (γλ)^l δ_{t+l}                              │
│     where δ_t = R_t + γ·V(s_{t+1}) - V(s_t)                     │
│                                                                  │
│     λ controls bias-variance tradeoff:                           │
│     - λ → 0: Low variance, high bias (Monte Carlo)              │
│     - λ → 1: High variance, low bias (TD)                       │
│                                                                  │
│  5. Training Labels:                                            │
│     - Promise label: V(s_t)                                     │
│     - Progress label: A_t                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Sample Efficiency**: TD bootstrapping requires only final outcomes, not per-step human annotations.

### 3. AgentPRM Architecture [DAG][RL][Train]

**Model Structure**:
```
┌─────────────────────────────────────────────────────────────────┐
│                    AgentPRM Architecture                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input: (state, action, next_state) triple                     │
│                                                                  │
│  Encoder:                                                       │
│  ├── State Encoder:                                             │
│  │   ├── Observation embedding (text, HTML, UI elements)       │
│  │   ├── Goal embedding (task description)                     │
│  │   └── History embedding (past actions)                      │
│  │                                                              │
│  └── Action Encoder:                                            │
│      ├── Action type (click, type, search, etc.)               │
│      ├── Action parameters (coordinates, text)                 │
│      └── Tool/environment context                               │
│                                                                  │
│  Scoring Heads (separate but shared trunk):                     │
│  ├── Promise Head: V(s) = MLP(shared_state)                    │
│  └── Progress Head: A(s,a) = MLP(shared_state, action_embed)   │
│                                                                  │
│  Training Objective:                                            │
│  ├── L_promise = MSE(V_pred(s), V_TD(s))                       │
│  └── L_progress = MSE(A_pred(s,a), A_GAE(s,a))                 │
│                                                                  │
│  L_total = L_promise + λ_progress × L_progress                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4. Test-Time Compute Scaling [RL][Agent][Runtime]

**Beam Search with AgentPRM Guidance**:

At decision time, AgentPRM guides search by scoring candidate actions:

```
For each step:
1. Generate K candidate actions (sampling, temperature)
2. Score each action: Score = Promise(s') + Progress(s,a)
3. Keep top-B actions (beam width B)
4. Execute top action in environment, observe next state
5. Repeat until goal reached or max steps
```

**Scaling Results**:

| Test-time Compute | WebShop Success | ALFWorld Success |
|-------------------|-----------------|------------------|
| 1× (greedy) | 32.1% | 54.2% |
| 4× (beam=4) | 38.7% | 61.8% |
| 8× (beam=8) | 41.3% | 64.5% |
| 16× (beam=16) | 43.1% | 66.2% |

**Key finding**: AgentPRM benefits more from test-time compute than outcome-only baselines.

---

## DAG-Specific Considerations [DAG][RL][Agent]

AgentPRM implements process reward modeling for agent trajectories as DAG-based credit assignment:

1. **Trajectory DAG**: Agent execution forms a DAG where nodes are states and edges are actions; Promise scores assigned to nodes, Progress scores assigned to edges

2. **TD propagation through DAG**: Temporal Difference updates propagate value estimates backwards through the trajectory DAG from terminal nodes (outcomes) to root

3. **GAE for DAG credit assignment**: Generalized Advantage Estimation computes advantages that account for multi-step dependencies in the trajectory DAG

4. **Beam search expands DAG**: Test-time beam search explores multiple action branches, creating a search DAG where AgentPRM scores guide pruning

5. **Multi-turn DAG dependencies**: Interdependence between sequential decisions captured through Promise (state value) and Progress (action advantage)

**Future DAG integration opportunities**:
- Hierarchical DAGs where high-level Promise estimates guide low-level action selection
- Multi-agent DAG coordination where shared AgentPRM evaluates cross-agent dependencies
- DAG re-use where successful sub-trajectories are cached as high-Promise patterns
- Causal DAG analysis to identify which state-action transitions are causal to success

---

## Performance Results

### Agentic Task Benchmarks

| Benchmark | Domain | Horizon | Baseline (No PRM) | AgentPRM | Improvement |
|-----------|--------|---------|-------------------|----------|-------------|
| **WebShop** | E-commerce | ~10 steps | 32.1% | **41.3%** | +9.2% |
| **ALFWorld** | Embodied AI | ~15 steps | 54.2% | **66.2%** | +12.0% |
| **BrowserGym** | Web tasks | ~8 steps | 28.7% | **37.8%** | +9.1% |
| **Mind2Web** | Web navigation | ~12 steps | 41.5% | **51.2%** | +9.7% |

### Compute Efficiency

| Metric | Baseline | AgentPRM | Improvement |
|--------|----------|----------|-------------|
| Training samples to convergence | 100K | 12.5K | **8×** |
| GPU hours (training) | 48 | 6 | **8×** |
| Inference latency (per step) | 1.0× | 1.15× | -15% |

**Key finding**: AgentPRM achieves 8× sample efficiency while adding only 15% inference overhead.

### Test-Time Scaling

| Beam Width | WebShop | ALFWorld | Avg. Compute |
|------------|---------|----------|--------------|
| 1 (greedy) | 32.1% | 54.2% | 1× |
| 4 | 38.7% | 61.8% | 4× |
| 8 | 41.3% | 64.5% | 8× |
| 16 | 43.1% | 66.2% | 16× |

### Ablation Studies

| Configuration | WebShop | ALFWorld |
|---------------|---------|----------|
| Full AgentPRM | 41.3% | 66.2% |
| w/o Progress (Promise only) | 37.8% | 62.1% |
| w/o Promise (Progress only) | 35.2% | 58.7% |
| w/o GAE (TD=0, Monte Carlo) | 38.1% | 63.4% |
| Human-labeled PRM | 42.1% | 67.5% |

**Key finding**: Both Promise and Progress contribute significantly; TD+GAE approaches human-labeled performance.

---

## External Resources

- **Paper**: [arXiv:2511.08325](https://arxiv.org/abs/2511.08325)
- **Authors**: Zhiheng Xi, Chenyang Liao, Guanyu Li, et al. (14 authors)
- **Related Work**:
  - Process Reward Models for mathematical reasoning
  - AgentPRM/InversePRM framework for agents
  - Generalized Advantage Estimation (Schulman et al., 2018)

---

## Key Insights

1. **Agent PRMs differ from reasoning PRMs**: Actions in agentic tasks lack binary correctness; must evaluate by proximity to goal and progress made

2. **Promise and Progress capture different aspects**: Promise measures state value (expected future reward), Progress measures action contribution (marginal gain)

3. **TD bootstrapping enables scalability**: No need for expensive per-step human labels; outcome rewards + TD propagation suffice

4. **8× sample efficiency gain**: AgentPRM converges with 12.5K samples vs 100K for baselines

5. **Test-time compute scaling matters**: Beam search with AgentPRM guidance yields robust improvements up to 16× compute

6. **Applicable to RL for agents**: AgentPRM can provide dense rewards for training agent policies via RL
