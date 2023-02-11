#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import math
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Bool
from rclpy.executors import SingleThreadedExecutor
import sys
#from nav2_bt_navigator.msg import 
mileage_array = [[],[],[],[]]
class MileageObserver(Node):
    
    def __init__(self,arg,robot_id):
        super().__init__("mileage_observer")
        self.subscription2 = self.create_subscription(PoseStamped,'barista_'+str(robot_id)+'/send_pose',self.getGoalPoint,10)
        self.subscription2 = self.create_subscription(Odometry,'barista_'+str(robot_id)+'/odom',self.addPointToTotalDistance,10)
        self.subscription3 = self.create_subscription(Bool,'/barista_'+str(robot_id)+'/goal_status',self.status_check,10)
        self.iteration = int(arg)
        self.i=0
        self.pose_subscriber = None
        self.goal_subscriber = None
        self.total_distance = 0
        self.prev_x = 0.0
        self.prev_y = 0.0
        self.goal_point = []
        self.first_time = True
        self.robot_number = robot_id
    def getGoalPoint(self, g):
        self.goal_point = g

    def distancePoints(self,x1,y1,x2,y2):
        return math.hypot(x2 - x1, y2 - y1)
    def addPointToTotalDistance(self, current_point):
        
        if self.first_time:
            self.first_time = False
            self.prev_x = current_point.pose.pose.position.x
            self.prev_y = current_point.pose.pose.position.y
        else:
            self.x = current_point.pose.pose.position.x
            self.y = current_point.pose.pose.position.y

            self.total_distance += self.distancePoints(self.x, self.y, self.prev_x, self.prev_y)

            self.prev_x = self.x
            self.prev_y = self.y
            # print("Current distance traveled= " + str(self.total_distance) + " meters")
            # if self.goal_point != []:
            #    if self.distancePoints(self.x, self.y, self.goal_point.pose.position.x, self.goal_point.pose.position.y) <= 0.1:
            #        print("Total Distance = " + str(self.total_distance) + " meters")
            #        print("Press Ctrl+C to exit.")
            #        quit()
    def status_check(self, msg):
        """Checking wheather the robot has completed the navigation to Goal

        Args:
            msg (String): goal status message
        """
        if msg.data == True:
            self.i+=1
            if(self.i<=self.iteration):
                print("stopped")
                print("Distance travelled by barista_"+str(self.robot_number) + " in iteration "+ str(self.i) + " :", self.total_distance)
                mileage_array[self.robot_number].append(self.total_distance)
            else:
                print("max iterations reached press CTRL + C")
            self.first_time = True
            self.total_distance = 0

    def final_data():
        finalData = mileage_array
        return finalData  

        
def main(args=None):
    rclpy.init(args=args)
    try:
        mileage_subscriber_0 = MileageObserver(sys.argv[1],robot_id=0) 
        mileage_subscriber_1 = MileageObserver(sys.argv[1],robot_id=1)
        mileage_subscriber_2 = MileageObserver(sys.argv[1],robot_id=2)
        mileage_subscriber_3 = MileageObserver(sys.argv[1],robot_id=3)
        executor = SingleThreadedExecutor()

        executor.add_node(mileage_subscriber_0)
        executor.add_node(mileage_subscriber_1)
        executor.add_node(mileage_subscriber_2)
        executor.add_node(mileage_subscriber_3)
        executor.spin()
    
    
    except KeyboardInterrupt:
        print(mileage_array)
        executor.shutdown()

if __name__ == '__main__':
    main()
