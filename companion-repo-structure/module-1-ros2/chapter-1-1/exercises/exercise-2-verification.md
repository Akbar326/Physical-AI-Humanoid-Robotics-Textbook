# Exercise 1.2: Verify ROS 2 Installation

## Objective
Verify that ROS 2 Humble Hawksbill is properly installed and operational on your system.

## Prerequisites
- ROS 2 Humble Hawksbill installed
- Terminal/Command prompt access

## Steps

### Step 1: Check ROS 2 Version
1. Open a terminal/command prompt
2. Run the following command:
   ```bash
   ros2 --version
   ```

### Step 2: Verify Environment Variables
1. Check if ROS environment variables are set:
   ```bash
   echo $ROS_DISTRO
   ```

### Step 3: Test Basic Commands
1. List available ROS 2 commands:
   ```bash
   ros2
   ```

2. Check available packages:
   ```bash
   ros2 pkg list
   ```

### Step 4: Create a Test Workspace (Optional)
1. Create a workspace directory:
   ```bash
   mkdir -p ~/ros2_test_ws/src
   cd ~/ros2_test_ws
   ```

2. Build the workspace:
   ```bash
   colcon build
   ```

## Expected Output

### Step 1 Expected Output:
```
ros2 humble
```

### Step 2 Expected Output:
```
humble
```

### Step 3 Expected Output:
Should show a list of available ros2 commands like `run`, `launch`, `pkg`, etc.

## Troubleshooting
- If `ros2 --version` returns "command not found", ensure you've sourced the setup script
- If environment variables are not set, add sourcing commands to your shell profile

## Next Steps
Once verification is complete, you're ready to proceed with Chapter 1.2: Creating Your First ROS 2 Node.