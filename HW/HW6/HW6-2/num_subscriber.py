import rclpy
from rclpy.node import Node
from my_msg_srv.msg import Num

class NumSubscriber(Node):
    def __init__(self):
        super().__init__('num_subscriber')
        self.sub = self.create_subscription(Num, 'num_topic', self.cb, 10)

    def cb(self, msg: Num):
        self.get_logger().info(f'Recv: {msg.num}')

def main():
    rclpy.init()
    node = NumSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
