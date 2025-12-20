# Exercise 1.1: Install ROS 2 Humble Hawksbill

## Objective
Install ROS 2 Humble Hawksbill on your operating system following the official installation guide.

## Prerequisites
- Ubuntu 22.04, Windows 10/11, or macOS 12+
- Internet connection
- Administrative privileges on your system

## Steps

### Step 1: System Preparation
1. Update your system packages (Ubuntu):
   ```bash
   sudo apt update && sudo apt upgrade
   ```

2. For Windows, ensure you have WSL2 installed if using Linux distributions

### Step 2: Install ROS 2
1. Follow the official installation guide for your OS:
   - [Ubuntu Installation](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)
   - [Windows Installation](https://docs.ros.org/en/humble/Installation/Windows-Install-Binary.html)
   - [macOS Installation](https://docs.ros.org/en/humble/Installation/macOS-Install-Binary.html)

### Step 3: Environment Setup
1. Source the ROS 2 setup script:
   ```bash
   source /opt/ros/humble/setup.bash
   ```

2. Verify installation:
   ```bash
   ros2 --version
   ```

## Expected Output
You should see output similar to:
```
ros2 humble
```

## Verification
Run the installation validator script:
```bash
python3 install_ros2.py
```

## Troubleshooting
If you encounter issues, refer to the troubleshooting guide in the code directory or check the official ROS 2 documentation.