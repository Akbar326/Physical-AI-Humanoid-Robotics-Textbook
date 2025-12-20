---
title: Prerequisites & System Requirements
sidebar_position: 2
---

# Prerequisites & System Requirements

## Programming Prerequisites

### Required Knowledge

- **Python**: Comfortable with basic syntax (variables, loops, functions, classes)
  - If you need to review: [Python official tutorial](https://docs.python.org/3/tutorial/)
- **Terminal/Command Line**: Comfortable navigating directories and running commands
  - Linux/macOS: Bash shell
  - Windows: PowerShell or Windows Terminal
- **Git**: Basic understanding of version control (clone, commit, push)
  - If you need to review: [Git Handbook](https://guides.github.com/introduction/git-handbook/)

### Optional (Helpful But Not Required)

- **C++**: Some Isaac Sim examples use C++, but Python alternatives provided
- **Docker**: Helpful for isolation, but not required
- **Bash Scripting**: Useful but optional

## System Requirements

### Operating System Support

This textbook supports **three operating systems** with full native support:

| OS | Version | Status | Notes |
|----|---------|--------|-------|
| **Ubuntu** | 22.04 LTS | ✅ Primary | Recommended for ROS 2 development |
| **Windows** | 10/11 | ✅ Supported | Native Windows 11 recommended |
| **macOS** | 12+ (Monterey+) | ✅ Supported | Intel or Apple Silicon |

### Hardware Requirements

#### Minimum (Module 1-2 Only)

- **CPU**: 4 cores (Intel i5/Ryzen 5 equivalent)
- **RAM**: 8 GB
- **Disk**: 20 GB free space
- **GPU**: Integrated graphics acceptable

#### Recommended (All Modules)

- **CPU**: 8 cores (Intel i7/Ryzen 7 equivalent)
- **RAM**: 16 GB
- **Disk**: 50 GB free space (SSD strongly recommended)
- **GPU**: NVIDIA GPU (GTX 1060+ or better) for Isaac Sim

#### For Isaac Sim (Module 3-4)

- **GPU**: NVIDIA GPU required
  - **Minimum**: GTX 1060 (6GB VRAM)
  - **Recommended**: RTX 3060+ (12GB VRAM)
  - **Optimal**: RTX 4080/4090 (24GB VRAM)
- **CUDA**: NVIDIA CUDA Toolkit 12.0+
- **GPU Driver**: Latest NVIDIA driver

### Virtual Machine Options

If you don't have native Ubuntu, use:

- **Ubuntu VM**: VirtualBox, VMware, or Hyper-V
  - Allocate: 8+ cores, 16+ GB RAM, 50 GB storage
  - GPU passthrough for Isaac Sim (advanced)
- **WSL2** (Windows Subsystem for Linux 2)
  - Best option for Windows users
  - Supports GPU access with latest NVIDIA drivers
- **macOS**: Docker Desktop or native macOS (preferred)

## Software Prerequisites

### Module 1: ROS 2 (Basic Requirements)

Required:
- **Ubuntu 22.04**, Windows 10/11, or macOS 12+
- **Python 3.10+**
- **Git**
- **Text editor**: VS Code, Sublime Text, or similar
- **Terminal**: Bash (Linux/macOS), PowerShell/CMD (Windows)

### Module 2: Simulation (Additional)

Required:
- **Gazebo Fortress** (simulates with ROS 2)
- **Unity 2022 LTS** (visualization)
- **Visual Studio** or build tools

### Module 3: AI Model Training (GPU Required)

Required:
- **NVIDIA GPU** (RTX 1060+ minimum)
- **NVIDIA CUDA Toolkit 12.0+**
- **cuDNN**
- **NVIDIA Isaac Sim 2023.1**
- **PyTorch or TensorFlow**

### Module 4: Vision-Language-Action

Required:
- All Module 3 requirements
- **Hugging Face Transformers**
- **OpenAI Whisper** (speech recognition)
- **YOLO v8** (object detection)

## Installation Guides

Quick links to setup:

- **[Ubuntu 22.04 Setup](./setup-guide.md#ubuntu)** - Complete ROS 2 installation
- **[Windows 10/11 Setup](./setup-guide.md#windows)** - PowerShell scripts
- **[macOS Setup](./setup-guide.md#macos)** - Homebrew installation
- **[GPU Setup](./setup-guide.md#gpu)** - NVIDIA driver configuration

## Browser Requirements

For accessing this textbook online:

- **Modern browser**: Chrome, Firefox, Safari, or Edge
- **JavaScript enabled**: Required for interactive components
- **Local testing**: Node.js 18+ for running local copy

## Bandwidth & Internet

- **Initial download**: ~2-5 GB for all dependencies
- **During learning**:
  - Downloading models: ~5-10 GB for full VLA models
  - Video tutorials (optional): ~100 MB per video
- **Recommended**: Stable internet connection (100+ Mbps)

## Data & Storage Breakdown

| Component | Size | Notes |
|-----------|------|-------|
| Source code (chapters) | ~100 MB | Markdown + examples |
| ROS 2 + Gazebo | ~8 GB | Full installation |
| Unity 2022 LTS | ~20 GB | Full editor |
| NVIDIA Isaac Sim | ~30 GB | Full installation |
| Python + PyTorch | ~10 GB | With CUDA toolkit |
| Pre-trained models | ~15 GB | YOLO, LLMs, etc. |
| Workspace/projects | ~20 GB | Student code |
| **Total** | **~100 GB** | Across all modules |

## Knowledge Checklist

Before starting, verify you can:

- [ ] Open and edit Python files
- [ ] Run Python scripts from terminal: `python script.py`
- [ ] Clone a GitHub repository: `git clone <url>`
- [ ] Install Python packages: `pip install package-name`
- [ ] Navigate directories in terminal: `cd`, `ls`, `pwd`
- [ ] View file contents: `cat`, `more`, or editor

**Can't do these?** Review [Basic Terminal Tutorial](./how-to-use.md#terminal-basics)

## Common Issues & Solutions

### "Python command not found"

**Solution**: Python 3.10+ not in PATH
- Linux/macOS: `sudo apt install python3.10` or `brew install python3.10`
- Windows: Download from [python.org](https://www.python.org/)

### "No NVIDIA GPU detected"

**Solutions**:
- Check driver: `nvidia-smi`
- Update driver to 525+ from [NVIDIA website](https://www.nvidia.com/Download/driverDetails.html/)
- For WSL2: Update WSL kernel and NVIDIA driver

### "Out of disk space"

**Solution**: Isaac Sim and dependencies require 50+ GB
- Clean unnecessary files
- Use external SSD for storage
- Consider cloud alternatives

### "Module not found" errors

**Solution**: Virtual environment issues
- Use Python virtual environments (recommended)
- See [Setup Guide - Virtual Environments](./setup-guide.md#virtual-environments)

## Next Steps

1. **Check your system**: Verify OS, Python version, and GPU (if needed)
2. **Follow setup guide**: [Complete Setup Instructions](./setup-guide.md)
3. **Verify installation**: Run test commands
4. **Start Module 1**: [Welcome to ROS 2](../module-1/chapter-1-1.md)

**Questions?** Check [How to Use This Book](./how-to-use.md) or open an issue on GitHub.
