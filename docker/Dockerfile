FROM ros:foxy

# Set up environment
ENV ROS1_DISTRO=noetic
ENV ROS1_INSTALL_PATH=/opt/ros/noetic
ENV ROS2_DISTRO=foxy
ENV ROS2_INSTALL_PATH=/opt/ros/foxy

ENV ROS_MASTER_URI=http://10.42.0.7:11311
ENV ROS_IP=10.42.0.50
ENV ROS_DOMAIN_ID=0

# Add tools
RUN apt-get update && apt-get install -y \
    curl gnupg2 lsb-release locales \
    software-properties-common \
    build-essential cmake git wget \
    && add-apt-repository universe \
    && rm -rf /var/lib/apt/lists/*

# Add ROS 1 Noetic
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" \
    > /etc/apt/sources.list.d/ros-latest.list' \
    && curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc \
    | apt-key add -
# Install packages  
RUN apt-get update && apt-get install -y \
    ros-noetic-ros-base ros-noetic-catkin ros-noetic-roscpp \
    ros-noetic-std-msgs ros-noetic-rosbash python3-rosdep python3-rospkg \
    && rm -rf /var/lib/apt/lists/*

# Debugging tools
RUN apt-get update && apt-get install -y \
    iputils-ping vim iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Initialize rosdep
RUN rosdep init || true && rosdep update

# Change workspace and set up entrypoint
WORKDIR /
# COPY ./docker/bashrc /home/${USERNAME}/.bashrc
COPY ./docker/entrypoint.sh /entrypoint.sh
COPY ./workspaces /workspaces
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["bash"]