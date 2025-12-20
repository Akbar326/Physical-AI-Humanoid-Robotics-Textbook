# Installation Scripts

This directory contains automated installation scripts for setting up the Physical AI & Humanoid Robotics textbook environment on different operating systems.

## Overview

Each script automates the complete setup process for your operating system:

- **Ubuntu 22.04**: `ubuntu-setup.sh` - Complete ROS 2 Humble + Gazebo installation
- **Windows 10/11**: `windows-setup.ps1` - Python 3.10 + ROS 2 Humble setup
- **macOS 12+**: `macos-setup.sh` - Homebrew-based Python + ROS 2 installation

All scripts include:
- ✅ Comprehensive error handling and validation
- ✅ Detailed progress output with color-coded messages
- ✅ System compatibility checks
- ✅ Environment variable configuration
- ✅ Installation verification
- ✅ Workspace creation
- ✅ Clear next-step instructions

## Quick Start

### Ubuntu 22.04

```bash
# Download and run the script
bash ubuntu-setup.sh

# Or if cloned from GitHub
git clone <repository-url>
cd shared/install-scripts
bash ubuntu-setup.sh
```

**What it installs:**
- Python 3.10 and development tools
- Build essentials (cmake, git, etc.)
- ROS 2 Humble with development tools
- Gazebo Fortress simulator
- Python scientific packages (numpy, scipy, matplotlib)
- ROS 2 workspace at `~/ros2_ws`

**System Requirements:**
- Ubuntu 22.04 LTS (other versions may work but are not officially supported)
- 4GB RAM minimum (8GB recommended)
- 10GB free disk space
- Internet connection
- Sudo access

**Time Required:** 20-30 minutes

---

### Windows 10/11

```powershell
# Run as Administrator
powershell.exe -ExecutionPolicy Bypass -File windows-setup.ps1

# Or if cloned from GitHub
git clone <repository-url>
cd shared\install-scripts
powershell.exe -ExecutionPolicy Bypass -File windows-setup.ps1
```

**Optional Parameters:**

```powershell
# Skip Python installation if already installed
powershell.exe -ExecutionPolicy Bypass -File windows-setup.ps1 -SkipPython

# Skip Build Tools if not needed
powershell.exe -ExecutionPolicy Bypass -File windows-setup.ps1 -SkipBuildTools

# Skip ROS 2 installation
powershell.exe -ExecutionPolicy Bypass -File windows-setup.ps1 -SkipROS2
```

**What it installs:**
- Python 3.10 (if not present)
- Git for version control
- Visual Studio Build Tools
- ROS 2 Humble binaries
- Python scientific packages
- ROS 2 workspace at `~\ros2_ws`

**System Requirements:**
- Windows 10 (Build 19041+) or Windows 11
- 4GB RAM minimum (8GB recommended)
- 15GB free disk space
- Internet connection
- Administrator access
- One of: Visual Studio Build Tools, Visual Studio Community, or Visual Studio Professional

**Time Required:** 25-40 minutes

**Notes:**
- Script requires Administrator privileges to install system-wide tools
- Python 3.10 is downloaded from official python.org
- Some operations may require restarting PowerShell or your terminal to take effect

---

### macOS 12 (Monterey) or later

```bash
# Download and run the script
bash macos-setup.sh

# Or if cloned from GitHub
git clone <repository-url>
cd shared/install-scripts
bash macos-setup.sh
```

**What it installs:**
- Xcode Command Line Tools (if not present)
- Homebrew package manager
- Python 3.10
- Build tools (cmake, git, pkg-config, graphviz)
- ROS 2 Humble (via Homebrew or from source)
- Gazebo simulator
- Python scientific packages
- ROS 2 workspace at `~/ros2_ws`

**System Requirements:**
- macOS 12 (Monterey) or later
- 4GB RAM minimum (8GB recommended for building from source)
- 15GB free disk space
- Internet connection
- ~5GB additional space if building ROS 2 from source

**Processor Support:**
- Intel Macs: Fully supported
- Apple Silicon (M1/M2/M3): Supported with native Homebrew

**Time Required:**
- 15-20 minutes with Homebrew packages
- 30-50 minutes if building ROS 2 from source

---

## After Installation

### 1. Activate your environment

**Ubuntu/macOS:**
```bash
source ~/.bashrc     # Ubuntu
# or
source ~/.zprofile   # macOS
```

**Windows:**
Restart PowerShell or your terminal application.

### 2. Verify the installation

```bash
# Test Python
python3 --version

# Test ROS 2
ros2 --version
```

### 3. Create a test workspace

```bash
# Ubuntu/macOS
mkdir -p ~/ros2_test/src
cd ~/ros2_test
colcon build

# Windows
mkdir %USERPROFILE%\ros2_test\src
cd %USERPROFILE%\ros2_test
colcon build
```

