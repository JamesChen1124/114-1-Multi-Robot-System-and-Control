import rclpy
from rclpy.node import Node
from my_interfaces.srv import MySRV

class MoneyService(Node):
    def __init__(self):
        super().__init__('money_service')
        self.srv = self.create_service(MySRV, 'money', self.money_callback)

    def money_callback(self, request, response):
        self.get_logger().info(f'Received request: {request.msg}')
        response.data = len(request.msg) * 100
        self.get_logger().info(f'Response data: {response.data}')
        return response

def main(args=None):
    rclpy.init(args=args)
    node = MoneyService()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
