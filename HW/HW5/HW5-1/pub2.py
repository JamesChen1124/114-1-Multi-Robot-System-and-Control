import rclpy
from rclpy.node import Node
from rclpy.logging import LoggingSeverity
from sensor_msgs.msg import Temperature
import serial, time

PORT = '/dev/ttyACM0'     
BAUD = 9600
PERIOD_SEC = 5.0         

class TemperaturePublisher(Node):
    def __init__(self):
        super().__init__('temperature_publisher')
        self.get_logger().set_level(LoggingSeverity.INFO)
        self.pub = self.create_publisher(Temperature, 'room_temperature', 10)

        self.ser = None
        try:
            self.ser = serial.Serial(PORT, BAUD, timeout=0.3)
            time.sleep(2.0)  
            self.get_logger().info(f'Connected: {PORT} @ {BAUD}')
        except Exception as e:
            self.get_logger().error(f'Serial open failed: {e}')

        self.timer = self.create_timer(PERIOD_SEC, self.timer_cb)

    def timer_cb(self):
        if not self.ser:
            self.get_logger().warning('Serial not available')
            return

        last = None
        try:
            for _ in range(30): 
                line = self.ser.readline().decode('utf-8', 'ignore').strip()
                if not line:
                    break
                last = line
        except Exception as e:
            self.get_logger().warning(f'Serial read error: {e}')
            return

        if last is None:
            self.get_logger().info('No data from serial')
            return
        if last == 'Error':
            self.get_logger().warning('Arduino reported Error')
            return

        token = ''.join(ch for ch in last if (ch.isdigit() or ch in '.-'))
        if token in ('', '-', '.'):
            self.get_logger().info(f'Garbage line: {last!r}')
            return

        try:
            t_c = float(token)
        except ValueError:
            self.get_logger().info(f'Not a number: {last!r}')
            return

        msg = Temperature()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'dht11_arduino'
        msg.temperature = t_c
        msg.variance = 0.5  
        self.pub.publish(msg)
        self.get_logger().info(f'T = {t_c:.2f} °C')

def main():
    rclpy.init()
    node = TemperaturePublisher()
    try:
        rclpy.spin(node)
    finally:
        if node.ser:
            node.ser.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
