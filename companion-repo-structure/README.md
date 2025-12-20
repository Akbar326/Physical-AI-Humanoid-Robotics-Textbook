# Physical AI & Humanoid Robotics - Code Examples Repository

**Repository**: `ai-humanoid-robotics-code`
**Purpose**: Code examples, exercises, and datasets for the Physical AI & Humanoid Robotics textbook
**License**: MIT

---

## Quick Start

### Clone the Repository

```bash
git clone https://github.com/physical-ai-lab/ai-humanoid-robotics-code.git
cd ai-humanoid-robotics-code
```

### Setup Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For GPU support (optional)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Run First Example

```bash
# Module 1 - ROS 2 Publisher
cd module-1/chapter-1-1/examples
python3 my_first_node.py
```

---

## Repository Structure

```
ai-humanoid-robotics-code/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── .gitignore                         # Git ignore rules
├── CONTRIBUTING.md                    # Contribution guidelines
├── requirements.txt                   # Python dependencies
│
├── module-1/                          # ROS 2 Fundamentals (19-23 hours)
│   ├── README.md
│   ├── chapter-1-1/                   # ROS 2 Overview
│   │   ├── examples/                  # Working code examples
│   │   ├── exercises/                 # Exercise templates
│   │   └── solutions/                 # Reference solutions
│   ├── chapter-1-2/ through chapter-1-6/  # Other chapters
│   └── shared/                        # Shared resources
│
├── module-2/                          # Gazebo Simulation (21-26 hours)
│   ├── README.md
│   ├── chapter-2-1/ through chapter-2-6/
│   └── shared/                        # Gazebo worlds, models
│
├── module-3/                          # Isaac Sim & AI (19-25 hours)
│   ├── README.md
│   ├── chapter-3-1/ through chapter-3-5/
│   └── shared/                        # Pre-trained models
│
├── module-4/                          # Vision-Language-Action (34-43 hours)
│   ├── README.md
│   ├── chapter-4-1/ through chapter-4-6/
│   └── shared/                        # VLA models, datasets
│
├── shared/                            # Cross-module resources
│   ├── utils/                         # Utility functions
│   ├── config/                        # Configuration templates
│   ├── datasets/                      # Datasets (git-lfs)
│   └── models/                        # Pre-trained models (git-lfs)
│
└── docs/
    └── SETUP.md                       # Links to main textbook setup
```

---

## Module Breakdown

### Module 1: ROS 2 Fundamentals (19-23 hours)

**What You'll Learn**: ROS 2 core concepts, package development, pub-sub communication

**Chapters**:
1. [Chapter 1.1](module-1/chapter-1-1/) - ROS 2 Overview and Installation
2. [Chapter 1.2](module-1/chapter-1-2/) - Packages and Workspaces
3. [Chapter 1.3](module-1/chapter-1-3/) - Publishers and Subscribers
4. [Chapter 1.4](module-1/chapter-1-4/) - Services and Actions
5. [Chapter 1.5](module-1/chapter-1-5/) - Parameters and Launch Files
6. [Chapter 1.6](module-1/chapter-1-6/) - Debugging and Development Tools

**Getting Started**:
```bash
cd module-1/chapter-1-1/
python3 examples/my_first_node.py
```

### Module 2: Gazebo Simulation (21-26 hours)

**What You'll Learn**: Physics simulation, world creation, robot modeling

**Chapters**:
1. [Chapter 2.1](module-2/chapter-2-1/) - Introduction to Simulation
2. [Chapter 2.2](module-2/chapter-2-2/) - Gazebo Basics and World Setup
3. [Chapter 2.3](module-2/chapter-2-3/) - Physics Simulation and Materials
4. [Chapter 2.4](module-2/chapter-2-4/) - Plugins and Custom Simulation
5. [Chapter 2.5](module-2/chapter-2-5/) - Interfacing Robots with Gazebo
6. [Chapter 2.6](module-2/chapter-2-6/) - Advanced Simulation Techniques

**Getting Started**:
```bash
cd module-2/chapter-2-1/
# Follow instructions in README.md
```

### Module 3: Isaac Sim & AI (19-25 hours)

**What You'll Learn**: Advanced simulation, synthetic data, computer vision, ML basics

