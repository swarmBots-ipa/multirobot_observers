#!/usr/bin/env python3
import math
import rclpy
from nav_msgs.msg import Path
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import PoseStamped
from actionlib_msgs.msg import GoalID
from std_msgs.msg import Bool
import sys
import os
      
subscriber = None
actual_path_length = []
no_of_bots= int(str((sys.argv[2])))
for n in range(no_of_bots):
    actual_path_length.append([])
filename = os.path.basename(__file__)
search_dir = '/home/'
for root, dirs, files in os.walk(search_dir):
    if filename in files:
        file_location = os.path.join(root, filename)
        break
path = file_location.replace('mileage_observer/'+filename,'data')
csv_path = (path + "/csv/Robot")

class PathDistance(Node):
      

    def __init__(self,arg,robot_id):
        global subscriber  
        self.i=1
        self.iterations=int(arg)
        super().__init__('calculate_path_distance_'+str(robot_id))
        self.subscriber = self.create_subscription(Path,'/barista_'+str(robot_id)+'/plan', self.printPath,10)
        self.subscription3 = self.create_subscription(Bool,'/barista_'+str(robot_id)+'/goal_status',self.status_check,10)
        self.robot_id=robot_id
        print('PATH OBSERVER FOR BOT_'+str(robot_id)+' READY')

    def status_check(self, msg):
        if msg.data == True:
            self.i+=1
                        
    def printPath(self,path):
        
        global subscriber
        first_time = True
        prev_x = 0.0
        prev_y = 0.0
        total_distance = 0.0
       # if(self.i<=self.iterations):
        if self.i <= self.iterations:
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
                    #self.destroy_subscription(subscriber)
                    if ((self.i-1)==len(actual_path_length[self.robot_id])):
                        actual_path_length[self.robot_id].append(total_distance)
                        print("Iteration : " + str(self.i) + " Total length of path for barista_"+str(self.robot_id)+" = "+str(total_distance)+" meters")

    

    def final_data():
        finalData = actual_path_length
        return finalData             