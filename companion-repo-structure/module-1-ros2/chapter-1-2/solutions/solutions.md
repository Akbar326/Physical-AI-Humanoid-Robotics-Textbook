# Chapter 1.2 Solutions

## Exercise 2.1: Create a Publisher Node

### Solution Code
The publisher node should look like:
```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MyPublisher(Node):
    def __init__(self):
        super().__init__('my_publisher')
        self.publisher_ = self.create_publisher(String, 'my_topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello from publisher: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    my_publisher = MyPublisher()
    rclpy.spin(my_publisher)
    my_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Common Mistakes
1. **Forgetting the shebang**: Always start with `#!/usr/bin/env python3`
2. **Incorrect message type**: Use `std_msgs.msg.String` not a custom type
3. **Missing init call**: Don't forget `rclpy.init(args=args)`
4. **Not making executable**: Run `chmod +x script.py`

### Expected Behavior
- Node publishes messages every 0.5 seconds
- Messages increment with each publication
- Node appears in `ros2 node list`

## Exercise 2.2: Create a Subscriber Node

### Solution Code
The subscriber node should look like:
```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MySubscriber(Node):
    def __init__(self):
        super().__init__('my_subscriber')
        self.subscription = self.create_subscription(
            String,
            'my_topic',  # Same topic as publisher
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'Subscriber heard: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    my_subscriber = MySubscriber()
    rclpy.spin(my_subscriber)
    my_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Common Mistakes
1. **Topic mismatch**: Publisher and subscriber must use the same topic name
2. **Wrong message type**: Both nodes must use the same message type
3. **Forgetting to prevent warning**: Add `self.subscription` comment
4. **Not sourcing workspace**: Remember to `source install/setup.bash`

### Verification Steps
1. Run publisher in one terminal: `ros2 run my_publisher_package my_publisher`
2. Run subscriber in another: `ros2 run my_publisher_package my_subscriber`
3. Confirm subscriber receives publisher's messages
4. Use `ros2 topic echo /my_topic std_msgs/msg/String` to verify

## Advanced Exercise Solution
For the relay node, create a class that inherits from both publisher and subscriber functionality:
```python
class RelayNode(Node):
    def __init__(self):
        super().__init__('relay_node')
        self.subscriber = self.create_subscription(...)
        self.publisher = self.create_publisher(...)

    def listener_callback(self, msg):
        # Process and republish the message
        self.publisher.publish(modified_msg)
```

## Debugging Tips
- Use `ros2 node list` to see running nodes
- Use `ros2 topic list` to see available topics
- Use `ros2 topic info /topic_name` to see publishers/subscribers
- Check that both nodes are on the same ROS domain

## Next Chapter Preparation
After completing these exercises, you should understand:
- How to create publisher and subscriber nodes
- How to configure ROS 2 packages
- How to build and run custom nodes
- How to verify node communication