# multiplier_client.py
import sys, rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MultiplierClient(Node):
    def __init__(self):
        super().__init__('multiplier_client')
        self.cli = self.create_client(AddTwoInts, 'multiply_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('waiting for service...')

    def call(self, a, b):
        req = AddTwoInts.Request(); req.a, req.b = int(a), int(b)
        future = self.cli.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        return future.result().sum          #乘積

def main():
    rclpy.init(); node = MultiplierClient()
    a, b = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) >= 3 else (3, 5)
    product = node.call(a, b)
    node.get_logger().info(f'Product = {product}')
    node.destroy_node(); rclpy.shutdown()

if __name__ == '__main__': main()
