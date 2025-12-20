---
title: Complete Setup Guide
sidebar_position: 4
---

# Complete Setup Guide

This guide covers installation for all supported operating systems: **Ubuntu 22.04**, **Windows 10/11**, and **macOS 12+**.

## Quick Start

**Choose your operating system:**

- [🐧 Ubuntu 22.04](#ubuntu)
- [🪟 Windows 10/11](#windows)
- [🍎 macOS 12+](#macos)
- [📦 GPU Setup (Optional)](#gpu-setup)

---

## Ubuntu 22.04

### Prerequisites Check

```bash
# Check Ubuntu version
lsb_release -a
# Should show: Ubuntu 22.04.x LTS

# Check existing Python
python3 --version
# Should show: Python 3.10 or higher
```

### Step 1: Update System

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y build-essential curl wget git
```

### Step 2: Install Python 3.10+

```bash
# Ubuntu 22.04 comes with Python 3.10
python3 --version

# If needed, install dev tools
sudo apt install -y python3-dev python3-pip python3-venv
```

### Step 3: Install ROS 2 Humble

```bash
# Add ROS 2 repository
sudo curl -sSL https://raw.githubusercontent.com/ros/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Update and install
sudo apt update
sudo apt install -y ros-humble-desktop
```

### Step 4: Setup Bash Environment

```bash
# Add to ~/.bashrc
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

# Verify
echo $ROS_DISTRO
# Should show: humble
```

### Step 5: Install Build Tools

```bash
sudo apt install -y python3-colcon-common-extensions
sudo apt install -y python3-rosdep2
sudo rosdep init
rosdep update
```

### Step 6: Create Workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
```

### Step 7: Install Gazebo

```bash
sudo apt install -y gazebo
sudo apt install -y ros-humble-gazebo-ros-pkgs
```

### Step 8: Install Additional Tools

```bash
# Terminal tools
sudo apt install -y tmux vim nano

# Python packages
pip3 install --user numpy scipy matplotlib

# VSCode (optional)
sudo apt install -y code
```

### Verification

```bash
# Test ROS 2
ros2 --version

# Test Gazebo
gazebo --version

# Test colcon
colcon --help
```

**✅ Ubuntu setup complete!**

---

## Windows 10/11

### Prerequisites Check

```powershell
# Run PowerShell as Administrator

# Check Windows version
Get-WmiObject -Class Win32_OperatingSystem | Select-Object Caption
# Should show: Windows 10 or Windows 11

# Check Python
python --version
# Should show: Python 3.10 or higher
```

### Step 1: Install Python 3.10+

**Option A: Direct Download**

1. Visit [python.org](https://www.python.org/downloads/)
2. Download **Python 3.10.x or higher**
3. Run installer with **"Add Python to PATH"** checked
4. Verify: `python --version`

**Option B: Chocolatey**

```powershell
# If Chocolatey installed
choco install python310

# If not, install Chocolatey first
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### Step 2: Install Git

```powershell
# Download from git-scm.com or use package manager
choco install git
```

### Step 3: Install Build Tools

```powershell
# Install Microsoft C++ Build Tools
# Download from Microsoft website and run installer

# Or use Chocolatey
choco install visualstudio2022-workload-nativedesktop -y
```

### Step 4: Install ROS 2 Windows Binary

```powershell
# Download pre-built Windows binary
# From https://github.com/ros2/ros2/releases
# Download: ros2-humble-windows-*.zip

# Extract to C:\ros2_humble
# (Adjust path as needed)

# Add to PATH permanently
$env:Path += ";C:\ros2_humble\bin;C:\ros2_humble\Scripts"

# Or set permanently in Environment Variables
# System Properties → Environment Variables → Edit PATH
```

### Step 5: Setup Environment

```powershell
# Create setup.ps1 in your project directory
$ROS_DISTRO="humble"
$PYTHONPATH="C:\ros2_humble\Lib\site-packages"

# Run before development
.\setup.ps1
```

### Step 6: Install Python Dependencies

```powershell
pip install numpy scipy matplotlib
pip install colcon-common-extensions
```

### Step 7: Create Workspace

```powershell
mkdir C:\ros2_ws\src
cd C:\ros2_ws
colcon build --merge-install
```

### Step 8: Install Gazebo

```powershell
# Download Windows binary from gazebosim.org
# Or use pre-built ROS 2 Windows with Gazebo included
```

### Verification

```powershell
ros2 --version
python --version
colcon --help
```

**Troubleshooting Windows Issues**

| Issue | Solution |
|-------|----------|
| "ros2 not found" | Add C:\ros2_humble\bin to PATH |
| "Python not found" | Reinstall Python with "Add to PATH" checked |
| Build fails | Install Visual C++ Build Tools |
| Port conflicts | Change ROS_DOMAIN_ID |

**✅ Windows setup complete!**

---

## macOS 12+

### Prerequisites Check

```bash
# Check macOS version
sw_vers -productVersion
# Should show: 12.x or higher

# Check existing Python
python3 --version
# Should show: Python 3.10 or higher
```

### Step 1: Install Homebrew

```bash
# If not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add to PATH if needed
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zprofile
source ~/.zprofile
```

### Step 2: Install Python 3.10+

```bash
brew install python@3.10

# Create alias
echo 'alias python3=/usr/local/opt/python@3.10/bin/python3' >> ~/.zprofile
source ~/.zprofile

# Verify
python3 --version
```

### Step 3: Install Build Tools

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Or install full Xcode from App Store
```

### Step 4: Install ROS 2 Humble

```bash
# Using Homebrew (recommended)
brew install ros

# Or download macOS binary
# From https://github.com/ros2/ros2/releases
```

### Step 5: Setup Bash Environment

```bash
# For zsh (default on macOS)
echo "source /opt/homebrew/opt/ros/humble/setup.zsh" >> ~/.zprofile

# Or for bash
echo "source /opt/homebrew/opt/ros/humble/setup.bash" >> ~/.bashrc

source ~/.zprofile  # or ~/.bashrc
```

### Step 6: Install Dependencies

```bash
brew install colcon
brew install gazebo

# Python packages
pip3 install numpy scipy matplotlib
```

### Step 7: Create Workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
```

### Step 8: Additional Setup

```bash
# Terminal tools
brew install tmux vim

# VSCode (optional)
brew install visual-studio-code
```

### Verification

```bash
ros2 --version
python3 --version
colcon --help
gazebo --version
```

**Troubleshooting macOS Issues**

| Issue | Solution |
|-------|----------|
| "Python not found" | Use python3 explicitly, check Homebrew install |
| M1/M2 compatibility | Use native ARM builds, not Rosetta 2 |
| ROS 2 not sourcing | Add to .zprofile or .bashrc |
| Permission denied | Use `brew doctor` and check PATH |

**✅ macOS setup complete!**

---

## GPU Setup (Optional)

### NVIDIA GPU Requirements

For Module 3 (Isaac Sim) and Module 4 (AI training):

**Supported GPUs:**
- **Minimum**: GTX 1060 (6GB VRAM)
- **Recommended**: RTX 3060+ (12GB VRAM)
- **Optimal**: RTX 4080/4090 (24GB+ VRAM)

### Step 1: Check GPU

```bash
# Linux
lspci | grep -i nvidia

# Windows (PowerShell)
Get-WmiObject Win32_VideoController

# macOS (Check if GPU available)
system_profiler SPDisplaysDataType
```

### Step 2: Install NVIDIA Drivers

**Linux (Ubuntu)**

```bash
sudo ubuntu-drivers autoinstall
# or
sudo apt install nvidia-driver-525

# Verify
nvidia-smi
```

**Windows**

1. Download from [nvidia.com](https://www.nvidia.com/Download/index.aspx)
2. Run installer
3. Verify in Device Manager or: `nvidia-smi` (if CUDA installed)

**macOS**

- GPU acceleration via CUDA is limited on macOS
- Consider Docker with GPU support
- Or use local Python training with CPU

### Step 3: Install CUDA Toolkit

**Linux**

```bash
# Ubuntu 22.04
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.0.0/local_installers/cuda-repo-ubuntu2204-12-0-local_12.0.0-525.60.13-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2204-12-0-local_12.0.0-525.60.13-1_amd64.deb
sudo apt-get update
sudo apt-get -y install cuda
```

**Windows**

1. Download from [developer.nvidia.com/cuda](https://developer.nvidia.com/cuda-downloads)
2. Run installer
3. Add to PATH

**macOS**

- CUDA support limited, consider Docker alternative

### Step 4: Install cuDNN

```bash
# Download from NVIDIA Developer Program (requires free registration)
# https://developer.nvidia.com/cudnn

# Linux
tar -xvf cudnn-*.tgz
sudo cp cuda/include/cudnn*.h /usr/local/cuda/include
sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn*.h
sudo chmod a+r /usr/local/cuda/lib64/libcudnn*
```

### Step 5: Verify GPU Access

```bash
# Test CUDA
nvcc --version
nvidia-smi

# Test with PyTorch
python3 -c "import torch; print(torch.cuda.is_available())"
# Should print: True
```

---

## Virtual Environment Setup

Recommended for keeping dependencies isolated:

```bash
# Create virtual environment
python3 -m venv ~/textbook_env

# Activate
# Linux/macOS:
source ~/textbook_env/bin/activate
# Windows (PowerShell):
~/textbook_env/Scripts/Activate.ps1

# Install packages
pip install numpy scipy matplotlib

# Deactivate when done
deactivate
```

---

## Docker Alternative

For complete isolation and consistency:

```bash
# Pull ROS 2 Docker image
docker pull osrf/ros:humble-desktop

# Run container
docker run -it osrf/ros:humble-desktop
```

---

## Troubleshooting Installation

### Problem: "Command not found"

**Check if installed:**
```bash
which ros2  # or "where" on Windows
which python3
```

**Solution:** Add to PATH or reinstall

### Problem: "Module/package not found"

```bash
# Check if installed
python3 -m pip list | grep package-name

# Install if missing
pip install package-name
```

### Problem: Permission denied

```bash
# Don't use sudo for pip (except system packages)
pip install --user package-name

# For system packages
sudo apt install package-name  # Linux
```

### Problem: Version conflicts

```bash
# Use virtual environment
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

---

## Next Steps

1. ✅ **Verify installation**: Run all verification commands
2. ✅ **Create workspace**: Set up directory structure
3. ✅ **Clone examples**: `git clone https://github.com/physical-ai-lab/textbook-examples`
4. ✅ **Start learning**: Go to Module 1, Chapter 1.1

---

## Getting Help

If you encounter issues:

1. **Check**: Review this guide for your OS
2. **Search**: Look in [GitHub discussions](https://github.com/physical-ai-lab/textbook/discussions)
3. **Ask**: Post a new discussion with:
   - Your OS and version
   - Python version (`python --version`)
   - Error message (complete output)
   - Steps to reproduce

**Ready?** → [Go to Prerequisites & System Requirements](./prerequisites.md) or [Start Module 1](../module-1/chapter-1-1.md)
