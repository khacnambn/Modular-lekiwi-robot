cmake_minimum_required(VERSION 3.10)
project(lekiwi_description)

find_package(ament_cmake REQUIRED)
find_package(robot_state_publisher REQUIRED)
find_package(rclpy REQUIRED)

install(
  DIRECTORY urdf launch urdf/meshes rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
