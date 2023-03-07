#! /usr/bin/env python3

import rclpy
from rclpy.executors import SingleThreadedExecutor
from mileage_observer.path_observer import PathDistance
from mileage_observer.mileage_observer import MileageObserver
import sys


nodes =[]
def main(args=None):
    agents=int(sys.argv[2])
    rclpy.init(args=args)
    try:

        for i in range(agents):
            pose_node = PathDistance(sys.argv[1],robot_id = i)
            nodes.append(pose_node)
            goal_node = MileageObserver(sys.argv[1],robot_id=i) 
            nodes.append(goal_node)
        global executor
        executor = SingleThreadedExecutor()
        for node in nodes:
            executor.add_node(node)
            
        executor.spin() 
    

    except KeyboardInterrupt:
       
        executor.shutdown()
def shut_down():
        executor.shutdown()

if __name__ == '__main__':
    main()

