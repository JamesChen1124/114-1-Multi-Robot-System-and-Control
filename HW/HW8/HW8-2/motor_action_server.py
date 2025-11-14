import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
import time
import serial
from motor_action_interfaces.action import MotorPWM


class MotorPWMServer(Node):
    def __init__(self):
        super().__init__('motor_action_server')
        self._action_server = ActionServer(
            self,
            MotorPWM,
            'motor_pwm_control',
            self.execute_callback)
        self.current_pwm = 0
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.ser.flush()
        self.get_logger().info("✅ Motor Action Server Ready.")

    def execute_callback(self, goal_handle):
        target = goal_handle.request.target_pwm
        self.get_logger().info(f'Received goal PWM: {target}')

        feedback_msg = MotorPWM.Feedback()
        step_time = 0.2
        feedback_interval = 1.0
        last_feedback_time = time.time()

        while self.current_pwm != target:
            step = 1 if target > self.current_pwm else -1
            self.current_pwm += step
            self.ser.write(f'{self.current_pwm}\n'.encode())
            time.sleep(step_time)

            if time.time() - last_feedback_time >= feedback_interval:
                feedback_msg.current_pwm = self.current_pwm
                goal_handle.publish_feedback(feedback_msg)
                self.get_logger().info(f'Feedback: PWM={self.current_pwm}')
                last_feedback_time = time.time()

        goal_handle.succeed()
        result = MotorPWM.Result()
        result.final_pwm = self.current_pwm
        self.get_logger().info(f'✅ Final PWM reached: {self.current_pwm}')
        return result


def main(args=None):
    rclpy.init(args=args)
    node = MotorPWMServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Server stopped.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

