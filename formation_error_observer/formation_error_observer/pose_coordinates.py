#!/usr/bin/env python3


from geometry_msgs.msg import PoseWithCovarianceStamped
from std_msgs.msg import Bool
from math import atan2
from tf_transformations import euler_from_quaternion
from rclpy.node import Node
import json
import csv
from formation_error_observer.goal_coordinates import GoalSubscriber
import os
import sys
#global variables

#Fetching no of bots from szstem arguments
no_of_bots= int(str((sys.argv[2])))
pose_data ={}

#creating empty arrays for storing data based on no of robots
for i in range(no_of_bots):
    pose_data["agent_"+str(i)+"_pose"] = list()
bot_coord =[]
for i in range(no_of_bots):
    bot_coord.append([])
    for j in range(4):
        bot_coord[i].append([])

counter = 0

#creating paths
filename = os.path.basename(__file__)
search_dir = '/home/'
for root, dirs, files in os.walk(search_dir):
    if filename in files:
        file_location = os.path.join(root, filename)
        break
path = file_location.replace('formation_error_observer/'+filename,'data')



json_folder = path+"/json"
csv_folder= path+"/csv"
graph_folder = path+"/graphs"
json_path = (path + "/json/Poses.json")
csv_path = (path + "/csv/Robot")

#Clearing Old data
def clear_old_data(folder_path):
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)

clear_old_data(json_folder)
clear_old_data(csv_folder)
clear_old_data(graph_folder)


class PoseSubscriber(Node):
   
    #Subscriber function 
    
    def __init__(self,arg,robot_id):
    
        
        super().__init__("Pose_subscriber_" + str(robot_id))
        self.subscription = self.create_subscription(PoseWithCovarianceStamped,'/agent_'+str(robot_id)+'/amcl_pose',self.callback,10)    
        self.subscription2 = self.create_subscription(Bool,'/agent_'+str(robot_id)+'/goal_status',self.goal_callback,10)
        self.robot_id = robot_id
        self.i = 0
        
        self.iteration = int(arg)
        self.get_logger().info("agent_"+str(robot_id)+" POSE SUBSCRIBER IS READY")

# fetching Coordinates    
    def callback(self, pose:PoseWithCovarianceStamped):
        self.time = pose.header.stamp.sec
        self._x=pose.pose.pose.position.x
        self._y=pose.pose.pose.position.y
        self.rot_q = pose.pose.pose.orientation
        (roll, pitch, self._theta) = euler_from_quaternion([self.rot_q.x, self.rot_q.y, self.rot_q.z, self.rot_q.w])  
        #self.get_logger().info("(X = " + str(self._x) + ",  Y= " + str(self._y) + ", Theta = " + str(self._theta) + ") agent_"+str(self.robot_id))
        i=self.robot_id
        bot_coord[i][0].append(self._x);bot_coord[i][1].append(self._y);bot_coord[i][2].append(self._theta);bot_coord[i][3].append(self.time)
        self.csv_data()
    
#fetching last coordinates after successfully reaching goal

    def goal_callback(self,goal:Bool):
        self.get_logger().info('=================================================')
        if (goal.data==True):
            self.get_logger().info("agent_"+str(self.robot_id)+": reached goal.")
            self.get_logger().info("agent_"+str(self.robot_id)+": Pose Coordinates: (x = " + str(self._x) + ", y = " + str(self._y) + ", Theta = " + str(self._theta)+")")
            pose_data["agent_"+str(self.robot_id)+"_pose"].append({"x":self._x, "y":self._y, "theta":self._theta})
            self.json_data()
            self.iteration_counter()
            
            
#Counting no. of iterations and shutting down node after reaching max iterations
    def iteration_counter(self):
        self.i += 1
        self.get_logger().info( "agent_" + str(self.robot_id)+ ": Iteration No.(" + str(self.i) + ") Completed.")
        global counter
        counter+=1
        if self.i==self.iteration:
            if counter == no_of_bots:
                self.get_logger().info('=================================================')
                self.get_logger().info("<--ITERATION "+str(self.i)+" COMPLETED FOR ALL BOTS-->")
                self.get_logger().info('=================================================')
                self.get_logger().info("<------------MAX ITERATIONS ACHIEVED------------>")
                self.get_logger().info('=================================================')
                self.get_logger().info('Press CTRL + C to exit')
                from formation_error_observer.main import nodes_shutdown
                nodes_shutdown()
        else:
            if counter == no_of_bots:
                self.get_logger().info('=================================================')
                self.get_logger().info("<--ITERATION "+str(self.i)+" COMPLETED FOR ALL BOTS-->")
                self.get_logger().info('=================================================')
                self.get_logger().info("<----------PLEASE START NEXT ITERATION---------->")
                counter = 0
        

#Writing json and csv files
    def json_data(self):
        final_pose_data=[pose_data]
        with open(json_path, "w") as output:
            json.dump(final_pose_data, output, sort_keys=True) 

    def csv_data(self):
        bot_coordinates=[]
        bot_coordinates.append(bot_coord)
        for i in range(no_of_bots):
            with open(csv_path + str(i) + '.csv', 'w', newline='')as f:
                field_names= ['X','Y','Theta','Timestamp']
                writer = csv.DictWriter(f, fieldnames=field_names)
                writer.writeheader()
                length = len(bot_coordinates[0][i][0])
                for j in range(length):
                    writer.writerow({'X':bot_coordinates[0][i][0][j],'Y':bot_coordinates[0][i][1][j],'Theta':bot_coordinates[0][i][2][j],'Timestamp':bot_coordinates[0][i][3][j]})