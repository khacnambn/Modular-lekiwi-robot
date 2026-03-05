from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    pkg_path = get_package_share_directory('lekiwi_description')
    urdf_path = os.path.join(pkg_path, 'urdf', 'LeKiwi.urdf')

    with open(urdf_path, 'r') as inf:
        robot_description = inf.read()

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': use_sim_time
            }]
        )

        # Node(
        #     package='joint_state_publisher',
        #     executable='joint_state_publisher',
        # )

        # Node(
        #     package='rviz2',
        #     executable='rviz2',
        #     arguments=['-d', os.path.join(pkg_path, 'rviz', 'modeltest.rviz')],
        #     output='screen'
        # )
    ])
