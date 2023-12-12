from hashlib import sha224
import os
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
    name='use_sim_time',
    default_value='true',
    description='Use simulation (Gazebo) clock if true')

    share_dir = FindPackageShare(package='inverted_pendulum').find('inverted_pendulum')

    world_file_name = 'default.world'
    world_path = os.path.join(share_dir, 'worlds', world_file_name)

    gazebo_models_path = os.path.join(share_dir, 'models')
    os.environ["GAZEBO_MODEL_PATH"] = gazebo_models_path

    gazebo_plugins_path = os.path.join(share_dir, 'inverted_pendulum')
    os.environ["GAZEBO_PLUGIN_PATH"] = gazebo_plugins_path

    plot_path = os.path.join(share_dir, 'rviz', 'plotJuggler.xml')

    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzserver.launch.py'
            ])
        ]),
        launch_arguments={
            'pause': 'true',
            'world': world_path,
            'verbose': 'true'
        }.items()
    )

    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzclient.launch.py'
            ])
        ])
    )

    plot_juggler = ExecuteProcess(
        cmd=[
            'ros2',
            'run',
            'plotjuggler',
            'plotjuggler',
            '-l',
            plot_path
        ]
    )

    return LaunchDescription([
        declare_use_sim_time_cmd,
        gazebo_server,
        gazebo_client,
        plot_juggler
    ])
