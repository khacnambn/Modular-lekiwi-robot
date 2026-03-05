#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import termios
import tty
import select

class OmniTeleop(Node):
    def __init__(self):
        super().__init__('omni_teleop')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.speed = 0.5
        self.turn = 1.0

        self.bindings = {
            'w': (1, 0, 0),
            's': (-1, 0, 0),
            'a': (0, 1, 0),
            'd': (0, -1, 0),
            'z': (0, 0, 1),
            'x': (0, 0, -1),
            'r': 'speed_up',
            'f': 'speed_down',
            'q': 'quit'
        }

        self.get_logger().info("OMNI TELEOP STARTED")
        self.get_logger().info("Use WASD to move, ZX to rotate, RF to change speed, Q to quit")
        self.run()

    def get_key(self):
        # read single keypress
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def run(self):
        self.settings = termios.tcgetattr(sys.stdin)
        try:
            while True:
                key = self.get_key()
                if key in self.bindings:
                    command = self.bindings[key]

                    if command == 'speed_up':
                        self.speed *= 1.1
                        self.turn *= 1.1
                        self.get_logger().info(f"Speed: {self.speed:.2f}, Turn: {self.turn:.2f}")

                    elif command == 'speed_down':
                        self.speed *= 0.9
                        self.turn *= 0.9
                        self.get_logger().info(f"Speed: {self.speed:.2f}, Turn: {self.turn:.2f}")

                    elif command == 'quit':
                        self.get_logger().info("Exiting teleop...")
                        break

                    else:
                        linear_x = command[0] * self.speed
                        linear_y = command[1] * self.speed
                        angular_z = command[2] * self.turn
                        twist = Twist()
                        twist.linear.x = linear_x
                        twist.linear.y = linear_y
                        twist.angular.z = angular_z
                        self.pub.publish(twist)

                elif key == '':
                    # Send stop command if no key pressed
                    twist = Twist()
                    self.pub.publish(twist)

        except Exception as e:
            self.get_logger().error(f"Exception: {e}")

        finally:
            twist = Twist()
            self.pub.publish(twist)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)


def main(args=None):
    rclpy.init(args=args)
    node = OmniTeleop()
    rclpy.shutdown()

if __name__ == '__main__':
    main()