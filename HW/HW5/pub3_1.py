import rclpy
from rclpy.node import Node
from rclpy.logging import LoggingSeverity
from std_msgs.msg import UInt8

class LedCyclePublisher(Node):
    def __init__(self):
        super().__init__('led_cycle_publisher')
        self.get_logger().set_level(LoggingSeverity.INFO)
        self.pub = self.create_publisher(UInt8, 'led_index', 10)
        self.i = 0
        self.timer = self.create_timer(1.0, self.tick)  # 每秒送一次

    def tick(self):
        msg = UInt8()
        msg.data = self.i % 3          # 0,1,2,0,1,2...
        self.pub.publish(msg)
        self.get_logger().info(f'publish led_index = {msg.data}')
        self.i += 1

def main():
    rclpy.init()
    node = LedCyclePublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node(); rclpy.shutdown()

if __name__ == '__main__':
    main()
