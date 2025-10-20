import rclpy
from rclpy.node import Node
from rclpy.logging import LoggingSeverity
from sensor_msgs.msg import Temperature

class TemperatureSubscriber(Node):
    def __init__(self):
        super().__init__('temperature_subscriber')
        self.get_logger().set_level(LoggingSeverity.INFO)
        self.sub = self.create_subscription(Temperature, 'room_temperature', self.cb, 10)
        self.get_logger().info('listening: /room_temperature')

    def cb(self, msg: Temperature):
        self.get_logger().info(f'[{msg.header.frame_id}] T = {msg.temperature:.2f} °C (var={msg.variance:.2f})')

def main():
    rclpy.init()
    node = TemperatureSubscriber()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