**Chapters**:
1. [Chapter 3.1](module-3/chapter-3-1/) - Introduction to Isaac Sim
2. [Chapter 3.2](module-3/chapter-3-2/) - Robot Simulation in Isaac Sim
3. [Chapter 3.3](module-3/chapter-3-3/) - Synthetic Data Generation
4. [Chapter 3.4](module-3/chapter-3-4/) - Computer Vision Fundamentals
5. [Chapter 3.5](module-3/chapter-3-5/) - AI and Machine Learning Integration

**Requirements**: NVIDIA GPU (RTX 1060+), CUDA toolkit

### Module 4: Vision-Language-Action (34-43 hours)

**What You'll Learn**: VLA models, language understanding, robot control, end-to-end learning

**Chapters**:
1. [Chapter 4.1](module-4/chapter-4-1/) - Fundamentals of Vision-Language Models
2. [Chapter 4.2](module-4/chapter-4-2/) - Action Prediction and Robot Control
3. [Chapter 4.3](module-4/chapter-4-3/) - Multi-Modal Learning and Fusion
4. [Chapter 4.4](module-4/chapter-4-4/) - Real-World Deployment
5. [Chapter 4.5](module-4/chapter-4-5/) - Advanced VLA Techniques
6. [Chapter 4.6](module-4/chapter-4-6/) - Capstone Project

**Capstone**: Build complete intelligent manipulation system

---

## Chapter Structure

Each chapter directory contains:

```
chapter-X-Y/
├── README.md                 # Chapter-specific instructions
├── examples/                 # Working code examples
│   ├── example1.py
│   ├── example2.py
│   └── data/                 # Example data files
├── exercises/                # Exercise templates
│   ├── exercise1.py
│   ├── exercise2.py
│   └── README.md
└── solutions/                # Reference solutions
    ├── exercise1_solution.py
    ├── exercise2_solution.py
    └── README.md
```

### Using Examples

```bash
# Run an example
cd chapter-1-1/examples
python3 my_first_node.py

# See what the example does
cat README.md

# Try modifying it
cp example1.py my_version.py
# Edit my_version.py...
python3 my_version.py
```

### Working on Exercises

```bash
# Start with the exercise template
cd chapter-1-1/exercises
cat exercise1.py        # See what needs to be implemented

# Implement your solution
python3 exercise1.py    # Test your code

# Compare with reference solution
diff exercise1.py ../solutions/exercise1_solution.py
```

---

## File Organization

### Examples (`examples/`)
- **Purpose**: Complete, working code demonstrations
- **Status**: Fully functional, tested on all platforms
- **Use**: Learn by reading and running
- **Modification**: Feel free to experiment

### Exercises (`exercises/`)
- **Purpose**: Templates for hands-on learning
- **Status**: Incomplete, requires implementation
- **Use**: Test your knowledge
- **Goal**: Make them work like the solutions

### Solutions (`solutions/`)
- **Purpose**: Reference implementations
- **Status**: Complete and tested
- **Use**: Check after attempting exercise
- **Note**: Don't look before trying!

---

## Installation & Setup

### Prerequisites

- Python 3.10 or higher
- Ubuntu 22.04, Windows 10/11 (WSL2), or macOS 12+
- 4GB RAM (8GB recommended)
- 10GB free disk space

### Step 1: Clone Repository

```bash
git clone https://github.com/physical-ai-lab/ai-humanoid-robotics-code.git
cd ai-humanoid-robotics-code
```

### Step 2: Setup Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate          # Linux/macOS
# or
venv\Scripts\activate              # Windows
```

### Step 3: Install Dependencies

```bash
# Install base requirements
pip install -r requirements.txt

# For Module 2 (Gazebo)
source /opt/ros/humble/setup.bash

# For Module 3 (Isaac Sim - GPU required)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# For Module 4 (Vision-Language-Action)
pip install transformers huggingface-hub
```

### Step 4: Verify Installation

```bash
# Test imports
python3 -c "import rclpy; print('ROS 2: OK')"
python3 -c "import numpy; print('NumPy: OK')"
python3 -c "import torch; print('PyTorch: OK')"

# Or run test script
python3 tests/check_installation.py
```

---

## Learning Paths

### Sequential Learning (Start Here)
Complete all 23 chapters in order, 19-117 hours total.

```
Module 1 → Module 2 → Module 3 → Module 4
```

**Best For**: Comprehensive learning, building strong foundations

### Module-by-Module Learning
Complete one module at a time.

**Module 1**: 19-23 hours
**Module 2**: 21-26 hours
**Module 3**: 19-25 hours (requires GPU)
**Module 4**: 34-43 hours (capstone project)

### Fast Track Learning
Focus on specific modules of interest.

**Path 1** (ROS 2 Fundamentals Only): 19-23 hours
**Path 2** (ROS 2 + Gazebo): 40-49 hours
**Path 3** (ROS 2 + Isaac Sim): 38-48 hours

---

## Running Code Examples

### ROS 2 Examples (Module 1)

```bash
# Terminal 1: Source ROS 2
source /opt/ros/humble/setup.bash

