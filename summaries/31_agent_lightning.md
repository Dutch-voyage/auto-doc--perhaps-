# Agent Lightning⚡
#AI_Agents [Reinforcement_Learning] [Framework] [Microsoft] [Multi-Agent_Systems] [Zero_Code_Change] [Training_Optimization]

## Summary

Agent Lightning is Microsoft's open-source framework that enables reinforcement learning training for **ANY** AI agent with **zero code change** (almost). It provides a flexible and extensible system that turns existing agents into optimizable systems while maintaining compatibility with all major agent frameworks.

## Key Technical Innovations [Framework][Reinforcement_Learning]

### Decoupled Architecture [System_Design][Multi_Agent_Systems]

![Agent Lightning Architecture](./images/agent_lightning_architecture.svg)

**Figure 1**: Agent Lightning's decoupled architecture showing how the framework separates agent execution from training optimization

- **Zero Lock-in Design**: Agents continue running as usual with any framework (LangChain, OpenAI Agent SDK, AutoGen, CrewAI, etc.)
- **Lightweight Integration**: Simple `agl.emit_xxx()` helpers or automatic tracer for prompts, tool calls, and rewards
- **LightningStore**: Central hub that synchronizes tasks, resources, and traces between agents and training algorithms

### Multi-Algorithm Support [Training][Algorithm_Diversity]

- **Reinforcement Learning**: Core RL training for agent optimization
- **Automatic Prompt Optimization**: Refines prompt templates automatically
- **Supervised Fine-tuning**: Traditional SFT capabilities
- **Custom Algorithms**: Extensible framework for writing custom optimization algorithms

### Selective Optimization [Multi-Agent_Systems][Training_Efficiency]

- **Targeted Training**: Optimize one or more agents selectively in multi-agent systems
- **Resource Management**: Efficient resource allocation and synchronization
- **Streaming Pipeline**: Real-time dataset streaming to runners and trainers

## Technical Architecture [System_Design][Distributed_Systems]

### Core Components [System_Architecture]

1. **Agent Layer**: Existing agents run unchanged with framework integration
2. **Event Collection**: Automatic tracing of prompts, tool calls, and rewards
3. **LightningStore**: Central synchronization hub for tasks and resources
4. **Algorithm Engine**: Pluggable algorithms for different optimization strategies
5. **Trainer**: Orchestrates the entire training pipeline

### Integration Patterns [Framework_Compatibility][API_Design]

- **Framework Agnostic**: Works with any agent framework or pure Python OpenAI
- **Minimal Invasion**: Drop-in helpers without requiring code restructuring
- **Gradual Adoption**: Start with simple tracing and progress to full optimization

## External Resources [Documentation][Community]

**Official Resources:**
- [Documentation Website](https://microsoft.github.io/agent-lightning/)
- [GitHub Repository](https://github.com/microsoft/agent-lightning)
- [arXiv Paper](https://arxiv.org/abs/2508.03680)
- [Microsoft Research Project Page](https://www.microsoft.com/en-us/research/project/agent-lightning/)

**Community Projects:**
- [DeepWerewolf](https://github.com/af-74413592/DeepWerewolf) - Chinese Werewolf game case study
- [AgentFlow](https://agentflow.stanford.edu/) - Multi-agent framework with Flow-GRPO algorithm

**Installation:**
```bash
pip install agentlightning
```