#!/usr/bin/env python3
#Current path witten using utils.py
current_path = "/home/janavi/swarmbot2/src/formation_error_observer/data" 
import rclpy
from geometry_msgs.msg import Point, Twist, PoseWithCovarianceStamped
from nav2_msgs.msg import BehaviorTreeLog
from std_msgs.msg import String
from math import atan2
from tf_transformations import euler_from_quaternion
from rclpy.node import Node
import json
import xlsxwriter
import pandas as pd
import csv

#Setting Arrays and dict for data storage (data = pose final coordinates; BotCoord = all coordinates at an instance)
pose_data_0={"barista_0_pose":list()}
pose_data_1={"barista_1_pose":list()}
pose_data_2={"barista_2_pose":list()}
pose_data_3={"barista_3_pose":list()}
bot_0_coord = [[],[],[],[]]
bot_1_coord = [[],[],[],[]]
bot_2_coord = [[],[],[],[]]
bot_3_coord = [[],[],[],[]]

class PoseSubscriber(Node):
   
    #Subsriber function 
    def __init__(self):
        super().__init__("Pose_subscriber")
        self.subscription_P0 = self.create_subscription(PoseWithCovarianceStamped,'/barista_0/amcl_pose',self.callback_0,10)
        self.subscription_P1 = self.create_subscription(PoseWithCovarianceStamped,'/barista_1/amcl_pose',self.callback_1,10)
        self.subscription_P2 = self.create_subscription(PoseWithCovarianceStamped,'/barista_2/amcl_pose',self.callback_2,10)
        self.subscription_P3 = self.create_subscription(PoseWithCovarianceStamped,'/barista_3/amcl_pose',self.callback_3,10)
        self.subscription_G0 = self.create_subscription(String,'/barista_0/goal_status',self.goal_callback_0,10)
        self.subscription_G1 = self.create_subscription(String,'/barista_1/goal_status',self.goal_callback_1,10)
        self.subscription_G2 = self.create_subscription(String,'/barista_2/goal_status',self.goal_callback_2,10)
        self.subscription_G3 = self.create_subscription(String,'/barista_3/goal_status',self.goal_callback_3,10)
        self.get_logger().info("Barista_Pose IS READY")

# fetching Coordinates    
    def callback_0(self, pose:PoseWithCovarianceStamped):
        global _x0
        global _y0
        global _theta0
        time0 = pose.header.stamp.sec
        _x0=pose.pose.pose.position.x
        _y0=pose.pose.pose.position.y
        rot_q = pose.pose.pose.orientation
        (roll, pitch, _theta0) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])  
        self.get_logger().info("(" + str(_x0) + " X " + str(_y0) + ")" + str(_theta0) + "barista_0")
        bot_0_coord[0].append(_x0);bot_0_coord[1].append(_y0);bot_0_coord[2].append(_theta0);bot_0_coord[3].append(time0)
        
    def callback_1(self, pose:PoseWithCovarianceStamped):
        global _x1
        global _y1
        global _theta1 
        time1 = pose.header.stamp.sec
        _x1=pose.pose.pose.position.x
        _y1=pose.pose.pose.position.y
        rot_q = pose.pose.pose.orientation
        (roll, pitch, _theta1) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])  
        self.get_logger().info("(" + str(_x1) + " X " + str(_y1) + ")" + str(_theta1) + "barista_1")
        bot_1_coord[0].append(_x1);bot_1_coord[1].append(_y1);bot_1_coord[2].append(_theta1);bot_1_coord[3].append(time1)
        

    def callback_2(self, pose:PoseWithCovarianceStamped):
        global _x2
        global _y2
        global _theta2
        time2 = pose.header.stamp.sec
        _x2=pose.pose.pose.position.x
        _y2=pose.pose.pose.position.y
        rot_q = pose.pose.pose.orientation
        (roll, pitch, _theta2) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])  
        self.get_logger().info("(" + str(_x2) + " X " + str(_y2) + ")" + str(_theta2) + "barista_2")
        bot_2_coord[0].append(_x2);bot_2_coord[1].append(_y2);bot_2_coord[2].append(_theta2);bot_2_coord[3].append(time2)

    def callback_3(self, pose:PoseWithCovarianceStamped):
        global _x3
        global _y3
        global _theta3
        time3 = pose.header.stamp.sec
        _x3=pose.pose.pose.position.x
        _y3=pose.pose.pose.position.y
        rot_q = pose.pose.pose.orientation
        (roll, pitch, _theta3) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])  
        self.get_logger().info("(" + str(_x3) + " X " + str(_y3) + ")" + str(_theta3) + "barista_3")
        bot_3_coord[0].append(_x3);bot_3_coord[1].append(_y3);bot_3_coord[2].append(_theta3);bot_3_coord[3].append(time3)

#fetching last coordinates after successfully reaching goal

    def goal_callback_0(self, goal:String):
        msg= goal.data
        if msg==('goal_reached'):
            self.get_logger().info("barista_0 reached goal")
            pose_data_0["barista_0_pose"].append({"x":_x0, "y":_y0, "theta":_theta0})
    
    def goal_callback_1(self, goal:String):
        msg= goal.data
        if msg==('goal_reached'):
            self.get_logger().info("barista_1 reached goal")
            pose_data_1["barista_1_pose"].append({"x":_x1, "y":_y1, "theta":_theta1})

    def goal_callback_2(self, goal:String):
        msg= goal.data
        if msg==('goal_reached'):
            self.get_logger().info("barista_2 reached goal")
            pose_data_2["barista_2_pose"].append({"x":_x2, "y":_y2, "theta":_theta2})

    def goal_callback_3(self, goal:String):
        msg= goal.data
        if msg==('goal_reached'):
            self.get_logger().info("barista_3 reached goal")
            pose_data_3["barista_3_pose"].append({"x":_x3, "y":_y3, "theta":_theta3})


#Writing json and csv files
    def final_data():
        final_pose_data=[pose_data_0,pose_data_1,pose_data_2,pose_data_3]
        with open(current_path + '/json/Poses.json', "w") as output:
            json.dump(final_pose_data, output, sort_keys=True) 
        bot_coordinates=[]
        bot_coordinates.append([bot_0_coord]+[bot_1_coord]+[bot_2_coord]+[bot_3_coord])
        for i in range(4):
            with open(current_path + '/csv/Robot'+ str(i) + '.csv', 'w', newline='')as f:
                field_names= ['X','Y','Theta','Timestamp']
                writer = csv.DictWriter(f, fieldnames=field_names)
                writer.writeheader()
                length = len(bot_coordinates[0][i][0])
                for j in range(length):
                    writer.writerow({'X':bot_coordinates[0][i][0][j],'Y':bot_coordinates[0][i][1][j],'Theta':bot_coordinates[0][i][2][j],'Timestamp':bot_coordinates[0][i][3][j]})




def main(args=None):
    rclpy.init(args=args)
    try: 
        node = PoseSubscriber()
        rclpy.spin(node)
    except KeyboardInterrupt: 
        rclpy.shutdown()  
    
    


if __name__ == '__main__':
    main()
