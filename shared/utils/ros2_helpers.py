"""
ROS 2 Utilities Module

Provides common utilities for ROS 2 development including node creation,
topic/service management, parameter handling, and debugging functions.
"""

import logging
import time
from typing import Any, List, Optional, Type, Callable

logger = logging.getLogger(__name__)


class ROS2Helper:
    """
    Utilities for ROS 2 development.

    Provides convenient methods for common ROS 2 operations including
    node setup, topic management, service handling, and parameters.

    Example:
        >>> from shared.utils import ROS2Helper
        >>> helper = ROS2Helper()
        >>> available_topics = helper.list_topics()
        >>> print(f"Found {len(available_topics)} topics")
    """

    @staticmethod
    def setup_node(
        node_name: str,
        namespace: str = "",
        domain_id: Optional[int] = None
    ) -> Any:
        """
        Initialize a ROS 2 node with common setup.

        Args:
            node_name: Name for the node
            namespace: Namespace for the node (optional)
            domain_id: ROS 2 domain ID (optional)

        Returns:
            ROS 2 node object

        Raises:
            ImportError: If rclpy is not installed
            RuntimeError: If node creation fails

        Example:
            >>> node = ROS2Helper.setup_node("my_node")
            >>> print(f"Node created: {node.get_name()}")
        """
        try:
            import rclpy
            from rclpy.node import Node
        except ImportError:
            logger.error("rclpy not installed. Install ROS 2 first.")
            raise ImportError("ROS 2 (rclpy) is required")

        try:
            if not rclpy.ok():
                rclpy.init()

            if namespace:
                node = Node(node_name, namespace=namespace)
            else:
                node = Node(node_name)

            logger.info(f"Node '{node.get_name()}' created successfully")
            return node
        except Exception as e:
            logger.error(f"Failed to create node: {e}")
            raise RuntimeError(f"Node creation failed: {e}")

    @staticmethod
    def list_topics() -> List[tuple]:
        """
        List all available ROS 2 topics.

        Returns:
            List of tuples (topic_name, message_types)

        Raises:
            ImportError: If rclpy is not installed

        Example:
            >>> topics = ROS2Helper.list_topics()
            >>> for topic_name, msg_types in topics:
            ...     print(f"{topic_name}: {msg_types}")
        """
        try:
            import rclpy
            from rclpy.node import Node
        except ImportError:
            raise ImportError("ROS 2 (rclpy) is required")

        try:
            if not rclpy.ok():
                rclpy.init()

            node = Node("temp_topic_lister")
            topic_names_and_types = node.get_topic_names_and_types()
            node.destroy_node()

            logger.debug(f"Found {len(topic_names_and_types)} topics")
            return topic_names_and_types
        except Exception as e:
            logger.error(f"Failed to list topics: {e}")
            return []

    @staticmethod
    def list_services() -> List[str]:
        """
        List all available ROS 2 services.

        Returns:
            List of service names

        Raises:
            ImportError: If rclpy is not installed

        Example:
            >>> services = ROS2Helper.list_services()
            >>> print(f"Available services: {services}")
        """
        try:
            import rclpy
            from rclpy.node import Node
        except ImportError:
            raise ImportError("ROS 2 (rclpy) is required")

        try:
            if not rclpy.ok():
                rclpy.init()

            node = Node("temp_service_lister")
            service_names_and_types = node.get_service_names_and_types()
            node.destroy_node()

            services = [name for name, _ in service_names_and_types]
            logger.debug(f"Found {len(services)} services")
            return services
        except Exception as e:
            logger.error(f"Failed to list services: {e}")
            return []

    @staticmethod
    def get_parameter(
        node: Any,
        param_name: str,
        default: Any = None
    ) -> Any:
        """
        Safely get a ROS 2 parameter with default fallback.

        Args:
            node: ROS 2 node object
            param_name: Name of the parameter
            default: Default value if parameter not found

        Returns:
            Parameter value or default

        Example:
            >>> value = ROS2Helper.get_parameter(node, "max_speed", 1.0)
            >>> print(f"Max speed: {value}")
        """
        try:
            param_value = node.get_parameter(param_name)
            logger.debug(f"Retrieved parameter '{param_name}': {param_value}")
            return param_value.value
        except Exception as e:
            logger.warning(f"Parameter '{param_name}' not found: {e}")
            return default

    @staticmethod
    def set_parameter(node: Any, param_name: str, value: Any) -> bool:
        """
        Set a ROS 2 parameter.

        Args:
            node: ROS 2 node object
            param_name: Name of the parameter
            value: Value to set

        Returns:
            True if successful, False otherwise

        Example:
            >>> success = ROS2Helper.set_parameter(node, "max_speed", 2.5)
            >>> print(f"Parameter set: {success}")
        """
        try:
            from rclpy.parameter import Parameter

            param = Parameter(param_name, Parameter.Type.DOUBLE if isinstance(value, float) else Parameter.Type.INTEGER, value)
            node.set_parameters([param])
            logger.info(f"Parameter '{param_name}' set to {value}")
            return True
        except Exception as e:
            logger.error(f"Failed to set parameter '{param_name}': {e}")
            return False

    @staticmethod
    def create_publisher(
        node: Any,
        topic_name: str,
        msg_type: Type,
        queue_size: int = 10
    ) -> Any:
        """
        Create a ROS 2 publisher with error handling.

        Args:
            node: ROS 2 node object
            topic_name: Name of the topic to publish to
            msg_type: Message type class
            queue_size: Publisher queue size

        Returns:
            Publisher object

        Raises:
            RuntimeError: If publisher creation fails

        Example:
            >>> from geometry_msgs.msg import Point
            >>> pub = ROS2Helper.create_publisher(
            ...     node, "/robot/position", Point)
            >>> print(f"Publisher created for {topic_name}")
        """
        try:
            publisher = node.create_publisher(msg_type, topic_name, queue_size)
            logger.info(f"Publisher created for topic '{topic_name}'")
            return publisher
        except Exception as e:
            logger.error(f"Failed to create publisher: {e}")
            raise RuntimeError(f"Publisher creation failed: {e}")

    @staticmethod
    def create_subscriber(
        node: Any,
        topic_name: str,
        msg_type: Type,
        callback: Callable,
        queue_size: int = 10
    ) -> Any:
        """
        Create a ROS 2 subscriber with error handling.

        Args:
            node: ROS 2 node object
            topic_name: Name of the topic to subscribe to
            msg_type: Message type class
            callback: Callback function for received messages
            queue_size: Subscriber queue size

        Returns:
            Subscription object

        Raises:
            RuntimeError: If subscriber creation fails

        Example:
            >>> def callback(msg):
            ...     print(f"Received: {msg.data}")
            >>> sub = ROS2Helper.create_subscriber(
            ...     node, "/topic", String, callback)
        """
        try:
            subscription = node.create_subscription(
                msg_type,
                topic_name,
                callback,
                queue_size
            )
            logger.info(f"Subscriber created for topic '{topic_name}'")
            return subscription
        except Exception as e:
            logger.error(f"Failed to create subscriber: {e}")
            raise RuntimeError(f"Subscriber creation failed: {e}")

    @staticmethod
    def wait_for_service(
        node: Any,
        service_name: str,
        timeout_sec: float = 5.0
    ) -> bool:
        """
        Wait for a ROS 2 service to become available.

        Args:
            node: ROS 2 node object
            service_name: Name of the service
            timeout_sec: Timeout in seconds

        Returns:
            True if service available, False if timeout

        Example:
            >>> if ROS2Helper.wait_for_service(node, "/move_robot"):
            ...     print("Service is available!")
        """
        try:
            from rclpy.client import Client

            client = node.create_client(type(None), service_name)
            start_time = time.time()

            while not client.wait_for_service(timeout_sec=0.1):
                if time.time() - start_time > timeout_sec:
                    logger.warning(f"Service '{service_name}' not available (timeout)")
                    return False

            logger.info(f"Service '{service_name}' is available")
            node.destroy_client(client)
            return True
        except Exception as e:
            logger.error(f"Error waiting for service: {e}")
            return False


# For backward compatibility
PublisherHelper = ROS2Helper
SubscriberHelper = ROS2Helper
