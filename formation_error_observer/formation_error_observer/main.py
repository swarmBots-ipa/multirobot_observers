#! /usr/bin/env python3

import rclpy
from rclpy.executors import SingleThreadedExecutor
from formation_error_observer.pose_coordinates import PoseSubscriber
from formation_error_observer.goal_coordinates import GoalSubscriber
import sys
pose_nodes = []
goal_nodes = []
def main(args=None):
    agents=int(sys.argv[2])
    rclpy.init(args=args)
    try:
        for i in range(agents):
            pose_node = PoseSubscriber(sys.argv[1],robot_id = i)
            pose_nodes.append(pose_node)
            goal_node = GoalSubscriber(robot_id = i)
            goal_nodes.append(goal_node)

        for pose_node in pose_nodes:
            executor = SingleThreadedExecutor()
            executor.add_node(pose_node)
            executor.spin()

        for goal_node in goal_nodes:
            executor = SingleThreadedExecutor()
            executor.add_node(goal_node)
            executor.spin()    
        
    except KeyboardInterrupt:
        #For writing data into json and csv files
        print("Run ($python3 formation_observer_plotter.py) to generate graph")
        executor.shutdown()


if __name__ == '__main__':
    main()

