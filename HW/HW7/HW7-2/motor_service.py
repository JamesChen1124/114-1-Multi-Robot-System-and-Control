from my_interfaces.srv import StrToStr

import rclpy
from rclpy.node import Node
import serial
import time

ser = serial.Serial("COM3", 9600)
time.sleep(2)


class MotorService(Node):

    def __init__(self):
        super().__init__('motor_service')
        self.srv = self.create_service(StrToStr, 'motor_status', self.str_to_str_callback)
        self.getStringTimes = 0

    def str_to_str_callback(self, request, response):
        self.get_logger().info('Incoming request: "%s", %s' % (request.request_msg, str(type(request.request_msg))))
        motor_status = ""
        while self.getStringTimes <= 1:
            while ser.in_waiting > 0:
                motor_status = ser.readline().decode()
            self.getStringTimes += 1
        self.getStringTimes = 1
        if(motor_status == "motor on"):
            response.response_msg = "motor is activate!"
        else:
            response.response_msg = "motor is enactivate!"

        return response


def main(args=None):
    rclpy.init(args=args)

    motor_service = MotorService()

    rclpy.spin(motor_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
