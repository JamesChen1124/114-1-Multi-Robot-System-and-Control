# hw51/hw51/multi_pub.py
import random, time, serial
import rclpy
from rclpy.node import Node
from rclpy.logging import LoggingSeverity
from std_msgs.msg import UInt8
from sensor_msgs.msg import Temperature

PORT = '/dev/ttyACM0'  
BAUD = 9600

class MultiPublisher(Node):
    def __init__(self):
        super().__init__('multi_publisher')
        self.get_logger().set_level(LoggingSeverity.INFO)

        # Pub1: 隨機數
        self.rand_pub = self.create_publisher(UInt8, 'random_byte', 10)
        self.rand_timer = self.create_timer(0.2, self.rand_cb)  # 5 Hz

        # Pub2: 溫度
        self.temp_pub = self.create_publisher(Temperature, 'room_temperature', 10)
        self.temp_timer = self.create_timer(5.0, self.temp_cb)  # 每 5 秒

        # 串列連線
        self.ser = None
        try:
            self.ser = serial.Serial(PORT, BAUD, timeout=0.3)
            time.sleep(2.0) 
            self.get_logger().info(f'Connected serial: {PORT} @ {BAUD}')
        except Exception as e:
            self.get_logger().error(f'Serial open failed: {e}')

        self.get_logger().info('multi_publisher up: /random_byte@5Hz, /room_temperature@5s')

    def rand_cb(self):
        msg = UInt8()
        msg.data = random.randint(0, 255)
        self.rand_pub.publish(msg)
        self.get_logger().info(f'random = {msg.data}')

    def temp_cb(self):
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
        self.temp_pub.publish(msg)
        self.get_logger().info(f'T = {t_c:.2f} °C')

def main():
    rclpy.init()
    node = MultiPublisher()
    try:
        rclpy.spin(node)
    finally:
        if node.ser:
            node.ser.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