# Terminal 2: Run publisher
cd module-1/chapter-1-3/examples
python3 publisher.py

# Terminal 3: Run subscriber
python3 subscriber.py
```

### Gazebo Examples (Module 2)

```bash
# Terminal 1: Start Gazebo
gazebo &

# Terminal 2: Run example
cd module-2/chapter-2-1/examples
python3 spawn_robot.py
```

### Isaac Sim Examples (Module 3)

```bash
# Requires NVIDIA GPU and Isaac Sim installation
cd module-3/chapter-3-1/examples
python3 isaac_example.py
```

### VLA Examples (Module 4)

```bash
# Requires GPU and pre-trained models
cd module-4/chapter-4-1/examples
python3 vision_language_example.py
```

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to add new examples
- Submitting bug reports
- Proposing enhancements
- Code style guidelines
- Testing requirements

### Adding Your Own Examples

1. Create directory: `module-X/chapter-X-Y/my-examples/`
2. Add your code
3. Include README explaining what it does
4. Test on multiple platforms
5. Submit pull request

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'rclpy'"
**Solution**: Source ROS 2:
```bash
source /opt/ros/humble/setup.bash
```

### "ImportError: No module named 'torch'"
**Solution**: Install PyTorch:
```bash
pip install torch torchvision
```

### "Gazebo not found"
**Solution**: Install Gazebo and source ROS 2:
```bash
source /opt/ros/humble/setup.bash
gazebo &
```

### GPU not detected
**Solution**: Verify NVIDIA drivers:
```bash
nvidia-smi
```

### More issues?
See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) or open an issue.

---

## Resources

### Main Textbook
- [Physical AI & Humanoid Robotics Textbook](https://github.com/physical-ai-lab/ai-humanoid-robotics)
- [Full Documentation](https://physical-ai-lab.github.io/ai-humanoid-robotics)

### Official Documentation
- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [Gazebo Documentation](https://gazebosim.org/)
- [NVIDIA Isaac Sim](https://docs.omniverse.nvidia.com/app_isaacsim/)
- [Hugging Face Transformers](https://huggingface.co/transformers/)

### Related Projects
- [TurtleBot3](https://emanual.robotis.com/docs/en/platform/turtlebot3/)
- [ROS 2 Humble](https://docs.ros.org/en/humble/index.html)
- [Gazebo Fortress](https://gazebosim.org/docs/fortress/)

---

## FAQ

**Q: Can I use this without ROS 2?**
A: Some examples (Module 3-4) can run without ROS 2, but Modules 1-2 require it.

**Q: Do I need a GPU?**
A: GPU strongly recommended for Module 3-4. Modules 1-2 work fine on CPU.

**Q: Can I run this on Windows?**
A: Yes! Use WSL2 with Ubuntu 22.04 for full support. Some Windows native support available.

**Q: How do I get help?**
A: Check the relevant chapter README, see [Troubleshooting](docs/TROUBLESHOOTING.md), or open a GitHub issue.

**Q: Can I modify examples?**
A: Absolutely! Experimentation is encouraged. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Citation

If you use this repository in your work, please cite:

```bibtex
@misc{physical_ai_robotics_2025,
  title={Physical AI & Humanoid Robotics: A Comprehensive Textbook},
  author={Physical AI Lab},
  year={2025},
  url={https://github.com/physical-ai-lab/ai-humanoid-robotics-code}
}
```

---

## Contact & Support

- **Issues**: [GitHub Issues](https://github.com/physical-ai-lab/ai-humanoid-robotics-code/issues)
- **Discussions**: [GitHub Discussions](https://github.com/physical-ai-lab/ai-humanoid-robotics-code/discussions)
- **Main Textbook**: [ai-humanoid-robotics](https://github.com/physical-ai-lab/ai-humanoid-robotics)

---

**Last Updated**: 2025-12-16
**Status**: Ready for use across all 4 modules
**Total Code Examples**: 100+
**Total Exercises**: 50+

**Enjoy learning Physical AI & Humanoid Robotics! 🤖**
