#!/usr/bin/env python3


import rclpy
from geometry_msgs.msg import PoseStamped
from math import atan2
from tf_transformations import euler_from_quaternion
from rclpy.node import Node
import json
from rclpy.executors import SingleThreadedExecutor
import sys

#Setting Arrays and dict for data storage (data = goal final coordinates)
goal_data={"barista_0_goal":list(), "barista_1_goal":list(), "barista_2_goal":list(), "barista_3_goal":list()}
bot_coord = [[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]]

class GoalSubscriber(Node):
   
    def __init__(self,robot_no):
        super().__init__("Goal_subscriber")
        self.subscription = self.create_subscription(PoseStamped,'/barista_'+str(robot_no)+'/send_pose',self.callback,10)
        self.robot_id = robot_no
        self.get_logger().info("Barista_Goal IS READY")


# fetching Coordinates 
    def callback(self, pose:PoseStamped):
        x=pose.pose.position.x
        y=pose.pose.position.y
        rot_q = pose.pose.orientation
        (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])  
        self.get_logger().info("(" + str(x) + " X " + str(y) + ")" + str(theta))
        goal_data["barista_"+str(self.robot_id)+"_goal"].append({"x":x, "y":y, "theta":theta})
        
# Creating Json files
    def final_data():
        with open('../data/json/Goals.json', "w") as output:
            final_goal_data=[goal_data]
            json.dump(final_goal_data, output, sort_keys=True)
            

