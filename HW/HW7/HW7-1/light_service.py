from my_interfaces.srv import MySRV

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
import serial


class LightService(Node):

    def __init__(self):
        super().__init__('light_service')
        self.srv = self.create_service(MySRV, 'get_light', self.get_light_callback)
        self.ser = serial.Serial('COM3', 9600, timeout=1)

    def get_light_callback(self, request, response):
        line = ""
    
        # organize message
        try:
            line = self.ser.readline().decode().strip()
            lux = float(line.replace("Light:", "").replace("lux", "").strip())
        except Exception as e:
            self.get_logger().warn(f"Failed to parse line: '{line}' ({e})")
            lux = -1.0
        
        # string to int
        response.response_msg = int(lux)
        self.get_logger().info('Incoming request(get lux value): %s, %s' % (request.request_msg, str(type(request.request_msg))))

        return response


def main():
    try:
        rclpy.init()
        light_service = LightService()
        rclpy.spin(light_service)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()