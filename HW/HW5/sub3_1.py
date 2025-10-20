import rclpy
from rclpy.node import Node
from rclpy.logging import LoggingSeverity
from std_msgs.msg import UInt8
import serial, time

PORT = '/dev/ttyACM0'   
BAUD = 9600            

class LedSerialBridge(Node):
    def __init__(self):
        super().__init__('led_serial_bridge')
        self.get_logger().set_level(LoggingSeverity.INFO)
        self.sub = self.create_subscription(UInt8, 'led_index', self.on_index, 10)

        self.ser = None
        try:
            self.ser = serial.Serial(PORT, BAUD, timeout=0.2)
            time.sleep(2.0) 
            self.get_logger().info(f'Connected serial: {PORT} @ {BAUD}')
        except Exception as e:
            self.get_logger().error(f'Serial open failed: {e}')

    def on_index(self, msg: UInt8):
        if not self.ser:
            self.get_logger().warning('Serial not available'); return
        idx = int(msg.data) % 3
        payload = f'{idx}\n'.encode('ascii')  
        try:
            self.ser.write(payload); self.ser.flush()
            self.get_logger().info(f'sent to Arduino: {payload!r}')
        except Exception as e:
            self.get_logger().warning(f'Serial write error: {e}')

    def destroy_node(self):
        try:
            if self.ser: self.ser.close()
        finally:
            return super().destroy_node()

def main():
    rclpy.init()
    node = LedSerialBridge()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node(); rclpy.shutdown()

if __name__ == '__main__':
    main()
