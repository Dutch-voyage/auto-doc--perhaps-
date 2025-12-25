# Verlog: An Efficient Synchronized Multi-turn RL Framework for LLM Agents

[ST][DAG][Async][Runtime][Batch] | [TP][RL][Rollout][Train][Sync][Reward] | [APP][Agent][Reasoning][MultiAgent]

## Summary

Verlog is a synchronized multi-turn reinforcement learning framework designed for training LLM agents on long-horizon, sparse-reward tasks where achieving goals requires extended planning and precise action sequences. The framework addresses two fundamental challenges: **algorithmic instability** from sparse feedback and **system inefficiency** from variance in rollout lengths. Verlog introduces **early truncation** and **per-turn asynchronous rollouts** to reduce rollout variance, combined with **dual-discounted GAE** and **pretrained value functions** for training stabilization. The paper provides the first systematic analysis of the "**off-policy tax**" in asynchronous training frameworks. Verlog achieves **3.0x throughput improvement** over synchronous baselines while remaining stable on trajectories exceeding **400 turns** where prior frameworks typically destabilize beyond **10 turns**.

## Key Technical Innovations [DAG][Async][RL][Runtime]

### 1. Multi-Turn RL as DAG Execution [DAG][Runtime][Agent]

**Core insight**: Multi-turn RL workflows can be modeled as Directed Acyclic Graphs where:
- **Nodes**: Individual turns (state-action pairs)
- **Edges**: Temporal dependencies between turns
- **Leaf nodes**: Final rewards that propagate back through the graph

