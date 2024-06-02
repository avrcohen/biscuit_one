import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():

    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name = 'biscuit_one'

    launch_path_rsp = os.path.join(get_package_share_directory(package_name), 'launch', 'rsp.launch.py')
    launch_arguments_rsp = {'use_sim_time': 'true', 'use_ros2_control': 'false'}
    rsp = IncludeLaunchDescription(PythonLaunchDescriptionSource([launch_path_rsp]), launch_arguments=launch_arguments_rsp.items()) 
    
    launch_path_gazebo = os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
    gazebo_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'gazebo_params.yaml')
    launch_arguments_gazebo = {'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}
    gazebo = IncludeLaunchDescription(PythonLaunchDescriptionSource([launch_path_gazebo]), launch_arguments=launch_arguments_gazebo.items()) 

    launch_arguments_node = ['-topic', 'robot_description', '-entity', 'my_bot']
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py', arguments=launch_arguments_node, output='screen')
     

    diff_drive_spawner = Node(package="controller_manager", executable="spawner", arguments=["diff_cont"],)

    joint_broad_spawner = Node(package="controller_manager",executable="spawner", arguments=["joint_broad"],)

    # Launch!
    return LaunchDescription([rsp, gazebo, spawn_entity, diff_drive_spawner, joint_broad_spawner])