#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from std_msgs.msg import Float64
import tf2_ros
import numpy as np

class OmniOdometry(Node):
    def __init__(self):
        super().__init__('omni_odometry')
        self.wheel_radius = 0.05
        self.wheel_base = 0.1732
        self.joint_axes = [
            np.array([0.866025, 0.0, 0.5]) / np.linalg.norm([0.866025, 0.0, 0.5]),
            np.array([0.866025, 0.0, 0.5]) / np.linalg.norm([0.866025, 0.0, 0.5]),
            np.array([0.866025, 0.0, 0.5]) / np.linalg.norm([0.866025, 0.0, 0.5])
        ]
        self.wheel_positions = [
            np.array([0.1732, 0.0, 0.0]),
            np.array([-0.0866, 0.15, 0.0]),
            np.array([-0.0866, -0.15, 0.0])
        ]
        
        # Odometry state
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.last_time = self.get_clock().now()

        # Publishers
        self.odom_pub = self.create_publisher(Odometry, '/lekiwi/odom', 10)
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

        # Subscribers for wheel velocities
        self.wheel_vels = [0.0] * 3
        self.wheel_subs = [
            self.create_subscription(Float64, f'/lekiwi/wheel_{i}/cmd_vel', 
                lambda msg, i=i: self.wheel_vel_callback(msg, i), 10)
            for i in range(3)
        ]

        # Timer for odometry update
        self.timer = self.create_timer(0.01, self.update_odometry)

    def wheel_vel_callback(self, msg, wheel_idx):
        self.wheel_vels[wheel_idx] = msg.data

    def update_odometry(self):
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time

        # Calculate robot velocity from wheel velocities
        vx = 0.0
        vy = 0.0
        wz = 0.0
        for i in range(3):
            # Wheel velocity in world frame
            angular_speed = self.wheel_vels[i]
            wheel_vel = angular_speed * self.wheel_radius * self.joint_axes[i]
            # Contribute to robot velocity
            vx += wheel_vel[0] / 3.0
            vy += wheel_vel[1] / 3.0
            wz += np.cross(self.wheel_positions[i], wheel_vel)[2] / (3.0 * self.wheel_base)

        # Update position and orientation
        self.theta += wz * dt
        self.x += (vx * np.cos(self.theta) - vy * np.sin(self.theta)) * dt
        self.y += (vx * np.sin(self.theta) + vy * np.cos(self.theta)) * dt

        # Publish odometry
        odom = Odometry()
        odom.header.stamp = current_time.to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation.z = np.sin(self.theta / 2.0)
        odom.pose.pose.orientation.w = np.cos(self.theta / 2.0)
        odom.twist.twist.linear.x = vx
        odom.twist.twist.linear.y = vy
        odom.twist.twist.angular.z = wz
        self.odom_pub.publish(odom)

        # Publish TF
        tf = TransformStamped()
        tf.header.stamp = current_time.to_msg()
        tf.header.frame_id = 'odom'
        tf.child_frame_id = 'base_link'
        tf.transform.translation.x = self.x
        tf.transform.translation.y = self.y
        tf.transform.rotation.z = np.sin(self.theta / 2.0)
        tf.transform.rotation.w = np.cos(self.theta / 2.0)
        self.tf_broadcaster.sendTransform(tf)

def main(args=None):
    rclpy.init(args=args)
    node = OmniOdometry()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()