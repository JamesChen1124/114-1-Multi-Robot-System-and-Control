import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8

class RandomSubscriber(Node):
    def __init__(self):
        super().__init__('random_subscriber')
        self.sub = self.create_subscription(UInt8, 'random_byte', self.cb, 10)
        self.get_logger().info('listening: /random_byte')

    def cb(self, msg: UInt8):
        self.get_logger().info(f'random_byte = {msg.data}')

def main():
    rclpy.init()
    node = RandomSubscriber()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
