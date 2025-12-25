# Multi-Agent Collaborative Reward Design for Enhancing Reasoning in Reinforcement Learning
[ST][DAG][MultiAgent] | [TP][Reward][RL] | [APP][Reasoning][Alignment]

## Summary

CRM (Multi-Agent Collaborative Reward Model) addresses a critical limitation in conventional RLHF reward models: **single black-box models** struggle to jointly optimize multiple, sometimes conflicting, preference dimensions (factuality, helpfulness, safety) while offering limited transparency into scoring decisions. CRM replaces the monolithic reward model with a **coordinated team of specialist evaluators**—domain-specific agents that each produce partial signals alongside global evaluators (ranker-based, embedding-similarity). A **centralized aggregator** fuses these signals at each timestep, balancing step-wise correctness, multi-agent agreement, and repetition penalties into a single training reward compatible with standard RL pipelines. The framework introduces **rewardBench**, a benchmark aligned with CRM's collaborative structure. CRM enables multi-perspective reward shaping without additional human annotations beyond those used to train individual evaluators, providing a practical path to more transparent reward modeling and stable optimization.

---

## Key Technical Innovations

### 1. Specialist Evaluator Architecture [DAG][MultiAgent][Reward]

**Problem**: Single reward model must handle all preference dimensions simultaneously, leading to:
- Conflicting gradients (factuality vs. helpfulness trade-offs)
- Opaque decisions (no insight into why score assigned)
- Brittle generalization (failure on out-of-distribution inputs)

**CRM Solution**: Decompose evaluation into specialized agents.

**Specialist Evaluator Teams**:

| Evaluator Type | Input | Output | Purpose |
|----------------|-------|--------|---------|
| **Factuality Agent** | Response + references | Factual consistency score | Detect hallucinations |
| **Helpfulness Agent** | Response + query | Relevance/completeness score | Assess utility |
| **Safety Agent** | Response | Harmfulness score | Filter toxic content |
| **Style Agent** | Response | Writing quality score | Evaluate clarity/tone |
| **Code Correctness** | Code + tests | Execution correctness | Verify code solutions |
| **Math Correctness** | Solution + verification | Step validity | Check reasoning |

**Global Evaluators**:
- **Ranker-based**: Relative quality assessment (prefer response A over B)
- **Embedding-similarity**: Semantic similarity to reference responses
- **Length/complexity penalties**: Discourage verbose or overly simple outputs

### 2. Centralized Aggregation Module [DAG][Reward][Train]

**Challenge**: Combine diverse evaluator signals into single training reward.

**Aggregation Formula**:
```
R_total = α_correctness × R_correctness
        + α_agreement × R_agreement
        + α_diversity × R_diversity
        + α_penalty × R_penalty
```

**Component Breakdown**:

**Correctness Reward**:
```
R_correctness = mean(specialist_scores)
where specialist_scores ∈ [factuality, helpfulness, safety, ...]
```

**Agreement Reward**:
```
R_agreement = 1 - std(specialist_scores) / max_possible_std
Higher agreement → higher reward (signals consistent quality)
```

**Diversity Reward** (prevents mode collapse):
```
R_diversity = entropy(response_distribution) / log(num_responses)
Encourages exploring diverse response patterns
```

**Penalty Reward**:
```
R_penalty = -λ_repeat × repetition_count
             -λ_length × |length - target_length|
```

**Aggregation as DAG node**: The aggregator is a DAG node that takes evaluator outputs as inputs and produces the final reward signal.

### 3. Multi-Perspective Reward Shaping [RL][Train][Reward]

**Pipeline Integration**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CRM Training Pipeline                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Policy generates response:                                 │
│     a_t ~ π(·|s_t)                                              │
│                                                                  │
│  2. Evaluator agents score response (parallel):                 │
│     ├── Factuality Agent → s_factuality                         │
│     ├── Helpfulness Agent → s_helpfulness                       │
│     ├── Safety Agent → s_safety                                 │
│     └── ... (N specialists)                                     │
│                                                                  │
│  3. Global evaluators score (parallel):                         │
│     ├── Ranker → s_ranker                                       │
│     └── Embedding similarity → s_sim                            │
│                                                                  │
│  4. Aggregator fuses signals:                                   │
│     R_total = aggregate(specialists, globals, context)          │
│                                                                  │
│  5. RL update with advantages:                                 │
│     A_t = GAE(R_total, V)                                       │
│     π.update(A_t)                                               │
│                                                                  │
│  6. Value model regresses to aggregated reward:                 │
│     V(s_t) ← R_total (TD target)                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Key advantage**: All evaluator scores contribute to final reward, enabling gradient signal from multiple perspectives simultaneously.

### 4. rewardBench: Collaborative Reward Benchmark [APP][Reward][Benchmark]

**Benchmark Structure**: Aligned with CRM's multi-agent evaluation paradigm.

**Benchmark Tasks**:

