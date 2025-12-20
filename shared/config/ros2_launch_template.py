"""
Physical AI & Humanoid Robotics - ROS 2 Launch File Template

This is a template for ROS 2 launch files using the Python DSL.
Copy this file and modify for your specific use case.

Usage:
    ros2 launch <package> ros2_launch_template.py

Requirements:
    - ROS 2 Humble
    - launch package
    - launch_ros package
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """
    Generate ROS 2 launch description.

    This template demonstrates:
    - Package discovery
    - Launch arguments
    - Node creation
    - Parameter passing
    - Remapping topics
    """

    # Get package share directory
    pkg_share = FindPackageShare(package='my_robot_package').find('my_robot_package')

    # ========================
    # Declare Launch Arguments
    # ========================

    # Node namespace
    namespace_arg = DeclareLaunchArgument(
        'namespace',
        default_value='robot',
        description='Namespace for robot nodes'
    )

    # Robot model
    robot_model_arg = DeclareLaunchArgument(
        'robot_model',
        default_value='turtlebot3_burger',
        description='Robot model (burger, waffle, waffle_pi)'
    )

    # Simulation vs Real
    use_sim_arg = DeclareLaunchArgument(
        'use_sim',
        default_value='true',
        description='Use simulation (true) or real hardware (false)'
    )

    # Logging level
    log_level_arg = DeclareLaunchArgument(
        'log_level',
        default_value='INFO',
        description='Logging level (DEBUG, INFO, WARN, ERROR)'
    )

    # Config file
    config_file_arg = DeclareLaunchArgument(
        'config_file',
        default_value=PathJoinSubstitution([pkg_share, 'config', 'robot.yaml']),
        description='Path to robot configuration file'
    )

    # ========================
    # Create Nodes
    # ========================

    # Get launch configuration values
    namespace = LaunchConfiguration('namespace')
    robot_model = LaunchConfiguration('robot_model')
    use_sim = LaunchConfiguration('use_sim')
    log_level = LaunchConfiguration('log_level')
    config_file = LaunchConfiguration('config_file')

    # Main Robot Controller Node
    robot_controller_node = Node(
        package='my_robot_package',
        executable='robot_controller',
        namespace=namespace,
        name='controller',
        output='screen',
        arguments=['--ros-args', '--log-level', log_level],
        parameters=[config_file],
        remappings=[
            # Remap topics
            ('/cmd_vel', [namespace, '/cmd_vel']),
            ('/odom', [namespace, '/odom']),
        ],
    )

    # Odometry Node
    odometry_node = Node(
        package='my_robot_package',
        executable='odometry_node',
        namespace=namespace,
        name='odometry',
        output='screen',
        parameters=[config_file],
    )

    # Sensor Driver Node
    sensor_node = Node(
        package='my_robot_package',
        executable='sensor_driver',
        namespace=namespace,
        name='sensor_driver',
        output='screen',
        parameters=[config_file],
        condition=IfCondition(use_sim),  # Only run in simulation
    )

    # TF2 Broadcaster Node
    tf_broadcaster_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['--x', '0', '--y', '0', '--z', '0.1',
                   '--roll', '0', '--pitch', '0', '--yaw', '0',
                   '--frame-id', 'base_link',
                   '--child-frame-id', 'lidar_link'],
    )

    # ========================
    # Log Information
    # ========================

    log_info = LogInfo(
        msg=[
            'Starting robot launch with:',
            ' - Namespace: ', namespace,
            ' - Robot Model: ', robot_model,
            ' - Simulation: ', use_sim,
            ' - Config File: ', config_file,
        ]
    )

    # ========================
    # Create Launch Description
    # ========================

    return LaunchDescription([
        # Arguments
        namespace_arg,
        robot_model_arg,
        use_sim_arg,
        log_level_arg,
        config_file_arg,

        # Actions
        log_info,

        # Nodes
        robot_controller_node,
        odometry_node,
        sensor_node,
        tf_broadcaster_node,
    ])


# ========================
# Advanced Features
# ========================

# The following would be added if needed:

# from launch.conditions import IfCondition
# from launch_ros.launch_context import LaunchContext

# 1. Conditional Node Execution
# condition=IfCondition(use_sim)

# 2. Include Other Launch Files
# from launch.actions import IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource
#
# other_launch = IncludeLaunchDescription(
#     PythonLaunchDescriptionSource([
#         FindPackageShare('other_package'),
#         '/launch/other.launch.py'
#     ])
# )

# 3. Event Handlers
# from launch.event_handlers import OnProcessExit
#
# handler = OnProcessExit(
#     target_action=robot_controller_node,
#     on_exit=[LogInfo(msg='Robot controller exited')]
# )

# 4. Timers
# from launch.actions import TimerAction
#
# timer = TimerAction(period=5.0, actions=[sensor_node])

# 5. Groups
# from launch.actions import GroupAction
#
# group = GroupAction(
#     actions=[node1, node2],
#     scoped=True,  # Scoped actions
# )


# ========================
# Configuration File Example (robot.yaml)
# ========================

"""
# robot.yaml - Example configuration

robot:
  name: "my_robot"
  model: "turtlebot3_burger"

  motion:
    max_linear_velocity: 0.26
    max_angular_velocity: 2.84

  sensors:
    lidar:
      enabled: true
      topic: "/scan"
    camera:
      enabled: true
      topic: "/camera/image_raw"

  control:
    linear_pid:
      kp: 1.0
      ki: 0.1
      kd: 0.5
    angular_pid:
      kp: 2.0
      ki: 0.2
      kd: 0.3

ros2:
  domain_id: 0
  middleware: "rmw_cyclonedds_cpp"
"""
