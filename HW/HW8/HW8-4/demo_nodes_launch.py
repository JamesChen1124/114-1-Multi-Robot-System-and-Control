from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='demo_nodes_cpp',
            executable='talker',
            name='talker1',
            remappings=[('/chatter', '/chatter1')]
        ),
        Node(
            package='demo_nodes_py',
            executable='listener',
            name='listener1',
            remappings=[('/chatter', '/chatter1')]
        ),

        Node(
            package='demo_nodes_cpp',
            executable='talker',
            name='talker2',
            remappings=[('/chatter', '/chatter2')]
        ),
        Node(
            package='demo_nodes_py',
            executable='listener',
            name='listener2',
            remappings=[('/chatter', '/chatter2')]
        ),
    ])