### 4. Read the complete setup guide

See `docs/preface/setup-guide.md` for:
- Detailed OS-specific setup instructions
- GPU configuration (NVIDIA CUDA/cuDNN)
- Docker alternatives
- Troubleshooting common issues
- Advanced configuration options

### 5. Start the textbook

```bash
# Navigate to textbook directory
cd ~/ai-humanoid-robotics

# Read the getting started guide
cat docs/preface/about.md

# Begin with Module 1, Chapter 1.1
```

---

## Troubleshooting

### Ubuntu

**Problem: "E: Unable to locate package ros-humble-desktop"**
- Solution: Verify the ROS 2 GPG key was added correctly. Run: `apt-key fingerprint 3B4FE6ACC0B21F32`

**Problem: "ROS 2 command not found after installation"**
- Solution: Reload your shell with: `source ~/.bashrc`
- If persistent, check: `ls /opt/ros/humble/setup.bash`

**Problem: "Permission denied" when running script**
- Solution: Make script executable: `chmod +x ubuntu-setup.sh`

---

### Windows

**Problem: "Running scripts is disabled on this system"**
- Solution: Run PowerShell as Administrator and execute:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

**Problem: "Python not found after installation"**
- Solution: Restart PowerShell completely (close and reopen)
- Verify: `python --version`

**Problem: "Visual Studio Build Tools installation hangs"**
- Solution: Cancel and install manually from https://visualstudio.microsoft.com/
- Script can continue without automatic installation

**Problem: "ROS 2 download fails"**
- Solution: Check internet connection
- Manual installation: https://docs.ros.org/en/humble/Installation/Windows-Install-Binary.html

---

### macOS

**Problem: "xcode-select: error: unable to get active developer directory"**
- Solution: Install Xcode Command Line Tools manually:
  ```bash
  xcode-select --install
  ```

**Problem: "Homebrew command not found"**
- Solution: On Apple Silicon, add to PATH:
  ```bash
  eval "$(/opt/homebrew/bin/brew shellenv)"
  ```

**Problem: "ROS 2 build takes very long"**
- This is normal when building from source (30-50 minutes)
- Ensure you have at least 15GB free disk space
- Do not interrupt the build process

**Problem: "M1/M2 Mac compatibility issues"**
- Script includes native arm64 architecture support
- Some packages may need to be built from source
- Apple Silicon support is improving with each ROS 2 release

---

## Manual Installation

If the automated scripts don't work for your system, see detailed manual installation steps in:
- **Ubuntu**: `docs/preface/setup-guide.md#ubuntu-2204`
- **Windows**: `docs/preface/setup-guide.md#windows-1011`
- **macOS**: `docs/preface/setup-guide.md#macos-12`

---

## Script Features

### Error Handling
- Scripts exit immediately on critical errors
- Non-critical warnings continue installation
- Clear error messages with remediation steps

### Progress Tracking
- Color-coded output (Green=success, Red=error, Yellow=warning, Cyan=info)
- Progress headers for each installation phase
- Verification steps to confirm successful installation

### Customization

**Ubuntu:** Edit variables at top of script
```bash
ROS_DISTRO="humble"
PYTHON_VERSION="3.10"
```

**Windows:** Edit parameters for PowerShell
```powershell
$ROS_DISTRO = "humble"
$PYTHON_VERSION = "3.10"
```

**macOS:** Edit variables at top of script
```bash
ROS_DISTRO="humble"
PYTHON_VERSION="3.10"
```

---

## Uninstallation

To remove installed tools (if needed):

**Ubuntu:**
```bash
sudo apt-get autoremove ros-humble-* python3.10*
```

**Windows:**
- Use Control Panel → Programs → Programs and Features
- Uninstall: Python, ROS 2, Visual Studio components

**macOS:**
```bash
brew uninstall python@3.10 ros2-humble gazebo
```

---

## Contributing

Found an issue with the installation scripts? Please:

1. Check the troubleshooting section above
2. Verify your system meets requirements
3. Review `docs/preface/setup-guide.md` for detailed guidance
4. Open an issue on GitHub with:
   - Your operating system and version
   - Complete error message and output
   - Steps to reproduce

---

## Additional Resources

- **ROS 2 Humble Documentation**: https://docs.ros.org/en/humble/
- **Gazebo Documentation**: https://gazebosim.org/
- **Python 3.10 Downloads**: https://www.python.org/downloads/
- **Homebrew Documentation**: https://brew.sh/

---

## License

These installation scripts are part of the Physical AI & Humanoid Robotics textbook project and are provided as-is for educational purposes.

**Last Updated:** 2025-12-16
**Maintained By:** Physical AI Lab
**Questions?** See `docs/preface/setup-guide.md` or open an issue on GitHub
