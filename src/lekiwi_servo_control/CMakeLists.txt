cmake_minimum_required(VERSION 3.10)
project(lekiwi_servo_control)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(ignition-gazebo6 REQUIRED)
find_package(ignition-plugin1 REQUIRED)

# Plugin library
add_library(lekiwi_servo_control SHARED src/lekiwi_servo_control.cpp)
target_include_directories(lekiwi_servo_control PUBLIC
  ${ignition-gazebo6_INCLUDE_DIRS}
)
target_link_libraries(lekiwi_servo_control
  ${ignition-gazebo6_LIBRARIES}
)
ament_target_dependencies(lekiwi_servo_control
  rclcpp std_msgs sensor_msgs ignition-plugin1
)

# Install
install(TARGETS
  lekiwi_servo_control
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

ament_package()