# DreamGym: Scaling Agent Learning via Experience Synthesis

Implementation of the DreamGym framework from the paper "Scaling Agent Learning via Experience Synthesis" (arXiv:2511.03773).

## Overview

DreamGym is a unified framework that synthesizes diverse experiences to enable effective online reinforcement learning (RL) training for autonomous agents. It addresses the challenges of costly rollouts, limited task diversity, unreliable reward signals, and infrastructure complexity.

### Key Features

- **Reasoning Experience Model**: Generates state transitions through chain-of-thought reasoning instead of expensive real environment rollouts
- **Experience Replay Buffer**: Stores and manages both real-world and synthesized experiences with quality filtering
- **Curriculum Task Generator**: Adaptively generates tasks at appropriate difficulty levels based on agent performance
- **PPO Training**: Implements Proximal Policy Optimization for policy learning
- **Multi-Environment Support**: Designed for WebArena, ALFWorld, and Tau-Bench

## Project Structure

```
DreamGym/
├── src/dreamgym/
│   ├── core/               # Core data structures and configuration
│   │   ├── data_structures.py
│   │   └── config.py
│   ├── models/             # Core components
│   │   ├── reasoning_model.py
│   │   ├── replay_buffer.py
│   │   └── curriculum_generator.py
│   ├── training/           # Training pipeline
│   │   ├── policy.py
│   │   ├── ppo.py
│   │   ├── trainer.py
│   │   ├── train.py
│   │   └── evaluate.py
│   ├── environments/       # Environment integrations
│   │   └── base_env.py
│   └── utils/              # Utility functions
├── configs/                # Configuration files
│   └── default.yaml
├── data/                   # Data storage
│   ├── offline/            # Offline demonstration data
│   ├── experiences/        # Experience replay data
│   └── checkpoints/        # Model checkpoints
├── tests/                  # Unit and integration tests
├── logs/                   # Training logs
├── results/                # Experiment results
├── requirements.txt        # Python dependencies
└── setup.py               # Package setup

```

## Installation

### Prerequisites

- Python 3.9 or higher
- CUDA-capable GPU (recommended for faster training)
- 32GB+ RAM (64GB+ recommended)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd DreamGym
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

4. Set up API keys (optional, for LLM access):
```bash
export OPENAI_API_KEY="your-api-key"
# or
export ANTHROPIC_API_KEY="your-api-key"
```

## Quick Start

### Training

Train the DreamGym agent with default configuration:

```bash
python -m dreamgym.training.train
```

With custom configuration:

```bash
python -m dreamgym.training.train --config configs/custom.yaml
```

With command-line overrides:

```bash
python -m dreamgym.training.train \
    --env webarena \
    --num-iterations 100 \
    --batch-size 64 \
    --use-wandb \
    --seed 42
```

### Evaluation

Evaluate a trained policy:

```bash
python -m dreamgym.training.evaluate \
    --checkpoint data/checkpoints/policy_iter_0100.json \
    --env webarena \
    --num-episodes 20 \
    --output results/eval_results.json
```

## Configuration

The system is configured via YAML files. Key configuration sections:

- `reasoning_model`: Reasoning experience model settings
- `policy_model`: Agent policy model settings
- `buffer`: Experience replay buffer parameters
- `curriculum`: Curriculum learning parameters
- `rl`: RL algorithm hyperparameters
- `training`: Training loop settings
- `environment`: Environment configuration

See `configs/default.yaml` for a complete example.

## Core Components

### 1. Reasoning Experience Model

Generates synthetic state transitions using LLM-based reasoning:

```python
from dreamgym.models.reasoning_model import ReasoningExperienceModel
from dreamgym.core.config import ReasoningModelConfig

config = ReasoningModelConfig()
reasoning_model = ReasoningExperienceModel(config, llm_client)

experience = reasoning_model.generate_experience(
    state=current_state,
    action=agent_action,
    task=task
)
```

### 2. Experience Replay Buffer

Stores and samples experiences for training:

```python
from dreamgym.models.replay_buffer import ExperienceReplayBuffer
from dreamgym.core.config import BufferConfig

config = BufferConfig(capacity=100000)
buffer = ExperienceReplayBuffer(config)

# Add experiences
buffer.add_experience(experience)

# Sample for training
batch = buffer.sample_balanced(batch_size=64)
```

### 3. Curriculum Task Generator

Adaptively generates tasks based on agent performance:

```python
from dreamgym.models.curriculum_generator import CurriculumTaskGenerator
from dreamgym.core.config import CurriculumConfig

config = CurriculumConfig()
generator = CurriculumTaskGenerator(config)

# Generate tasks
tasks = generator.generate_tasks(num_tasks=10, llm_client=llm_client)

# Update performance
generator.update_performance(completed_episode)
```

## Training Pipeline

The main training loop integrates all components:

1. **Task Generation**: Curriculum generator creates tasks at appropriate difficulty
2. **Experience Collection**: Agent performs rollouts (synthetic or real)
3. **Buffer Management**: Experiences stored with quality filtering
4. **Policy Update**: PPO updates policy using sampled experiences
5. **Evaluation**: Periodic evaluation and checkpoint saving

## Experiments

### Reproducing Paper Results

To reproduce results from the paper:

1. **WebArena Experiments**:
```bash
python -m dreamgym.training.train --config configs/webarena.yaml
```

2. **ALFWorld Experiments**:
```bash
python -m dreamgym.training.train --config configs/alfworld.yaml
```

3. **Tau-Bench Experiments**:
```bash
python -m dreamgym.training.train --config configs/taubench.yaml
```

### Ablation Studies

Run ablation studies by modifying configuration:

- **Without Reasoning Model**: Set `buffer.synthetic_ratio = 0.0`
- **Without Curriculum**: Set `curriculum.difficulty_increment = 0.0`
- **Synthetic Only**: Remove offline real data

## Development

### Running Tests

```bash
pytest tests/
```

With coverage:

```bash
pytest tests/ --cov=dreamgym --cov-report=html
```

### Code Style

Format code with Black:

```bash
black src/
```

Lint with flake8:

```bash
flake8 src/
```

Type checking with mypy:

```bash
mypy src/
```

## Monitoring and Logging

### TensorBoard

View training metrics:

```bash
tensorboard --logdir logs/
```

### Weights & Biases

Enable W&B logging:

```bash
python -m dreamgym.training.train --use-wandb
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the package is installed with `pip install -e .`
2. **Out of Memory**: Reduce batch size or buffer capacity
3. **Slow Training**: Enable GPU acceleration, reduce max episode steps
4. **Poor Quality Experiences**: Adjust quality threshold or validation settings

### Debug Mode

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Citation

If you use this implementation, please cite the original paper:

```bibtex
@article{chen2025dreamgym,
  title={Scaling Agent Learning via Experience Synthesis},
  author={Chen, Zhaorun and others},
  journal={arXiv preprint arXiv:2511.03773},
  year={2025}
}
```

## License

This implementation is provided for research purposes.

## Acknowledgments

This is a reproduction of the DreamGym framework described in arXiv:2511.03773. The original research was conducted by researchers from multiple institutions.

## Contact

For questions about this implementation, please open an issue on the repository.
