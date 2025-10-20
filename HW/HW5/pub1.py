import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8
from rclpy.logging import LoggingSeverity 
class RandomPublisher(Node): 
#創建一個子類別RandomPublisher，負責處理發送隨機數字這個任務。他已經繼承父類別Node這個基底，Node這個基底是rclpy提供的，內含一大堆的功能，因此不需要自己寫一個父類別。
        
    def __init__(self): 
    #每當做node=RandomPublisher()，這個物件會被建立好(看不到)，接著自動呼叫__init__(把節點所需東西建構好)，self則是指這個物件本身，用來存取或設定物件的屬性

        super().__init__('random_publisher') 
        #super會去呼叫父類別，而這句super().__init__('random_publisher')則是呼叫父類別Node的initializer，並設節點名稱為random_publi+she+r(會在ros node list上看到的)

        self.pub = self.create_publisher(UInt8, 'random_byte', 10) 
        #向ROS2登記一個Publisher物件，並存成(self.pub)這個屬性，這個屬性名稱可以自己取。後面的self.create_publisher是固定的，需一字不差而不能更改。
        #( )內需分別是:訊息類別, topic名稱(供訂閱，要跟subscriber一樣), 佇列深度

        self.timer = self.create_timer(0.2, self.timer_cb)
        #建立一個Timer物件，並存成self.timer這個屬性。每0.2秒執行一次回呼，self.timer_cb是回呼函式的參考，每次到期(0.2秒)就回呼他一次
        #( )內需分別是，計數秒數second, 需回呼函式

        self.get_logger().info('random_publisher started @5Hz on topic /random_byte')
        # self.get_logger()是Node提供的固定API，.info則是他的等級，取得這個節點專屬的logger，()裡面則是先用節點名random_publisher作為前綴，整行的作用是 啟動時給一條狀態訊息，確認節點名稱、頻率、topic是否正確
        self.get_logger().set_level(LoggingSeverity.INFO)
        
    def timer_cb(self):
    #回呼函式。會被上面寫的timer呼叫
        msg = UInt8()
        #建立一個訊息物件
        msg.data = random.randint(0, 255)
        self.pub.publish(msg)
        self.get_logger().info(f'Published: {msg.data}')

def main():
    rclpy.init()
    node = RandomPublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
