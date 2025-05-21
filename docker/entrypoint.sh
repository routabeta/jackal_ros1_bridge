#!/bin/bash
set -e

# 1. Build ROS 1 workspace (ROS 1 only)
(
	source ${ROS1_INSTALL_PATH}/setup.bash
	cd /workspaces/ros1_jackal_msgs_ws
	catkin_make_isolated --install || {
		echo "[ENTRYPOINT] Failed to build ros1_jackal_msgs_ws"
		exit 1
	}
)


# 2. Build ROS 2 workspaces (ROS 2 only)
(
	source ${ROS2_INSTALL_PATH}/setup.bash
	cd /workspaces/ros2_jackal_msgs_ws
	colcon build --symlink-install --packages-select jackal_msgs || {
		echo "[ENTRYPOINT] Failed to build ros2_jackal_msgs"
		exit 1
	}
	cd /workspaces/jackal_control_ros2_ws
	colcon build --symlink-install --packages-select keyboard_control || {
		echo "[ENTRYPOINT] Failed to build keyboard_control"
		exit 1
	}
)

# 3. Build ros1_bridge (ROS 1 + ROS 2)
(
	source ${ROS1_INSTALL_PATH}/setup.bash
	source ${ROS2_INSTALL_PATH}/setup.bash
	source /workspaces/ros1_jackal_msgs_ws/install_isolated/setup.bash
	source /workspaces/ros2_jackal_msgs_ws/install/local_setup.bash
	
	cd /workspaces/ros1_bridge_ws # Build bridge
	colcon build --symlink-install --packages-select ros1_bridge --cmake-force-configure || {
		echo "[ENTRYPOINT] Failed to build ros1_bridge"
		exit 1
	}
)

echo "[ENTRYPOINT] bridge built"
exec /bin/bash
