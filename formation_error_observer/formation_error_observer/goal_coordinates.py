#!/usr/bin/env python3


from geometry_msgs.msg import PoseStamped
from math import atan2
from tf_transformations import euler_from_quaternion
from rclpy.node import Node
import json
import os
import sys 

#global variables
no_of_bots= int(str((sys.argv[2])))
goal_data ={}

#creating empty arrays for storing data based on no of robots
for i in range(no_of_bots):
    goal_data["agent_"+str(i)+"_goal"] = list()

#creating paths
filename = os.path.basename(__file__)
search_dir = '/home/'
for root, dirs, files in os.walk(search_dir):
    if filename in files:
        file_location = os.path.join(root, filename)
        break

path = file_location.replace('formation_error_observer/'+filename,'data')
json_path = (path + "/json/Goals.json")

class GoalSubscriber(Node):
   #Subscribing topics
    def __init__(self,robot_id):
        super().__init__("Goal_subscriber_" + str(robot_id))
        self.subscription = self.create_subscription(PoseStamped,'/agent_'+str(robot_id)+'/send_pose',self.callback,10)
        self.robot_id = robot_id
        self.get_logger().info("agent_"+str(robot_id)+" GOAL SUBSCRIBER IS READY")


# fetching Coordinates 
    def callback(self, pose:PoseStamped):
        x=pose.pose.position.x
        y=pose.pose.position.y
        rot_q = pose.pose.orientation
        (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])  
        self.get_logger().info('=================================================')
        self.get_logger().info("agent_"+str(self.robot_id)+": Goal Coordinates: (x = " + str(x) + ", y = " + str(y) + ", Theta = " + str(theta)+")")
        goal_data["agent_"+str(self.robot_id)+"_goal"].append({"x":x, "y":y, "theta":theta})
        GoalSubscriber.final_data()
# Creating Json files
    def final_data():
        with open(json_path, "w") as output:
            final_goal_data=[goal_data]
            json.dump(final_goal_data, output, sort_keys=True)