![Per-Step Input Structure](https://via.placeholder.com/800x300.png?text=Per-Step+Input+Structure+DAG)

**Figure 1**: Per-step input structure showing how multi-turn trajectories are decomposed into per-step training samples. Each trajectory produces T per-step samples where only the final action at is trainable. The value function of the first token in subsequent states provides intermediate supervision (bootstrapping), creating a DAG-like dependency structure across turns.

**DAG topology for multi-turn RL**:
```
Turn 1: s₀ → a₁ → V(s₁) ─┐
Turn 2: s₁ → a₂ → V(s₂) ─┤│
Turn 3: s₂ → a₃ → V(s₃) ─┤│
Turn T: s_{T-1} → a_T → r_T ─┘│
                              └─> Backward pass (GAE)
```

**Per-step input structure**:
- Training: Decompose trajectory `{o₀, o₁, a₁, ..., o_T, a_T}` into per-step samples
- Each sample: `{o₀, o_{t-h}, a_{t-h}, ..., o_t, a_t}` (h=1 in practice)
- Inference: Only most recent h turns provided to agent
- Ensures consistency between training and inference

### 2. Quantifying the Off-Policy Tax in Asynchronous RL [Async][RL][Sync]

**Core breakthrough**: First systematic analysis quantifying the performance cost of asynchronous training

**The fundamental trade-off**:

| Aspect | Synchronous Training | Asynchronous Training |
|--------|----------------------|-------------------------|
| **GPU Utilization** | Low (idle waiting) | High (continuous work) |
| **Data Freshness** | On-policy (πₒₗ𝒹 = π) | Off-policy (πₒₗ𝒹 ≠ π) |
| **Stability** | High | Lower (staleness) |
| **Throughput** | Baseline | 3-4x higher |

**Figure 2: Off-Policy Tax Quantification**

![Off-Policy Tax](https://via.placeholder.com/800x400.png?text=Off-Policy+Tax+Analysis)

**Figure 2**: Quantifying the off-policy tax. The vertical dotted line marks the off-policyness induced by asynchronous training. Scattered points show performance versus off-policyness for models trained with different PPO epochs. The "off-policy tax" is the reward gap between synchronous PPO-1 and the performance level achievable with the same off-policyness as asynchronous training.

**Key findings**:

| Scenario | Async Off-Policyness | PPO Equivalents | Off-Policy Tax |
|----------|----------------------|-----------------|-----------------|
| pickup_seq_goto | ~0.0025 KL | 2-4 epochs | ~15% reward gap |
| open | >0.0050 KL | 3+ epochs | **19.47%** reward gap |

**Critical insight**: PPO has limited tolerance to stale data in LLM-based RL:
- Classic RL domains: 5-10 PPO epochs tolerated
- LLM-based RL: Only 1-2 PPO epochs tolerated
- LLM agents more sensitive to distribution shift

**Off-policy data as limited resource**:
```
Total off-policy budget = fixed threshold

Can allocate to:
├── Sample efficiency: Additional PPO epochs for data reuse
└── System efficiency: Asynchronous rollouts for GPU utilization

Asynchronous PPO "spends" this budget on system efficiency,
    losing potential gains from higher sample efficiency
```

### 3. Rollout Variance Reduction [Async][Batch][DAG]

#### 3.1 Sources of GPU Underutilization [DAG][Batch]

**Table 1: GPU Idle Time in Synchronized Multi-Turn RL**

| Environment | Idle Turn Ratio | Idle Token Ratio | Combined Waste |
|-------------|-----------------|------------------|----------------|
| BabyAI | 0.357 ± 0.187 | 0.475 ± 0.081 | **~67%** |
| BabaIsAI | 0.296 ± 0.201 | 0.522 ± 0.082 | **~66%** |
| Crafter | 0.386 ± 0.080 | 0.489 ± 0.088 | **~68%** |
| **Overall** | **0.333** | **0.498** | **~67%** |

**Two sources of variance in DAG execution**:

1. **Response length variance** (within DAG nodes):
   - Different token generation lengths within a turn
   - Idle Token Ratio = `Σ(L_max - len(r_i)) / (n × L_max)`

2. **Trajectory length variance** (DAG depth):
   - Different numbers of turns per episode
   - Idle Turn Ratio = `Σ(T_max - len(traj_j)) / (m × T_max)`

![Variance Sources](https://via.placeholder.com/800x350.png?text=DAG+Variance+Analysis)

**Figure 3**: Sources of variance in synchronized multi-turn RL DAG execution. Response length variance causes idle time within individual turn nodes, while trajectory length variance causes idle time waiting for longer DAG paths to complete.

#### 3.2 Early Truncation: Fixed DAG Depth [Runtime][DAG]

**Core innovation**: Fixed horizon `L_episode` truncates rollouts at predetermined step count

**Implementation**:
```python
# Early truncation algorithm
for step in range(L_episode):  # Fixed DAG depth
    for env_id in range(n_env):  # Parallel DAG branches
        state = envs[env_id].reset_if_done()
        action = agent.generate(state)
        next_state, reward, done = envs[env_id].step(action)
        buffer.store(state, action, reward)

# Each batch = L_episode × n_env samples
# Auto-reset ensures continuous DAG execution
```

**Figure 4: Early Truncation DAG Structure**

![Early Truncation](https://via.placeholder.com/800x300.png?text=Early+Truncation+DAG)

**Figure 4**: Early truncation creates fixed-depth DAG subgraphs. Each trajectory is truncated at L_episode steps, with environments auto-resetting to create new DAG branches. This eliminates trajectory length variance while preserving causal dependencies within each branch.

**Benefits**:
- Predictable batch sizes (critical for deep learning frameworks)
- Eliminates trajectory depth variance
- Enables pipeline overlapping between rollouts

**Requirements for stability**:
- Must incorporate value function (no GRPO variants)
- Value function must be accurate → requires pretraining

#### 3.3 Per-Turn Asynchronous Rollouts [Async][DAG][Batch]

**Core innovation**: Relax lockstep requirement at turn level, treating each turn as minimal DAG scheduling unit

**Synchronous vs Asynchronous (per-turn)**:

```
Synchronous (lockstep):
Turn 1: [Env1][Env2][Env3][Env4] ─┬─> Wait for longest
Turn 2: [Env1][Env2][Env3][Env4] ─┤     (GPU idle)
Turn 3: [Env1][Env2][Env3][Env4] ─┘

Asynchronous (per-turn):
Env1: Turn1→Turn2→Turn3→Turn4 (continuous)
Env2: Turn1──→Turn2──→Turn3───> Ready
Env3: Turn1────→Turn2───────> Processing
Env4: Turn1────────→Turn2────> Processing

Global counter: ████████ (batch complete)
```

**Table 2: Rollout Efficiency Comparison (tokens/second)**

| Task | Early Truncation | +Async Rollouts | Fully Async | Efficiency Gain |
|------|-------------------|-----------------|--------------|------------------|
| BabyAI Avg | 324.7 | **1021.0** | 1203.6 | **3.14x** |
| BabaIsAI Avg | 353.9 | **925.5** | 1241.0 | **2.61x** |
| **Overall** | **339.3** | **973.2** | 1222.3 | **2.87x** |

**Key result**: Per-turn async rollouts achieve **~80% of fully async throughput** while avoiding off-policy tax

**Figure 5: Asynchronous Rollout DAG Scheduling**

![Async Rollout DAG](https://via.placeholder.com/800x350.png?text=Async+Rollout+Scheduling)

**Figure 5**: Per-turn asynchronous rollout DAG scheduling. Each environment (DAG branch) progresses independently through turns, contributing to a shared global counter. This minimizes idle time while maintaining on-policy training integrity.

### 4. Dual-Discounted GAE [DAG][Reward][RL]

#### 4.1 The Efficiency-Depth Tension [DAG][Reward]

**Challenge**: Multi-turn RL DAG faces tension between:
- **Shorter trajectories** → more efficient execution
- **Longer responses** → necessary reasoning depth

**Discount factor trade-off**:
```
γ = 1: Preserves reasoning depth (no response shrinkage)
      ↓
      Encourages long, meandering dialogues
      ↓
      Reduced computational efficiency

γ < 1: Encourages shorter dialogues
      ↓
      May truncate reasoning prematurely
      ↓
      Reduced task performance
```

#### 4.2 Dual-Discounted GAE Design [DAG][RL]

**Core innovation**: Decouple token-level and turn-level discounting to preserve reasoning while encouraging efficiency

**Parameters**:
- Token level: `(γ_token, λ_token) = (1, 1)` → preserve reasoning length
- Turn level: `(γ_step, λ_step) = (0.99, 0.95)` → promote efficiency

**GAE recursion**:
```
Â_t = γλ · Â_{t+1} + δ^V_t

where γλ = {
    γ_step · λ_step,  if tokens t and t+1 belong to different turns
    γ_token · λ_token, otherwise
}

δ^V_t = -V(s_t) + r_t + γV(s_{t+1})
```

**Figure 6: Dual-Discounted GAE Structure**

![Dual-Discount GAE](https://via.placeholder.com/800x400.png?text=Dual-Discount+GAE+Structure)

**Figure 6**: Dual-discounted GAE with per-step input structure. Separate γ and λ values at token (γ_token=1, λ_token=1) and step (γ_step=0.99, λ_step=0.95) levels enable preserving reasoning depth within turns while encouraging task completion in fewer dialogue turns. The value function of the first token in each subsequent state provides intermediate supervision, creating a DAG bootstrapping structure.

**Bootstrapping mechanism**:
```
Turn t:   s_t → a_t → V(s_{t+1}) ─┐
                              │
Turn t+1: s_{t+1} → a_{t+1} → V(s_{t+2}) ─┤│
                                 ││
Turn t+2: s_{t+2} → a_{t+2} → V(s_{t+3}) ─┘││
                                    └─> r_T (final reward)

Value(s_{t+1}) bootstraps Turn t even before observing r_T
```

**Algorithm 1: Dual-Discounted GAE Computation**

```python
def compute_dual_discount_gae(trajectory, gamma_token=1.0, lambda_token=1.0,
                                 gamma_step=0.99, lambda_step=0.95):
    advantages = []
    gae = 0.0

    # Process backward from final token
    for t in reversed(range(len(trajectory))):
        if trajectory[t].is_first_token_of_turn:
            # Use step-level discount between turns
            gamma_lambda = gamma_step * lambda_step
        else:
            # Use token-level discount within turns
            gamma_lambda = gamma_token * lambda_token

        delta = -trajectory[t].value + trajectory[t].reward + \
                 (gamma_step if trajectory[t].is_last_token else gamma_token) * \
                 trajectory[t+1].value if t+1 < len(trajectory) else 0

        gae = delta + gamma_lambda * gae
        advantages.insert(0, gae)

    return advantages
```

**Figure 7: Effect of Dual-Discounted GAE**

![Dual-Discount GAE Effect](https://via.placeholder.com/800x350.png?text=Dual-Discount+GAE+Effect)

**Figure 7**: Effect of dual-discounted GAE on BabyAI pickup tasks. Dual-discount GAE (blue) accelerates win-rate convergence and encourages shorter trajectories compared to standard single-discount variant (orange). The step-level discount (γ_step=0.99) encourages agents to solve tasks with fewer turns while preserving reasoning depth within each turn.

### 5. Value Function Pretraining [RL][Train][DAG]

**Requirement**: Early truncation requires accurate value function for bootstrapping

**Pretraining procedure**:
1. Train value function on collected trajectories
2. Continue until value loss stabilizes
3. Verify no large fluctuations at RL onset
4. Use pretrained value function for RL bootstrapping

**Benefits**:
- Stable bootstrapping over truncated horizons
- Reduced variance in advantage estimation
- Faster convergence in RL training

## Performance Results [DAG][RL][Agent]

### End-to-End Performance on Long-Horizon Tasks

**Table 3: Experimental Setup**

| Benchmark | Model | Training | Hardware | Duration | Max Turns |
|-----------|-------|----------|----------|----------|-----------|
| BabyAI | Qwen2.5-3B | 300 PPO updates | 4×A40 (48GB) | ~24 hours | ~128 |
| BabaIsAI | Qwen2.5-3B | 300 PPO updates | 4×A40 (48GB) | ~24 hours | ~100 |
| Crafter | Qwen2.5-7B | 170 PPO updates | 8×H100 (82GB) | ~36 hours | **400+** |

**Figure 8: BabyAI and BabaIsAI Results**

![BabyAI BabaIsAI Results](https://via.placeholder.com/900x500.png?text=BabyAI+and+BabaIsAI+Results)

**Figure 8**: BabyAI and BabaIsAI results comparing Qwen2.5-7B fine-tuned with PPO (Verlog) vs zero-shot GPT-4o-mini baseline across 8 scenarios. Fine-tuning significantly improves task scores, demonstrating that Verlog enables RL policies to learn from long-horizon DAG-structured interactions with the environment.

**Scenarios evaluated**:
- goto, pickup, pickup_seq_goto, open, distr_obj, 2room, 2room_rule, maybe_break_stop

**Figure 9: Crafter Results**

![Crafter Results](https://via.placeholder.com/800x400.png?text=Crafter+Results)

**Figure 9**: Crafter results comparing Qwen2.5-7B fine-tuned with PPO vs zero-shot GPT-4o-mini. Fine-tuning achieves higher average score (~8 vs ~6) with shorter average trajectory length (~185 vs ~205), suggesting possible reward hacking where agents learn to exploit reward function rather than fully understanding the game.

### Throughput Efficiency

**Table 4: Performance vs Efficiency Trade-offs**

| Method | Throughput (tok/s) | Off-Policy Tax | Max Stable Turns |
|--------|-------------------|-----------------|-------------------|
| Synchronous (baseline) | 339.3 | 0% | 10 (typical) |
| +Early Truncation | 339.3 | 0% | ~50 |
| +Async Rollouts | **973.2** | 0% | **400+** |
| Fully Async | 1222.3 | 15-20% | Variable |

**Key result**: Per-turn async rollouts achieve **2.87x throughput** while maintaining stability

### Limitation: RL Can't Learn Skills Beyond Base Model

**Figure 10: Skill-Specific Achievement Breakdown**

![Skill Breakdown](https://via.placeholder.com/800x350.png?text=Skill-Specific+Achievements)

**Figure 10**: Breakdown of skill-specific achievements before and after fine-tuning. Improvements are concentrated in tasks that the base model already demonstrated partial competence in (make wood sword), while skills absent in the base model (make iron sword) remain largely unlearned. This indicates current RL primarily reinforces existing latent skills rather than enabling acquisition of genuinely new long-horizon capabilities.

**Critical observation**: Fine-tuning sharpens action distribution toward higher-reward behaviors rather than enabling new capabilities

### Limitation: Diversity Reduction in Reasoning

**Figure 11: Diversity vs Normalized Reward**

![Diversity Analysis](https://via.placeholder.com/800x350.png?text=Diversity+vs+Reward)

**Figure 11**: Diversity score versus normalized reward in BabyAI goto tasks. As rewards increase, the diversity of reasoning pattern (measured by normalized Levenshtein edit distance between POS-tag sequences) decreases. This reduction coincides with the sharp increase in win rate, indicating transition from broad exploration to problem-specific exploitation.

**Diversity score formula**:
```
Diversity = d_edit(POS_gen, POS_ref) / max(|POS_gen|, |POS_ref|)

where:
- POS_gen: POS-tag sequence of generated reasoning
- POS_ref: POS-tag sequence of reference reasoning
- d_edit: Levenshtein edit distance
```

## DAG-Specific Considerations [DAG][Async][RL]

Verlog models multi-turn RL trajectories as DAGs where each turn is a node and causal dependencies form edges:

1. **Multi-turn trajectory DAG**: Nodes are state-action pairs, edges represent causal dependencies, with bootstrapping path through value function enabling credit assignment across truncated horizons
2. **Per-turn asynchrony**: Process each turn immediately when ready without waiting for other environments, enabling fine-grained load balancing and GPU utilization
3. **Independent branch parallelization**: Multiple environments execute concurrently as independent DAG branches with variable lengths, coordinated via shared global counter
4. **Bootstrapping for sparse rewards**: Value function V(s_{t+1}) provides intermediate supervision for turn t even before final reward r_T observed, creating backward dependency chain through DAG

**Future DAG integration opportunities**:
- Extend to general DAG topologies beyond linear trajectories (branching tool calls, conditional reasoning paths)
- Support inter-tool dependencies and compound actions in environment action space
- Dynamic DAG construction based on task complexity and environmental feedback
- Multi-agent DAG coordination where agents represent specialized sub-agents

## System Architecture [ST][DAG][Runtime]

### Verlog Implementation Variants

**Table 5: Verlog Implementation Variants**

| Version | Training | Early Truncation | Async Rollouts | Off-Policy Tax |
|---------|----------|------------------|-----------------|-----------------|
| V1 | Synchronized | ✓ | – | 0% |
| V2 | Synchronized | ✓ | ✓ | 0% |
| V3 | Asynchronous | ✓ | – | 15-20% |

**Recommended**: V2 (Synchronous + Early Truncation + Async Rollouts)
- Achieves 2.87x throughput improvement
- Zero off-policy tax
- Stable on 400+ turn trajectories

### Comparison to Related Work

| Framework | Max Turns | Async Rollouts | Off-Policy Tax | DAG-Based |
|-----------|-----------|-----------------|-----------------|-----------|
| RAGEN | 5-10 | No | 0% | Implicit |
| Search-R1 | 5-10 | No | 0% | Implicit |
| verl-agent | Limited | No | 0% | Per-step only |
| VeRL | Variable | Yes | Present | Implicit |
| Slime | Variable | Yes | Present | Implicit |
| AReaL | Variable | Yes | Present | Implicit |
| **Verlog** | **400+** | **Per-turn** | **0%** | **Explicit** |

**Verlog advantages**:
- First to demonstrate stability on 400+ turn trajectories
- Avoids off-policy tax through synchronous training
- Per-turn async achieves ~80% of async throughput benefit
- Explicit DAG modeling with per-step decomposition

## Key Insights [DAG][Async][RL]

1. **Off-policy tax quantified**: 15-20% performance gap when using asynchronous training in LLM-based RL

2. **Two-thirds GPU waste**: Synchronized rollouts waste ~67% GPU time due to variance in DAG execution

3. **Per-turn async is sweet spot**: Achieves 2.87x throughput with zero off-policy tax

4. **400+ turn stability**: Dual-discount GAE + pretrained value function enables unprecedented stability

5. **RL reinforces existing skills**: Cannot teach genuinely new long-horizon capabilities beyond base model

6. **Diversity decreases with training**: Transition from exploration to exploitation narrows reasoning patterns

## External Resources

- [Paper on OpenReview](https://openreview.net/forum?id=U3yTQonq10)
- [PDF](https://openreview.net/pdf?id=U3yTQonq10)
- Related: [VeRL](https://github.com/volcengine/verl), [BALROG](https://arxiv.org/abs/2411.13543), [Search-R1](https://arxiv.org/abs/2503.09516)

## Tags Breakdown

**System Topics [ST]**:
- `[DAG]` - Multi-turn trajectories modeled as DAG with turn-level nodes
- `[Async]` - Per-turn asynchronous rollouts for efficiency
- `[Runtime]` - Synchronized training with early truncation
- `[Batch]` - Fixed batch sizes through L_episode × n_env samples

**Training Phases [TP]**:
- `[RL]` - PPO-based reinforcement learning
- `[Rollout]` - Multi-turn rollouts with variance reduction
- `[Train]` - On-policy PPO with dual-discounted GAE
- `[Sync]` - Synchronous training avoids off-policy tax
- `[Reward]` - Sparse reward handling through bootstrapping

**Application [APP]**:
- `[Agent]` - LLM agent training for autonomous decision-making
- `[Reasoning]` - Long-horizon reasoning tasks requiring planning
- `[MultiAgent]` - Multi-environment parallel training
