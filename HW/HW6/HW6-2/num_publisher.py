import rclpy
from rclpy.node import Node
from my_msg_srv.msg import Num

class NumPublisher(Node):
    def __init__(self):
        super().__init__('num_publisher')
        self.pub = self.create_publisher(Num, 'num_topic', 10)
        self.i = 0
        self.create_timer(0.5, self.tick)

    def tick(self):
        msg = Num()
        msg.num = self.i
        self.pub.publish(msg)
        self.get_logger().info(f'Publish: {msg.num}')
        self.i += 1

def main():
    rclpy.init()
    node = NumPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
