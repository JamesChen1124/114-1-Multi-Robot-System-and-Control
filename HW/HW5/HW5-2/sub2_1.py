# hw51/hw51/multi_sub.py
import rclpy
from rclpy.node import Node
from rclpy.logging import LoggingSeverity
from std_msgs.msg import UInt8
from sensor_msgs.msg import Temperature

class MultiSubscriber(Node):
    def __init__(self):
        super().__init__('multi_subscriber')
        self.get_logger().set_level(LoggingSeverity.INFO)
        self.sub_rand = self.create_subscription(UInt8, 'random_byte', self.rand_cb, 10)
        self.sub_temp = self.create_subscription(Temperature, 'room_temperature', self.temp_cb, 10)
        self.get_logger().info('listening: /random_byte, /room_temperature')

    def rand_cb(self, msg: UInt8):
        self.get_logger().info(f'random_byte = {msg.data}')

    def temp_cb(self, msg: Temperature):
        self.get_logger().info(f'[{msg.header.frame_id}] T = {msg.temperature:.2f} °C (var={msg.variance:.2f})')

def main():
    rclpy.init()
    node = MultiSubscriber()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
