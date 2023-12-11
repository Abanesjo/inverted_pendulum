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

    gazebo_launch = IncludeLaunchDescription(
        PathJoinSubstitution(
            [
                FindPackageShare('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            ]
        ),
        launch_arguments={
            'gui': 'true',
            'pause': 'true',
            'verbose': 'true'
        }.items()
    )

    urdf_spawner_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='urdf_spawner',
        arguments=['-topic', '/robot_description', '-entity', 'inverted_pendulum', '-z', '0.5', '-unpause'],
        output='screen'
    )

    return LaunchDescription([
        gazebo_launch,
        robot_state_publisher,
        urdf_spawner_node
    ])