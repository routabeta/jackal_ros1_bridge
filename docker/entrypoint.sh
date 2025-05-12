#!/bin/bash
set -e

# Note this path after COPY in Dockerfile
WORKSPACE_PATH=/workspaces/ros1_bridge_ws

# Source ROS 2
source ${ROS2_INSTALL_PATH}/setup.bash || {
	echo "[ENTRYPOINT] Failed to source ROS 2 $ROS2_DISTRO"
	exit 1
}

# Build all except ros1_bridge
cd $WORKSPACE_PATH
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --packages-skip ros1_bridge || {
	echo "[ENTRYPOINT] Failed to build all (non-ros1_bridge)"
	exit 1
}

# Source ROS 1
source ${ROS1_INSTALL_PATH}/setup.bash || {
	echo "[ENTRYPOINT] Failed to source ROS 1 $ROS1_DISTRO"
	exit 1
}

# Build ros1_bridge
colcon build --symlink-install --packages-select ros1_bridge --cmake-force-configure || {
	echo "[ENTRYPOINT] Failed to build ros1_bridge"
	exit 1
}

echo "[ENTRYPOINT] bridge built"
exec /bin/bash
