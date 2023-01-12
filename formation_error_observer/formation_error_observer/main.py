#! /usr/bin/env python3

import rclpy
from rclpy.executors import SingleThreadedExecutor
from multirobot_experiment.pose_json import PoseSubscriber
from multirobot_experiment.goal_json import GoalSubscriber
import sys

def main(args=None):

    rclpy.init(args=args)
    try:
        pose_node_0 = PoseSubscriber(sys.argv[1],robot_no = 0)   
        pose_node_1 = PoseSubscriber(sys.argv[1],robot_no = 1)
        pose_node_2 = PoseSubscriber(sys.argv[1],robot_no = 2)
        pose_node_3 = PoseSubscriber(sys.argv[1],robot_no = 3) 
        goal_node_0 = GoalSubscriber(robot_no = 0)   
        goal_node_1 = GoalSubscriber(robot_no = 1)
        goal_node_2 = GoalSubscriber(robot_no = 2)
        goal_node_3 = GoalSubscriber(robot_no = 3) 
        executor = SingleThreadedExecutor()
        executor.add_node(pose_node_0)
        executor.add_node(pose_node_1)
        executor.add_node(pose_node_2)
        executor.add_node(pose_node_3)
        executor.add_node(goal_node_0)
        executor.add_node(goal_node_1)
        executor.add_node(goal_node_2)
        executor.add_node(goal_node_3)
        executor.spin()
        
    except KeyboardInterrupt:
        #For writing data into json and csv files
        executor.shutdown()


if __name__ == '__main__':
    main()

