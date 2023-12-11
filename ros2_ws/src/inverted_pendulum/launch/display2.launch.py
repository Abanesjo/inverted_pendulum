from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    ld = LaunchDescription()

    ld.add_action(IncludeLaunchDescription(
        PathJoinSubstitution([
            FindPackageShare('urdf_launch'),
            'launch',
            'display.launch.py'
        ]),
        launch_arguments={
            'urdf_package':'inverted_pendulum',
            'urdf_package_path': PathJoinSubstitution(['urdf', 'inverted_pendulum.urdf'])
        }.items()
    ))

    return ld