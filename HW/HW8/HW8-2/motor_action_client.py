import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from motor_action_interfaces.action import MotorPWM
import time


class MotorPWMClient(Node):
    def __init__(self):
        super().__init__('motor_action_client')
        self.client = ActionClient(self, MotorPWM, 'motor_pwm_control')
        self._get_result_future = None

    def send_goal(self, target_pwm):
        goal_msg = MotorPWM.Goal()
        goal_msg.target_pwm = target_pwm
        self.get_logger().info(f'Sending goal: PWM {target_pwm}')

        self.client.wait_for_server()
        self._send_goal_future = self.client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('❌ Goal rejected.')
            return
        self.get_logger().info('✅ Goal accepted.')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        current = feedback_msg.feedback.current_pwm
        self.get_logger().info(f'Feedback (每秒): current PWM = {current}')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Final PWM reached: {result.final_pwm}')


def main(args=None):
    rclpy.init(args=args)
    node = MotorPWMClient()

    try:
        target = int(input("請輸入目標 PWM (0~255): "))
    except ValueError:
        print("請輸入整數。")
        node.destroy_node()
        rclpy.shutdown()
        return

    node.send_goal(target)

    while rclpy.ok():
        rclpy.spin_once(node, timeout_sec=1.0)
        time.sleep(1.0)
        if node._get_result_future and node._get_result_future.done():
            break

    node.destroy_node()
    rclpy.shutdown()
    print("✅ 已完成，返回 shell")

