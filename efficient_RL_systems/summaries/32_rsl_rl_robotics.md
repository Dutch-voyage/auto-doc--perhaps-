# RSL-RL: Robotics Reinforcement Learning Library
#Robotics [Reinforcement_Learning] [GPU_Optimization] [PPO] [ETH_Zurich] [NVIDIA] [Fast_Training]

## Summary

RSL-RL is a fast and simple implementation of learning algorithms specifically designed for robotics applications from the Robotic Systems Lab at ETH Zurich & NVIDIA. The library focuses on GPU-accelerated training with implementations of PPO and Student-Teacher Distillation, enhanced with advanced research features like curiosity-driven exploration and symmetry-based augmentation.

## Key Technical Innovations [Robotics][GPU_Optimization]

### GPU-Accelerated Training [Performance][GPU-side]
- **Fast Implementation**: Designed to run fully on GPU for maximum performance
- **Simple Architecture**: Clean, straightforward codebase optimized for robotics workloads
- **Multiple Environment Support**: Compatible with major robotics simulation platforms

### Algorithm Support [Reinforcement_Learning][Training_Algorithms]

**Core Algorithms:**
- **PPO (Proximal Policy Optimization)**: Industry-standard RL algorithm
- **Student-Teacher Distillation**: Knowledge transfer between policies

**Research Features:**
- **Random Network Distillation (RND)**: Intrinsic reward for exploration encouragement
- **Symmetry-based Augmentation**: Enforces symmetric behaviors for better generalization

## Environment Ecosystem [Framework_Integration][Simulation_Support]

### Supported Platforms [Multi_Framework][Simulation]

**Primary Environments:**
- **Isaac Lab**: Built on NVIDIA Isaac Sim for advanced robotics simulation
- **Legged Gym**: Built on NVIDIA Isaac Gym specifically for legged robots
- **MuJoCo Playground**: Built on MuJoCo MJX and Warp for physics simulation
- **mjlab**: Built on MuJoCo Warp for enhanced performance

### Integration Benefits [Interoperability][Research_Infrastructure]
- **Unified Interface**: Common API across different simulation environments
- **Research Pipeline**: End-to-end workflow from simulation to deployment
- **Community Ecosystem**: Active development and contribution from robotics community

## Technical Architecture [System_Design][Performance]

### Core Features [Implementation_Details][Logging]
- **Multiple Logging Frameworks**: Tensorboard, Weights & Biases, Neptune support
- **Configuration Management**: YAML-based configuration system
- **Code Quality**: Pre-commit hooks, ruff linting, Google-style documentation

### Performance Optimization [GPU_side][Training_Efficiency]
- **GPU-Native Design**: Fully leverages GPU parallel processing
- **Memory Efficiency**: Optimized for large-scale robotics training
- **Scalability**: Designed for both research and production deployments

## Research Applications [Robotics_Research][Academic_Research]

### Maintainers and Affiliation [Research_Institution][Industry_Collaboration]
- **Maintainers**: Mayank Mittal and Clemens Schwarke
- **Affiliation**: Robotic Systems Lab, ETH Zurich & NVIDIA
- **Contact**: cschwarke@ethz.ch

### Citation Impact [Academic_Contributions][Research_Papers]
The library has been used in multiple research publications covering:
- Curiosity-driven learning for locomotion and manipulation
- Symmetry considerations in robot policy learning
- Large-scale robotics training systems

## External Resources [Documentation][Installation]

**Official Resources:**
- [GitHub Repository](https://github.com/leggedrobotics/rsl_rl)
- [Overview Paper](https://arxiv.org/pdf/2509.10771)
- [Legged Gym Documentation](https://leggedrobotics.github.io/legged_gym/)
- [Isaac Lab Repository](https://github.com/isaac-sim/IsaacLab)

**Installation:**
```bash
pip install rsl-rl-lib
```

**Development Setup:**
```bash
git clone https://github.com/leggedrobotics/rsl_rl
cd rsl_rl
pip install -e .
```