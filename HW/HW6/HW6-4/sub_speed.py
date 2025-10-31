import rclpy
from rclpy.node import Node
from my_interfaces.msg import MyMSG

class SpeedSubscriber(Node):
    def __init__(self):
        super().__init__('speed_subscriber')
        self.subscription = self.create_subscription(MyMSG, 'speed', self.listener_callback, 10)
        self.subscription

    def listener_callback(self, msg):
        self.get_logger().info(f'Received speed: {msg.data:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = SpeedSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