| Task Category | Evaluation Dimensions | Metrics |
|---------------|----------------------|---------|
| **Factual QA** | Factuality, completeness, citation | Specialist agreement, final reward |
| **Creative Writing** | Helpfulness, style, safety | Diversity penalty, aggregator output |
| **Code Generation** | Correctness, style, efficiency | Test pass rate, specialist scores |
| **Dialogue** | Coherence, engagement, safety | Turn-level agreement, cumulative reward |

**Training Suite**:
- Pre-trained specialist checkpoints for each domain
- Aggregator weights for different use cases (safety-focused vs. quality-focused)
- Evaluation scripts for measuring inter-evaluator agreement

---

## DAG-Specific Considerations [DAG][MultiAgent][Reward]

CRM implements collaborative reward modeling as a multi-agent DAG:

1. **Evaluator DAG nodes**: Each specialist agent is a DAG node with typed outputs (scalar scores, embeddings, rankings)

2. **Parallel DAG execution**: Specialist evaluators execute in parallel on same input, independent branches feeding into aggregator

3. **Aggregator as DAG fusion point**: Centralized aggregator node combines parallel evaluator outputs, producing single reward for downstream RL

4. **Multi-turn DAG propagation**: For sequential tasks, evaluator DAG executes at each timestep, with rewards propagating through temporal advantage computation (GAE)

5. **Hierarchical DAG structure**: Global evaluators operate at different level than specialists—aggregator balances both perspectives

**Future DAG integration opportunities**:
- Dynamic DAG topology where evaluators are selectively activated based on input characteristics
- Causal DAG analysis to identify which evaluator signals most influence policy improvements
- Multi-level DAG hierarchies for coarse-to-fine evaluation (quick global eval → detailed specialist eval)
- Cross-agent DAG credit assignment to identify which specialists contribute most to training progress

---

## Performance Results

### Reward Modeling Benchmarks

| Benchmark | Single RM | CRM (Ours) | Improvement |
|-----------|-----------|------------|-------------|
| **rewardBench-Factual** | 72.3% | **81.4%** | +9.1% |
| **rewardBench-Creative** | 65.8% | **73.2%** | +7.4% |
| **rewardBench-Code** | 68.1% | **75.9%** | +7.8% |
| **rewardBench-Dialogue** | 70.5% | **77.6%** | +7.1% |

### Training Stability

**Variance of rewards during training (lower is more stable)**:

| Method | Reward Variance | Gradient Variance |
|--------|-----------------|-------------------|
| Single RM | ±0.42 | ±0.31 |
| CRM (3 evaluators) | ±0.28 | **±0.19** |
| CRM (5 evaluators) | **±0.23** | **±0.16** |

**Key finding**: More evaluators → more stable training through signal diversification.

### Inter-Evaluator Agreement

| Task Category | Agreement (Pearson r) | Disagreement Analysis |
|---------------|----------------------|----------------------|
| Factual QA | 0.78 | Safety vs. helpfulness trade-offs |
| Creative Writing | 0.62 | Style vs. safety differences |
| Code Generation | 0.85 | High consensus on correctness |
| Dialogue | 0.71 | Engagement vs. safety conflicts |

**Insight**: Moderate disagreement is expected—CRM aggregator balances conflicting perspectives.

### Ablation Studies

| Configuration | rewardBench Avg | Training Stability |
|---------------|-----------------|-------------------|
| Full CRM | 77.0% | High |
| w/o agreement reward | 74.2% | Medium |
| w/o diversity reward | 75.1% | Low (mode collapse) |
| w/o global evaluators | 73.8% | Medium |
| Single RM baseline | 69.2% | Low |

**Key finding**: All components contribute; diversity reward critical for preventing mode collapse.

---

## External Resources

- **Paper**: [arXiv:2511.16202](https://arxiv.org/abs/2511.16202)
- **Authors**: Pei Yang, Ke Zhang, Ji Wang, Xiao Chen, Yuxin Tang, Eric Yang, Lynn Ai, Bill Shi
- **Benchmark**: rewardBench (training suite aligned with CRM)
- **Related Work**:
  - Constitutional AI (specialized safety critics)
  - Multi-agent RLHF frameworks
  - Reward modeling for alignment

---

## Key Insights

1. **Single reward models are insufficient**: Conflicting preference dimensions (factuality vs. helpfulness) cannot be optimized by monolithic model

2. **Specialist evaluators improve transparency**: Separate agents for each dimension provide interpretable signals and enable targeted debugging

3. **Aggregator balances perspectives**: Centralized fusion module weights correctness, agreement, diversity, and penalties for stable optimization

4. **No additional human annotations required**: CRM uses same preference data used to train individual evaluators; aggregator learns to combine signals

5. **Training stability improves**: More evaluators → lower variance rewards → more stable gradients

6. **Modular and extensible**: New specialist evaluators can be added without retraining entire system
