# DAG-Math: Graph-Guided Mathematical Reasoning in LLMs
[ST][DAG][Reasoning] | [TP][Train][Reward] | [APP][Math]

## Summary

DAG-MATH introduces a novel framework for evaluating mathematical reasoning in LLMs by modeling Chain-of-Thought (CoT) as a **rule-based stochastic process over directed acyclic graphs (DAGs)**. Unlike existing approaches that rely solely on PASS@k metrics (final answer accuracy), DAG-MATH introduces **logical closeness**—a metric quantifying how well a model's reasoning trajectory adheres to the DAG structure of valid derivations. The framework addresses a fundamental question: do LLMs succeed at math through genuine rule-consistent reasoning, or through pattern matching and rote procedures? The authors introduce the DAG-MATH CoT format and a benchmark that guides LLMs to generate graph-structured reasoning, enabling evaluation of reasoning fidelity beyond final correctness. Analysis reveals significant differences in reasoning quality across LLM families even when PASS@k scores are comparable, highlighting gaps between answer accuracy and derivation quality.

---

## Key Technical Innovations

### 1. DAG-Based Reasoning Model [DAG][Reasoning][Math]

**Concept**: Model mathematical CoT as a stochastic process over DAGs where nodes represent intermediate derivation states and edges encode rule applications.

**DAG Structure for Mathematical Reasoning**:
```
                    ┌─────────────────────────────────────────┐
                    │         Mathematical Problem             │
                    │         "Solve: 2x + 5 = 13"              │
                    └─────────────────┬───────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │         Initial State Node               │
                    │         S0: {2x + 5 = 13}                │
                    └─────────────────┬───────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┬───────┐
                    │                 │                 │       │
                    ▼                 ▼                 ▼       ▼
              ┌─────────┐       ┌─────────┐       ┌─────────┐ ┌───────┐
              │ S1      │       │ S1'     │       │ S1''    │ │ ...   │
              │Subtract │       │ Divide  │       │Expand   │ │       │
              │  5      │       │         │       │         │ │       │
              └────┬────┘       └────┬────┘       └────┬────┘ └───────┘
                   │                 │                 │
                   ▼                 ▼                 ▼
              ┌─────────┐       ┌─────────┐       ┌─────────┐
              │ S2      │       │ S2'     │       │ S2''    │
              │2x = 8   │       │         │       │         │
              └────┬────┘       └─────────┘       └─────────┘
                   │
                   ▼
              ┌─────────┐
              │ S3      │
              │x = 4    │
              └─────────┘
```

**Key insight**: Valid mathematical reasoning forms a DAG where each edge represents a valid rule application (e.g., "subtract 5 from both sides").

### 2. Logical Closeness Metric [DAG][Reward][Math]

**Problem**: PASS@k only measures final answer correctness, ignoring whether the derivation path was valid.

**Solution**: Logical closeness quantifies how well a model's CoT trajectory adheres to the DAG structure.

**Logical Closeness Definition**:
```
LC(trajectory, DAG) = Σ P(valid_step | context) / trajectory_length
```

**Intuition**: A model that follows valid derivation paths (even with intermediate errors) scores higher than one that jumps to correct answers through invalid reasoning.

**Comparison to existing metrics**:

| Metric | What it measures | Limitation |
|--------|------------------|------------|
| **PASS@k** | Final answer accuracy | Ignores reasoning quality |
| **Logical Closeness** | Adherence to valid DAG paths | Requires ground-truth DAG |
| **Process Reward Models** | Step-by-step correctness | Expensive to annotate |

### 3. DAG-MATH CoT Format [DAG][Reasoning][Format]

**Structured format** for graph-aware reasoning:
```
<PROBLEM> 2x + 5 = 13. Solve for x.

<STEP_1>
State: 2x + 5 = 13
Rule: subtract_both_sides(5)
New State: 2x = 8
Justification: Isolates variable term

<STEP_2>
State: 2x = 8
Rule: divide_both_sides(2)
New State: x = 4
Justification: Solves for x

<ANSWER> x = 4
```

**Key features**:
- Explicit state tracking
- Rule annotation for each transition
- Justification for each step
- Enables DAG construction from CoT

### 4. Benchmark Construction and Analysis [Train][Reward][Math]

**Methodology**:
1. Convert standard math datasets (MATH, GSM8K, OlympiadBench) to DAG-MATH format
2. Train models to generate DAG-structured CoT via supervised fine-tuning
3. Evaluate both PASS@k and logical closeness across model families

