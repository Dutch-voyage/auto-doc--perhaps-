# slime: SGLang-Native Post-Training Framework for RL Scaling
#Hardware_Topics #GPU-side #CPU-side #System_/_Runtime
#RL_Training_phases #Inference #Training #Experience_Buffer_/_Replay
#Scenarios #Multi-agents #GUI-agent

## Summary [System_/_Runtime][RL_Training_phases]

slime is a **lightweight, maintainable post-training framework** built specifically for **RL scaling** with native SGLang integration. Developed collaboratively by LMSYS and THUDM, it provides **high-performance training capabilities** and has quietly powered many production post-training pipelines and large MoE (Mixture of Experts) runs.

## Repository Architecture [System_/_Runtime][Inference]

### Core Framework Design [GPU-side][CPU-side]
- **Deep SGLang integration** enabling deterministic inference for reproducible RL training
- **Lightweight architecture** focused on maintainability and production deployment
- **Modular systematic design** for comprehensive RL workflow management
- **Framework interoperability** designed to work alongside major LLM frameworks

### Performance Optimizations [GPU-side][System_/_Runtime]
- **Memory pooling systems** reducing allocation overhead during RL training
- **Custom CUDA/ROCm kernels** for performance-critical operations
- **Kernel fusion techniques** combining multiple operations to reduce launch overhead
- **Dynamic memory allocation** strategies optimized for RL workloads
- **Efficient memory reuse** mechanisms for intermediate tensors and activations

### Multi-Modal and Tool Support [Multi-agents][Experience_Buffer_/_Replay]
- **Holistic agentic RL** supporting comprehensive agent-based scenarios
- **Standardized tool management** with unified APIs for different modalities
- **Multi-turn LLM agent optimization** for complex conversational scenarios
- **Versatile framework** supporting code-generation models and RL training systems

## Technical Features [RL_Training_phases][Hardware_Topics]

### Training Modes [Training][Inference]
- **Colocated or decoupled** training setups for different deployment scenarios
- **Synchronous or asynchronous** execution modes for flexible RL workflows
- **RL or DPO** algorithm support for diverse training paradigms
- **Fully customizable rollout interface** for flexible experimentation

### Hardware Compatibility [GPU-side][System_/_Runtime]
- **AMD ROCm optimization** with dedicated platform-specific performance improvements
- **Cross-platform compatibility** designed for different hardware architectures
- **Hardware-aware deployment** strategies tuned for specific configurations
- **Efficient resource management** for distributed training across nodes/GPUs

### Integration Capabilities [System_/_Runtime][Experience_Buffer_/_Replay]
- **SGLang rollout + Megatron training** seamless integration patterns
- **Framework extensibility** with modular architecture for customization
- **Production integration** capabilities with existing ML infrastructure
- **Multi-framework support** enabling flexible deployment strategies

## Production Impact [Hardware_Topics][RL_Training_phases]

### Real-World Deployment [System_/_Runtime]
- **Battle-tested framework** with proven success in large MoE deployments
- **Foundation technology** serving as base for advanced frameworks like Miles
- **Real-world adoption** having quietly powered many post-training pipelines
- **Enterprise scalability** supporting large-scale commercial RL operations

### Research Foundation [Multi-agents][Training]
- **Academic research foundation** incorporating latest advances in efficient AI computing
- **Cutting-edge RL research** support for exploring new algorithms and techniques
- **Open-source contribution** enabling community collaboration and improvement
- **FP8 integration initiatives** for moving beyond mixed precision in stable RL

## Repository Resources [System_/_Runtime]

### Official Links
- **GitHub Repository**: [https://github.com/THUDM/slime](https://github.com/THUDM/slime)
- **Official Documentation**: Comprehensive README and installation guides
- **LMSYS Blog**: [Detailed technical blog post](https://lmsys.org/blog/2025-07-09-slime/)
- **Community Support**: Active development and maintenance

### Platform Support
- **AMD ROCm Integration**: [AMD ROCm Blog Post](https://rocm.blogs.amd.com/artificial-intelligence/slime/README.html)
- **Multi-Platform Deployment**: Support for CUDA and ROCm platforms
- **Hardware Optimization**: Platform-specific performance enhancements

### Framework Integration
- **SGLang Native Integration**: Seamless SGLang compatibility
- **Megatron Training**: Integration with Megatron training frameworks
- **Framework Ecosystem**: Part of broader LLM training infrastructure

## Use Cases and Applications [Multi-agents][Training]

### Large-Scale Model Training [GPU-side][RL_Training_phases]
- **Mixture of Experts (MoE) models** optimization for massive parameter counts
- **Multi-modal RL training** supporting text, code, and vision applications
- **Agent-based learning** for complex, multi-turn interaction scenarios
- **Production pipeline integration** for continuous model improvement

### Research Applications [Multi-agents][Experience_Buffer_/_Replay]
- **Reproducible RL training** through deterministic inference capabilities
- **Algorithm experimentation** with flexible and customizable framework
- **Performance benchmarking** with optimized baseline implementations
- **Systems research** for advancing RL training infrastructure

slime represents a **significant advancement** in RL training infrastructure by providing **both SGLang's inference optimizations and production-ready RL training capabilities** in a unified, maintainable framework that has already proven its value in real-world deployments.