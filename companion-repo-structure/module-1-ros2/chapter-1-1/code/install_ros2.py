#!/usr/bin/env python3
"""
Automated installation validator for ROS 2 Humble
"""
import subprocess
import sys
import platform

def check_ros2_installation():
    """Check if ROS 2 is properly installed"""
    try:
        result = subprocess.run(['ros2', '--version'],
                              capture_output=True, text=True, check=True)
        print(f"ROS 2 installation found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ROS 2 not found in PATH. Please install ROS 2 Humble Hawksbill.")
        return False

def main():
    print("ROS 2 Installation Validator")
    print("=" * 30)

    if check_ros2_installation():
        print("✓ ROS 2 installation is valid")
        sys.exit(0)
    else:
        print("✗ ROS 2 installation not found")
        sys.exit(1)

if __name__ == "__main__":
    main()