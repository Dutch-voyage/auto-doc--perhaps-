# Tags - DAG-Based Training Systems

This document defines the taxonomy for tagging materials related to DAG-based training systems for multi-modal agentic reasoning.

---

## Three Main Categories

| Category | Symbol | Description |
|----------|--------|-------------|
| **System Topics** | [ST] | Hardware and system-level design |
| **Training Phases** | [TP] | Stages and methods in the training loop |
| **Application** | [APP] | Use cases and deployment scenarios |

---

## 1. System Topics [ST]

Focus: System architecture, hardware utilization, distributed execution

| Tag | Description | Related Keywords |
|-----|-------------|------------------|
| `[DAG]` | Graph-based computation structure | topology, nodes, edges, directed graph |
| `[Async]` | Asynchronous execution patterns | non-blocking, concurrent, parallel |
| `[Batch]` | Batching strategies for efficiency | node batching, topological batching |
| `[Shard]` | Weight/data sharding across devices | tensor parallel, model parallel |
| `[Runtime]` | Runtime optimization and scheduling | inference engine, execution manager |
| `[Network]` | Communication and data transfer | distributed training, gradient sync |
| `[GPU]` | GPU-specific optimizations | CUDA, memory management, kernels |

---

## 2. Training Phases [TP]

Focus: Training methodology, data flow, optimization techniques

| Tag | Description | Related Keywords |
|-----|-------------|------------------|
| `[SFT]` | Supervised Fine-Tuning | imitation learning, behavioral cloning |
| `[RL]` | Reinforcement Learning | policy gradient, reward optimization |
| `[Rollout]` | Data generation/inference phase | exploration, episode generation |
| `[Train]` | Backward pass and weight updates | gradient descent, optimizer step |
| `[Chunk]` | Chunk-based data organization | uniform chunks, long context |
| `[Reward]` | Reward design and attribution | credit assignment, verifier |
| `[Oracle]` | Ground truth injection | interventional training, correction |
| `[Sync]` | Weight synchronization | parameter server, weight transfer |

---

## 3. Application [APP]

Focus: Use cases, task types, deployment scenarios

| Tag | Description | Related Keywords |
|-----|-------------|------------------|
| `[Reasoning]` | Complex logical inference | multi-step, chain-of-thought |
| `[MultiModal]` | Cross-modal data processing | vision-language, audio-text |
| `[Agent]` | Agentic tool use | function calling, tool augmentation |
| `[Verifier]` | Verifiable reward scenarios | math, coding, formal verification |
| `[MultiAgent]` | Multi-agent collaboration | cooperative, competitive |
| `[Alignment]` | Safety and alignment training | HH-RLHF, preference optimization |
| `[Coding]` | Code generation tasks | programming, synthesis |
| `[Math]` | Mathematical problem solving | theorem proving, calculation |

---

## Usage Format

Apply tags using bracketed notation:

```markdown
# DistFlow: Distributed RL Framework
[ST][DAG][Async][Batch] | [TP][Rollout][Train][Sync] | [APP][Reasoning][MultiModal]

## Key Innovation [DAG][Async]
...
```

---

## Guidelines for Expanding New Tags

### 1. Check Existing Tags First
Before adding a new tag, verify that:
- The concept is not already covered by an existing tag
- The new tag cannot be expressed as a combination of existing tags
- The new tag represents a fundamentally distinct concept

### 2. New Tag Proposal Template

When proposing a new tag, document:

| Field | Description |
|-------|-------------|
| **Tag Name** | Concise identifier (2-15 characters) |
| **Category** | [ST], [TP], or [APP] |
| **Rationale** | Why this tag is needed |
| **Scope** | What materials it applies to |
| **Related Tags** | Similar or complementary existing tags |

### 3. Category Placement Rules

**System Topics [ST]** - Add when:
- Relates to hardware, infrastructure, or execution engine
- Describes how components are distributed or scheduled
- Involves communication, memory, or compute optimization

**Training Phases [TP]** - Add when:
- Describes a stage in the training loop
- Involves data transformation, optimization, or update
- Relates to how models learn from feedback

**Application [APP]** - Add when:
- Describes a specific use case or task domain
- Relates to what the model is being trained to do
- Involves deployment scenario or target application

### 4. Tag Coherence Principles

1. **Consistent Naming**: Use existing terminology from literature
2. **Avoid Overlap**: Each tag should have a distinct meaning
3. **Hierarchical When Needed**: Use `Parent_Child` format for subcategories
4. **Keep It Simple**: Prefer shorter, more recognizable names

### 5. Examples of Good vs Bad Tags

| Good Tag | Why | Bad Tag | Why |
|----------|-----|---------|-----|
| `[Async]` | Standard term, concise | `[Asynchronous_Execution]` | Too verbose |
| `[Verifier]` | Clear, specific | `[GoodThing]` | Too vague |
| `[DAG]` | Universally recognized | `[GraphBased]` | Less standard |

---

## Tag Quick Reference

```bash
# System Topics [ST]
DAG, Async, Batch, Shard, Runtime, Network, GPU

# Training Phases [TP]
SFT, RL, Rollout, Train, Chunk, Reward, Oracle, Sync

# Application [APP]
Reasoning, MultiModal, Agent, Verifier, MultiAgent, Alignment, Coding, Math
```
