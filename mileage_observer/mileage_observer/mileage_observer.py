#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import math
import csv
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Bool
from rclpy.executors import SingleThreadedExecutor
import sys
import os
from mileage_observer import path_observer
#from nav2_bt_navigator.msg import 
path_travelled = []
no_of_bots= int(str((sys.argv[2])))
for n in range(no_of_bots):
    path_travelled.append([])
counter = 0
filename = os.path.basename(__file__)
search_dir = '/home/'
for root, dirs, files in os.walk(search_dir):
    if filename in files:
        file_location = os.path.join(root, filename)
        break
path = file_location.replace('mileage_observer/'+filename,'data')
csv_path = path + "/csv/Robot"
csv_folder= path+"/csv"
graph_folder = path+"/graphs"

def clear_old_data(folder_path):
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)

clear_old_data(csv_folder)
clear_old_data(graph_folder)

class MileageObserver(Node):
    
    def __init__(self,arg,robot_id):
        super().__init__("mileage_observer_"+str(robot_id))
        self.subscription2 = self.create_subscription(PoseStamped,'barista_'+str(robot_id)+'/send_pose',self.getGoalPoint,10)
        self.subscription2 = self.create_subscription(Odometry,'barista_'+str(robot_id)+'/odom',self.addPointToTotalDistance,10)
        self.subscription3 = self.create_subscription(Bool,'/barista_'+str(robot_id)+'/goal_status',self.status_check,10)
        print('MILEAGE OBSERVER FOR BOT_'+str(robot_id)+' READY')
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
           
    def status_check(self, msg):
        """Checking wheather the robot has completed the navigation to Goal

        Args:
            msg (String): goal status message
        """
        if msg.data == True:
            self.i+=1
            if(self.i<=self.iteration):
                print('batrista_0'+str(self.robot_number)+" stopped")
                print("Distance travelled by barista_"+str(self.robot_number) + " in iteration "+ str(self.i) + " :", self.total_distance)
                path_travelled[self.robot_number].append(self.total_distance)
                global actual_path_length
                actual_path_length = path_observer.actual_path_length
                self.csv_data()
                global counter
                counter+=1
                print(counter)
                if counter==no_of_bots:
                    print('=======================================')
                    print('==ITERATION '+str(self.i)+' COMPLETE===')
                    print('=======================================')
                    if(self.i != self.iteration):
                        print('=====PLEASE START NEXT ITERATION=======')
                        print('=======================================')
                    counter =0
                    if self.i == self.iteration:
                        print("MAX ITERATIONS ACHIEVED. PRESS CTRL + C")
                        print('=======================================')
                        from mileage_observer.main import shut_down
                        shut_down()
            self.first_time = True
            self.total_distance = 0

    def csv_data(self):
        for i in range(no_of_bots):
            with open(csv_path + str(i) + '.csv', 'w', newline='')as f:
                field_names= ['Iteration No','Actual Path Length','Path Travelled']
                writer = csv.DictWriter(f, fieldnames=field_names)
                writer.writeheader()
                length = len(path_travelled[i])
                for j in range(length):
                    writer.writerow({'Iteration No':j+1,'Actual Path Length':actual_path_length[i][j],'Path Travelled':path_travelled[i][j]})


    def final_data():
        finalData = path_travelled
        return finalData  

