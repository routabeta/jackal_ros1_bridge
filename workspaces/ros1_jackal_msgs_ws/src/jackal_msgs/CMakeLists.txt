cmake_minimum_required(VERSION 3.0.2)
project(jackal_msgs)

find_package(catkin REQUIRED COMPONENTS
  std_msgs
  message_generation
)

add_message_files( 
  FILES
  Drive.msg
  DriveFeedback.msg
  Feedback.msg
  Status.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(CATKIN_DEPENDS std_msgs message_runtime)