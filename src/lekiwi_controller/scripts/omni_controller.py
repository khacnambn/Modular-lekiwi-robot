#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import numpy as np

class OmniController(Node):
    def __init__(self):
        super().__init__('omni_controller')
        # Parameters
        self.wheel_radius = 0.05  # Radius of wheels
        self.wheel_base = 0.1732  # Distance from center to wheel
        # Joint axis for each wheel (normalized)
        self.joint_axes = [
            np.array([0.866025, 0.0, 0.5]) / np.linalg.norm([0.866025, 0.0, 0.5]),
            np.array([0.866025, 0.0, 0.5]) / np.linalg.norm([0.866025, 0.0, 0.5]),
            np.array([0.866025, 0.0, 0.5]) / np.linalg.norm([0.866025, 0.0, 0.5])
        ]
        # Wheel positions relative to base_link
        self.wheel_positions = [
            np.array([0.1732, 0.0, 0.0]),
            np.array([-0.0866, 0.15, 0.0]),
            np.array([-0.0866, -0.15, 0.0])
        ]

        # Publishers for wheel velocities
        self.wheel_pubs = [
            self.create_publisher(Float64, f'/lekiwi/wheel_{i}/cmd_vel', 10)
            for i in range(3)
        ]

        # Subscriber for cmd_vel
        self.cmd_vel_sub = self.create_subscription(
            Twist, '/lekiwi/cmd_vel', self.cmd_vel_callback, 10
        )

    def cmd_vel_callback(self, msg):
        # Extract linear and angular velocities
        vx = msg.linear.x
        vy = msg.linear.y
        wz = msg.angular.z

        # Kinematics for 3 omni wheels with custom joint axes
        wheel_speeds = []
        for i in range(3):
            # Robot velocity at wheel position
            wheel_vel = np.array([
                vx - wz * self.wheel_positions[i][1],
                vy + wz * self.wheel_positions[i][0],
                0.0
            ])
            # Project onto joint axis to get angular velocity
            angular_speed = np.dot(wheel_vel, self.joint_axes[i]) / self.wheel_radius
            wheel_speeds.append(angular_speed)

        # Publish wheel velocities
        for i, speed in enumerate(wheel_speeds):
            vel_msg = Float64()
            vel_msg.data = speed
            self.wheel_pubs[i].publish(vel_msg)

def main(args=None):
    rclpy.init(args=args)
    node = OmniController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()