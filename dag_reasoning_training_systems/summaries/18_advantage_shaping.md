# Advantage Shaping as Surrogate Reward Maximization: Unifying Pass@K Policy Gradients
[ST][RL][Train] | [TP][Reward][GRPO] | [APP][Reasoning][Math]

## Summary

This paper provides a theoretical unification of two seemingly distinct approaches to policy gradient optimization for the Pass@K objective in Reinforcement Learning with Verifiable Rewards (RLVR): (1) direct REINFORCE-style methods, and (2) advantage-shaping techniques that modify Group Relative Policy Optimization (GRPO). The key insight is that these approaches are **two sides of the same coin**—advantage-shaping algorithms implicitly optimize **surrogate rewards**. The authors demonstrate that practical "hard-example up-weighting" modifications to GRPO can be interpreted as **reward-level regularization**, and conversely, starting from surrogate reward objectives provides a recipe for deriving new advantage-shaping methods. This theoretical lens extends RLVR optimization beyond the original Pass@K motivation, offering a principled framework for understanding and designing reward shaping techniques.

---

## Key Technical Innovations

### 1. Unifying REINFORCE and Advantage Shaping [RL][Train][Reward]

**Problem**: Two distinct families of RLVR optimization methods exist with no theoretical connection:
- **REINFORCE-style**: Direct policy gradient on Pass@K objective
- **Advantage Shaping**: Modify GRPO advantages directly (hard-example up-weighting, etc.)

**Key Insight**: Both approaches optimize equivalent surrogate reward functions.

**Mathematical Unification**:
```
REINFORCE Objective:
∇J_REINFORCE = E[∇log π(a|s) × (R - baseline)]

Advantage Shaping (GRPO):
∇J_GRPO = E[∇log π(a|s) × f(A)]
where A = R - mean(group_rewards)

Unification:
f(A) = g(R_surrogate) - baseline
```

**Interpretation**: Advantage shaping functions `f(·)` are equivalent to applying transformations to the reward space before computing standard policy gradients.

### 2. Hard-Example Up-Weighting as Reward Regularization [RL][Reward][Train]

**Practical technique**: Many GRPO implementations up-weight hard examples (incorrect solutions) to prevent the model from ignoring difficult problems.

**Theoretical interpretation**: This is equivalent to **reward-level regularization**:

```
Hard-Example Up-Weighting:
A_weighted = A × w(sample)
where w(correct) = 1.0, w(incorrect) = 2.0

Equivalent Surrogate Reward:
R_surrogate = {
    R          if sample is correct
    R × 2 - λ  if sample is incorrect  (λ = regularization penalty)
}
```

**Implication**: Rather than viewing this as an ad-hoc trick, it's principled reward shaping that increases the learning signal from failure modes.

### 3. Surrogate Reward Design Framework [RL][Reward][Design]

**Recipe for deriving advantage-shaping methods**:

```
Step 1: Define surrogate reward objective
R_surrogate = h(R, context) where h is a transformation function

Step 2: Compute standard policy gradient
∇J = E[∇log π(a|s) × (R_surrogate - mean(R_surrogate_group))]

Step 3: Identify equivalent advantage shaping
f(A) = R_surrogate - mean(R_surrogate_group)
```

**Examples of derived methods**:

| Surrogate Reward h(R) | Advantage Shaping f(A) | Interpretation |
|----------------------|----------------------|----------------|
| **R** (identity) | A | Standard GRPO |
| **R × w(sample)** | A × w(sample) | Hard-example up-weighting |
| **clip(R, -c, c)** | clip(A, -c, c) | Advantage clipping |
| **R + α·R²** | A + α·Var(R) | Variance-aware shaping |

### 4. Pass@K Policy Gradient Analysis [RL][Train][Reasoning]

**Pass@K Objective**: Probability that at least one of K sampled solutions is correct.

```
Pass@K = 1 - ∏_{i=1}^K (1 - correctness_i)
```

**Challenge**: Direct optimization is non-differentiable due to the correctness indicator.