**Key Finding**: Statistically significant differences in reasoning fidelity even when PASS@k comparable:

| Model Family | PASS@k | Logical Closeness | Gap |
|--------------|--------|-------------------|-----|
| GPT-4        | 85.2%  | 0.78              | -7.2% |
| Claude 3     | 84.7%  | 0.71              | -13.7% |
| Llama 3      | 76.3%  | 0.82              | +5.7% |
| Gemma        | 74.8%  | 0.65              | -9.8% |

**Interpretation**: Some models achieve high accuracy through pattern matching (low LC), while others show more rule-consistent reasoning (high LC even with lower PASS@k).

---

## DAG-Specific Considerations [DAG][Reasoning][Math]

DAG-MATH provides a formal framework for DAG-based reasoning evaluation:

1. **Explicit DAG representation**: Mathematical derivations modeled as DAGs with rule-annotated edges, enabling structural analysis of reasoning paths

2. **Logical closeness as DAG adherence metric**: Quantifies how well trajectories follow valid DAG edges rather than measuring only terminal node correctness

3. **Multi-path DAG traversal**: Unlike linear CoT, DAG-MATH acknowledges multiple valid derivation paths to the same answer

4. **State-level DAG nodes**: Each intermediate derivation state explicitly represented, enabling fine-grained credit assignment

5. **Rule-annotated DAG edges**: Transitions labeled with mathematical rules (distributive property, substitution, etc.), enabling explainable reasoning

**Future DAG integration opportunities**:
- RL training with DAG-based rewards that reinforce valid rule applications
- Multi-agent DAG construction where different agents specialize in different rule types
- Hierarchical DAGs for multi-step proof construction with lemma subgraphs
- Causal credit assignment through DAG path analysis

---

## Performance Results

### Mathematical Reasoning Benchmarks

| Dataset | Model | PASS@1 | Logical Closeness |
|---------|-------|--------|-------------------|
| **MATH-500** | GPT-4 | 85.2% | 0.78 |
| **MATH-500** | Claude 3 | 84.7% | 0.71 |
| **MATH-500** | Llama 3 | 76.3% | 0.82 |
| **GSM8K** | GPT-4 | 92.1% | 0.85 |
| **GSM8K** | Claude 3 | 91.4% | 0.79 |
| **OlympiadBench** | GPT-4 | 58.3% | 0.62 |
| **OlympiadBench** | Claude 3 | 56.7% | 0.58 |

### Correlation Analysis

**PASS@k vs Logical Closeness correlation**: r = 0.67

**Interpretation**: Moderate correlation indicates that answer correctness doesn't fully capture reasoning quality—models can achieve similar accuracy through different reasoning strategies.

### Ablation Studies

| Configuration | PASS@1 | Logical Closeness |
|---------------|--------|-------------------|
| DAG-MATH format | 82.3% | 0.79 |
| Standard CoT | 80.1% | 0.65 |
| No intermediate states | 76.8% | 0.52 |

**Key finding**: DAG-structured format improves both final accuracy and reasoning fidelity.

---

## External Resources

- **Paper**: [arXiv:2510.19842](https://arxiv.org/abs/2510.19842)
- **Authors**: Yuanhe Zhang, Ilja Kuzborskij, Jason D. Lee, Chenlei Leng, Fanghui Liu
- **Code & Benchmark**: [github.com/YuanheZ/DAG-MATH-Formatted-CoT](https://github.com/YuanheZ/DAG-MATH-Formatted-CoT)
- **Related Work**:
  - Process Reward Models for step-level supervision
  - Formal proof systems (Lean, Coq)
  - Rule-based mathematical reasoning

---

## Key Insights

1. **Answer accuracy ≠ reasoning quality**: High PASS@k doesn't guarantee rule-consistent derivation; some models pattern-match rather than reason

2. **DAG structure enables richer evaluation**: Logical closeness measures adherence to valid reasoning paths, not just final correctness

3. **Explicit state tracking matters**: DAG-MATH format with state/rule annotations improves both accuracy and reasoning fidelity

4. **Model families differ in reasoning style**: Some models prioritize correctness (high LC), others prioritize efficiency (pattern matching)

5. **Benchmark bridges gap between free-form and formal**: DAG-MATH balances structured reasoning evaluation with practical LLM deployment

6. **Training implications**: DAG-structured CoT can be used for both evaluation and training, enabling reward signals for rule-consistent reasoning
