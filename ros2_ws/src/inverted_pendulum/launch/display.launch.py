import os

from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

from scripts import GazeboRosPaths

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    share_dir = FindPackageShare('inverted_pendulum').find('inverted_pendulum')

    urdf_file_name = 'inverted_pendulum.urdf'
    urdf = os.path.join(share_dir, 'urdf', urdf_file_name)

    rviz_config_file = os.path.join(share_dir, 'rviz', 'config.rviz')

    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    robot_state_publisher = Node(
        name='robot_state_publisher',
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time' : use_sim_time,
            'robot_description': robot_desc}],
        arguments=[urdf]
    )

    joint_state_publisher = Node(
        name='joint_state_publisher',
        package='joint_state_publisher',
        executable='joint_state_publisher'
    )

    joint_state_publisher_gui = Node(
        name='joint_state_publisher_gui',
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'
    )

    rviz = Node(
        name='rviz2',
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false'
        ),
        robot_state_publisher,
        joint_state_publisher,
        joint_state_publisher_gui,
        rviz
    ])