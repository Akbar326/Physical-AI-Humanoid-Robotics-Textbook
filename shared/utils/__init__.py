"""
Shared utilities for Physical AI & Humanoid Robotics textbook.

This package provides reusable utilities for ROS 2, Gazebo, visualization,
and configuration management across all chapters and projects.
"""

__version__ = "1.0.0"
__author__ = "Physical AI Lab"

from .ros2_helpers import ROS2Helper
from .gazebo_utils import GazeboHelper
from .visualization import Visualizer
from .config_loader import ConfigLoader

__all__ = [
    "ROS2Helper",
    "GazeboHelper",
    "Visualizer",
    "ConfigLoader",
]
