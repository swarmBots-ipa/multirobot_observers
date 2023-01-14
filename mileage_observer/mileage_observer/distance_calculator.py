import math
import rclpy
from nav_msgs.msg import Path
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import PoseStamped
from actionlib_msgs.msg import GoalID
import sys
import os
      
subscriber = None

class PathDistance(Node):
    
    def __init__(self,robot_id):
            global subscriber  
            
            super().__init__('calculate_path_distance')
            self.subscriber = self.create_subscription(Path,'/barista_'+str(robot_id)+'/plan', self.printPath,10)
            self.robot_id=robot_id
            print ("Listening to /barista_"+str(robot_id)+"/plan")
            

    def printPath(self,path):
        global subscriber
        first_time = True
        
        prev_x = 0.0
        prev_y = 0.0
        total_distance = 0.0
        if len(path.poses) > 0:
            for current_point in path.poses:
                x = current_point.pose.position.x
                y = current_point.pose.position.y
                if not first_time:
                    total_distance += math.hypot(prev_x - x, prev_y - y) 
                else:
                    first_time = False
                prev_x = x
                prev_y = y
            self.destroy_subscription(subscriber)
            print("Total distance remaining for bot_"+str(self.robot_id)+" = "+str(total_distance)+" meters")

def main(args=None):

    rclpy.init(args=args)
    try:
        node_0= PathDistance(robot_id=0)
        node_1= PathDistance(robot_id=1)
        node_2= PathDistance(robot_id=2)
        node_3= PathDistance(robot_id=3)
        executor = SingleThreadedExecutor()

        executor.add_node(node_0)
        executor.add_node(node_1)
        executor.add_node(node_2)
        executor.add_node(node_3)
        executor.spin()
        

    except KeyboardInterrupt:
        rclpy.shutdown()

if __name__ == '__main__':
    main()