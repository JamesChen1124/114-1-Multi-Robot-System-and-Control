import sys

from my_interfaces.srv import StrToStr
import rclpy
from rclpy.node import Node


class MotorClientAsync(Node):

    def __init__(self):
        super().__init__('motor_client_async')
        self.cli = self.create_client( StrToStr, 'motor_status')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req =  StrToStr.Request()

    def send_request(self):
        self.req.request_msg = "need motor status(status request)"
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main(args=None):
    rclpy.init(args=args)

    motor_client = MotorClientAsync()
    response = motor_client.send_request()
    motor_client.get_logger().info(
        'Result (status): %s, %s'%
        (response.response_msg, str(type(response.response_msg))))

    motor_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
