import time
import serial
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from led_action_interfaces.action import LedControl

class LedActionServer(Node):
    def __init__(self):
        super().__init__('led_action_server')
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            time.sleep(2)
            self.get_logger().info('✅ Connected to Arduino on /dev/ttyACM0')
        except serial.SerialException:
            self.get_logger().error('❌ Failed to connect to Arduino')
            raise SystemExit
        self._action_server = ActionServer(
            self,
            LedControl,
            'led_control',
            self.execute_callback)
    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing LED control goal...')
        feedback_msg = LedControl.Feedback()
        result = LedControl.Result()
        total_leds = goal_handle.request.total_leds

        start_time = time.t
ime()
        current_led = 1
        self.ser.write(b'1\n')
        self.get_logger().info('💡 Lighting LED 1')
        while True:
            elapsed = int(time.time() - start_time)
            if elapsed >= (current_led) * 2 and current_led < total_leds:
                current_led += 1
                cmd = f"{current_led}\n".encode()
                self.ser.write(cmd)
                self.get_logger().info(f'💡 Lighting LED {current_led}')
            feedback_msg.current_led = current_led
            feedback_msg.elapsed_time = elapsed
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(
                f'Feedback sent: LED={feedback_msg.current_led}, time={feedback_msg.elapsed_time}s'
            )
            if current_led >= total_leds and elapsed >= (total_leds - 1) * 2:
                break
            time.sleep(1)
        goal_handle.succeed()
        result.success = True
        result.result_message = f'All {total_leds} LEDs are ON ✅'
        self.get_logger().info(result.result_message)
        return result
    def destroy_node(self):
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()
            self.get_logger().info('Disconnected from Arduino')
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = LedActionServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Server stopped by user')
    finally:
        node.destroy_node()
        rclpy.shutdown()
if __name__ == '__main__':
    main()
