from my_interfaces.srv import MySRV

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

import random


class LightClientAsync(Node):

    def __init__(self):
        super().__init__('light_client_async')
        self.cli = self.create_client(MySRV, 'get_light')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = MySRV.Request()

    def send_request(self):
        self.req.request_msg = "need light value(lux)"
        return self.cli.call_async(self.req)


def main(args=None):
    try:
        rclpy.init(args=args)
        light_client = LightClientAsync()
        future = light_client.send_request()
        rclpy.spin_until_future_complete(light_client, future)
        response = future.result()
        light_client.get_logger().info(
            'request of "%s"(lux value), %s -> %d, %s'%
            (light_client.req.request_msg, str(type(light_client.req.request_msg)), response.response_msg, str(type(response.response_msg))))
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()