# Chapter 1.1 Solutions

## Exercise 1.1: Install ROS 2 Humble Hawksbill

### Solution and Expected Behavior
- ROS 2 Humble Hawksbill should be successfully installed on your system
- The `ros2 --version` command should return the version information
- All required dependencies should be properly resolved

### Common Mistakes
1. **Not updating system packages first**: Always run system updates before installing ROS 2
2. **Incorrect repository setup**: Ensure you're using the correct ROS 2 repository for your OS
3. **Not sourcing the setup script**: Remember to source the ROS 2 environment in each new terminal

### Additional Tips
- For Ubuntu users: Use the Debian installation method rather than building from source for beginners
- For Windows users: WSL2 provides the most stable ROS 2 experience
- For macOS users: Binary installation is available but Linux is recommended for development

## Exercise 1.2: Verify ROS 2 Installation

### Solution and Expected Behavior
- `ros2 --version` should return "ros2 humble"
- `echo $ROS_DISTRO` should return "humble"
- The `ros2` command should show available subcommands

### Troubleshooting Common Issues
1. **Environment not sourced**: Add `source /opt/ros/humble/setup.bash` to your `~/.bashrc` or `~/.zshrc`
2. **Command not found**: Check that ROS 2 packages were installed correctly
3. **Missing dependencies**: Install missing packages using your system's package manager

### Verification Checklist
- [ ] `ros2 --version` returns correct version
- [ ] Environment variables are properly set
- [ ] Basic ROS 2 commands are available
- [ ] Installation validator script passes

## Advanced Exercises (Optional)

### Exercise: Install Additional Packages
Install the turtlesim package for later exercises:
```bash
sudo apt install ros-humble-turtlesim  # Ubuntu
```

### Exercise: Create First Workspace
Create a basic workspace structure:
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
source install/setup.bash
```

## Next Chapter Preparation
After completing these exercises, you should be ready to proceed with Chapter 1.2: Creating Your First ROS 2 Node.