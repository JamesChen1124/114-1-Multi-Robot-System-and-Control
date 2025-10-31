import rclpy
from rclpy.node import Node
from my_interfaces.msg import MyMSG

class SpeedPublisher(Node):
    def __init__(self):
        super().__init__('speed_publisher')
        self.publisher_ = self.create_publisher(MyMSG, 'speed', 10)
        timer_period = 1.0
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0.0

    def timer_callback(self):
        msg = MyMSG()
        msg.data = self.i
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing speed: {msg.data:.2f}')
        self.i += 0.5

def main(args=None):
    rclpy.init(args=args)
    node = SpeedPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