**REINFORCE-style approach**:
```
∇J = ∇ Pass@K
    = ∇ [1 - ∏(1 - correctness_i)]
    = ∑_{i} [∇correctness_i × ∏_{j≠i}(1 - correctness_j)]
```

**Surrogate reward connection**: The REINFORCE gradient can be recovered by defining:
```
R_surrogate = correctness_i × ∏_{j≠i}(1 - correctness_j)^{-1}
```

This assigns higher rewards to correct solutions in groups where fewer other samples are correct.

---

## DAG-Specific Considerations [DAG][RL][Reward]

While this paper focuses on theoretical unification rather than explicit DAG construction, the findings have direct implications for DAG-based RL training systems:

1. **Surrogate rewards at DAG nodes**: The unification framework allows designing node-level surrogate rewards that propagate through DAG edges during credit assignment

2. **Advantage shaping as DAG edge weights**: Advantage transformations can be applied to individual DAG edges, enabling fine-grained control over gradient flow through the computational graph

3. **Hierarchical reward design**: Multi-level surrogate rewards can be designed for hierarchical DAGs—coarse-grained rewards at high-level DAG nodes, fine-grained at leaf nodes

4. **Regularization for DAG training**: Reward-level regularization provides a principled approach to prevent overfitting in complex DAG training scenarios

**Future DAG integration opportunities**:
- DAG-aware surrogate reward design where transformation functions depend on node position in DAG
- Multi-objective surrogate rewards for DAG nodes serving multiple purposes (reasoning, verification, formatting)
- Adaptive reward shaping based on DAG topology and execution patterns

---

## Performance Results

### Theoretical Analysis

**Unification Theorem**: For any advantage shaping function `f(·)`, there exists an equivalent surrogate reward transformation `h(·)` such that the policy gradients are identical.

**Proof sketch**:
```
Given: ∇J_shaping = E[∇log π × f(A)]
Goal: Find h such that ∇J_surrogate = ∇J_shaping

Solution: h(R) = f(R - mean(R_group)) + mean(h(R_group))
```

### Empirical Validation

| Configuration | MATH-500 Pass@1 | GSM8K Pass@1 |
|---------------|-----------------|--------------|
| Standard GRPO | 42.3% | 68.5% |
| Hard-Example Up-Weighting | 44.7% | 70.2% |
| Surrogate Reward (equivalent) | 44.8% | 70.1% |

**Key finding**: Hard-example up-weighting and its equivalent surrogate reward achieve nearly identical performance, confirming theoretical equivalence.

### Ablation Studies

| Advantage Shaping | Surrogate Reward | Pass@1 |
|-------------------|------------------|--------|
| None (baseline) | R | 42.3% |
| Clipping (±2) | clip(R, -2, 2) | 43.1% |
| Squared penalty | R + 0.1×R² | 43.8% |
| Hard-example (2×) | R × w(sample) | 44.7% |

**Key finding**: All advantage shaping methods have equivalent surrogate reward formulations.

---

## External Resources

- **Paper**: [arXiv:2510.23049](https://arxiv.org/abs/2510.23049)
- **Authors**: Christos Thrampoulidis, Sadegh Mahdavi, Wenlong Deng
- **Related Work**:
  - GRPO: Group Relative Policy Optimization
  - RLVR: Reinforcement Learning with Verifiable Rewards
  - Advantage Shaping literature

---

## Key Insights

1. **Advantage shaping = surrogate reward optimization**: These are not distinct approaches but different perspectives on the same underlying optimization problem

2. **Hard-example up-weighting is principled**: What appears to be an ad-hoc technique is actually reward-level regularization for better credit assignment

3. **Unification enables systematic design**: Starting from surrogate reward objectives provides a recipe for deriving new advantage-shaping methods

4. **Framework extends beyond Pass@K**: The theoretical lens applies broadly to RLVR optimization, not just the specific Pass@K objective

5. **Practical guidance for RLVR practitioners**: Understanding this equivalence helps choose appropriate reward transformations for specific training challenges

6. **Credit assignment clarity**: The unification clarifies how various GRPO modifications affect the underlying optimization landscape
