#! /usr/bin/env python3

import rclpy
from rclpy.executors import SingleThreadedExecutor
import sys
from power_usage_observer.power_usage_observer import PowerUsageObserver


#Initializing and appending nodes based on no. of robots
nodes = []
def main(args=None):
    agents = int(sys.argv[1])
    rclpy.init(args=args)
    try: 
        for i in range(agents):
         power_node = PowerUsageObserver(robot_id = i)
         nodes.append(power_node)
         global executor
        executor = SingleThreadedExecutor()
        for node in nodes:
            executor.add_node(node)
            
        executor.spin() 
    

    except KeyboardInterrupt:
       
        executor.shutdown()


if __name__ == '__main__':
    main()
