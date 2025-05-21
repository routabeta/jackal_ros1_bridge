import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import termios, sys, tty, select, signal

class KB_Control(Node):
    def __init__(self):
        super().__init__("kb_control")
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info("[KB_CONTROL] starting kb control.\n|\n|\n|\n|\n|")

    def get_key(self):  
        new_settings = termios.tcgetattr(sys.stdin)
        new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
            if key =='\x03': raise KeyboardInterrupt
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, og_settings)
        return key
    
    def timer_callback(self):
        # get key and depending on what it is, publish to cmd_vel
        key = self.get_key()
        msg = Twist()
        if key == 'q':
            msg.linear.x = 0.5
            msg.angular.z = 1.0
        elif key == 'w':
            msg.linear.x = 0.5
        elif key == 'e':
            msg.linear.x = 0.5
            msg.angular.z = -1.0
        elif key == 'a':
            msg.angular.z = 1.0
        elif key == 's':
            msg.linear.x = -0.5
        elif key == 'd':
            msg.angular.z = -1.0
        elif key == "Q":
            msg.linear.x = 2.0
            msg.angular.z = 2.0
        elif key == 'W':
            msg.linear.x = 2.0
        elif key == "E":
            msg.linear.x = 2.0
            msg.angular.z = -2.0
        elif key == 'S':
            msg.linear.x = -2.0
        elif key == 'A':
            msg.angular.z = 2.0
        elif key == 'D':
            msg.angular.z = -2.0

        if key:
            self.publisher_.publish(msg)

def main():
    global og_settings
    og_settings = termios.tcgetattr(sys.stdin)
    rclpy.init()

    node = KB_Control()
    def shutdown_handler(signum, frame):
        node.get_logger().info("Exiting due to keyboard interrupt...")
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, og_settings)
        rclpy.shutdown()
    signal.signal(signal.SIGINT, shutdown_handler)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Exiting due to signal interrupt")
    finally:
        rclpy.shutdown()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, og_settings)  

if __name__ == "__main__":
    main()