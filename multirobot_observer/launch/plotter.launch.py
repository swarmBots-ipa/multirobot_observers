from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription([
        Node(
            package='formation_error_observer',
            executable='formation_observer_plotter',
            name='formation_error_observer'
            
        ),

        Node(
            package='mileage_observer',
            executable='mileage_observer_plotter',
            name='mileage_observer'
            
        ),

        Node(
            package='power_usage_observer',
            executable='power_observer_plotter',
            name='power_usage_observer'
            
        )

    

    ])
     

    return ld