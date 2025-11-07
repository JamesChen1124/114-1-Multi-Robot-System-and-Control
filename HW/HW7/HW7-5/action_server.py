import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from fibonacci_interface.action import MyFibonacci


class MyFibonacciActionServer(Node):

    def __init__(self):
        super().__init__('my_fibonacci_action_server')

        self._action_server = ActionServer(
            self,
            MyFibonacci,
            'my_fibonacci',
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = MyFibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]


        for i in range(1, goal_handle.request.order):
            next_num = feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i - 1]
            feedback_msg.partial_sequence.append(next_num)

            self.get_logger().info(f'Feedback: {feedback_msg.partial_sequence}')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()
        result = MyFibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        self.get_logger().info(f'Result: {result.sequence}')
        return result

def main(args=None):
    rclpy.init(args=args)
    action_server = MyFibonacciActionServer()

    try:
        rclpy.spin(action_server)
    except KeyboardInterrupt:
        pass

    action_server.destroy()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
