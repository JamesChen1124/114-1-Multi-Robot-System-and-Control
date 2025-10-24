# multiplier_service.py
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MultiplierService(Node):
    def __init__(self):
        super().__init__('multiplier_service')
        self.srv = self.create_service(AddTwoInts, 'multiply_two_ints', self.cb)

    def cb(self, req, res):
        res.sum = req.a * req.b            #乘法
        self.get_logger().info(f'{req.a} * {req.b} = {res.sum}')
        return res

def main():
    rclpy.init(); node = MultiplierService()
    try: rclpy.spin(node)
    finally: node.destroy_node(); rclpy.shutdown()

if __name__ == '__main__': main()
