#! /usr/bin/env python3

import rclpy
from rclpy.executors import SingleThreadedExecutor
from formation_error_observer.pose_coordinates import PoseSubscriber
from formation_error_observer.goal_coordinates import GoalSubscriber
import sys
nodes = []
i=0
def main(args=None):
    agents=int(sys.argv[2])
    rclpy.init(args=args)
    try:
        for i in range(agents):
            pose_node = PoseSubscriber(sys.argv[1],robot_id = i)
            nodes.append(pose_node)
            goal_node = GoalSubscriber(robot_id = i)
            nodes.append(goal_node)
        global executor
        executor = SingleThreadedExecutor()
        for node in nodes:
            executor.add_node(node)
            
        executor.spin() 
        

    except KeyboardInterrupt:
        executor.shutdown() 

def iteration_indicator(i):
    print('=================================================')
    print("<--ITERATION "+str(i)+" COMPLETED FOR ALL BOTS-->")
    print('=================================================')
    print("<----------PLEASE START NEXT ITERATION---------->")

def nodes_shutdown(i):
    print('=================================================')
    print("<--ITERATION "+str(i)+" COMPLETED FOR ALL BOTS-->")
    print('=================================================')
    print("<------------MAX ITERATIONS ACHIEVED------------>")
    print('=================================================')
    print('Press CTRL + C to exit')
    executor.shutdown()
    


if __name__ == '__main__':
    main()

