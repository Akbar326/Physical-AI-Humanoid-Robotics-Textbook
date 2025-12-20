# ROS 2 Installation Troubleshooting

This guide covers common issues when installing ROS 2 Humble Hawksbill on different platforms.

## Ubuntu Installation Issues

### Problem: Package dependencies not satisfied
**Solution**: Ensure your system is updated:
```bash
sudo apt update && sudo apt upgrade
```

### Problem: Locale errors
**Solution**: Set proper locale:
```bash
export LANG=C.UTF-8
export LC_ALL=C.UTF-8
```

## Windows Installation Issues

### Problem: Python not found
**Solution**: Ensure Python 3.8+ is installed and added to PATH

### Problem: Permission errors
**Solution**: Run PowerShell as Administrator when installing

## macOS Installation Issues

### Problem: Homebrew dependencies
**Solution**: Update Homebrew and dependencies:
```bash
brew update && brew upgrade
```

## Common Issues

### Problem: rosdep initialization failure
**Solution**: Initialize rosdep manually:
```bash
sudo rosdep init
rosdep update
```

### Problem: Environment not sourced
**Solution**: Source the setup script:
```bash
source /opt/ros/humble/setup.bash
```

For additional help, see the [official ROS 2 troubleshooting guide](https://docs.ros.org/).