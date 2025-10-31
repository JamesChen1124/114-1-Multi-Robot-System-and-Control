import sys
import rclpy
from rclpy.node import Node
from my_interfaces.srv import MySRV

class MoneyClient(Node):
    def __init__(self):
        super().__init__('money_client')
        self.cli = self.create_client(MySRV, 'money')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')
        self.req = MySRV.Request()

    def send_request(self, message: str):
        self.req.msg = message
        return self.cli.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)
    node = MoneyClient()
    text = sys.argv[1] if len(sys.argv) >= 2 else input("Enter message: ")
    future = node.send_request(text)
    rclpy.spin_until_future_complete(node, future)
    if future.result() is not None:
        node.get_logger().info(f"Response int64: {future.result().data}")
    else:
        node.get_logger().error("Service call failed")
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

