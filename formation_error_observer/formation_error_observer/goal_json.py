#!/usr/bin/env python3
#Current path witten using utils.py
current_path = "/home/janavi/swarmbot2/src/formation_error_observer/data" 
import rclpy
from geometry_msgs.msg import PoseStamped
from math import atan2
from tf_transformations import euler_from_quaternion
from rclpy.node import Node
import json

#Setting Arrays and dict for data storage (data = goal final coordinates)
goal_data_0={"barista_0_goal":list()}
goal_data_1={"barista_1_goal":list()}
goal_data_2={"barista_2_goal":list()}
goal_data_3={"barista_3_goal":list()}

class GoalSubscriber(Node):
   
    def __init__(self):
        super().__init__("Goal_subscriber")
        self.subscription = self.create_subscription(PoseStamped,'/barista_0/send_pose',self.callback_0,10)
        self.subscription = self.create_subscription(PoseStamped,'/barista_1/send_pose',self.callback_1,10)
        self.subscription = self.create_subscription(PoseStamped,'/barista_2/send_pose',self.callback_2,10)
        self.subscription = self.create_subscription(PoseStamped,'/barista_3/send_pose',self.callback_3,10)

        self.get_logger().info("Barista_Goal IS READY")


# fetching Coordinates 
    def callback_0(self, pose:PoseStamped):
        x=pose.pose.position.x
        y=pose.pose.position.y
        rot_q = pose.pose.orientation
        (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])  
        self.get_logger().info("(" + str(x) + " X " + str(y) + ")" + str(theta))
        goal_data_0["barista_0_goal"].append({"x":x, "y":y, "theta":theta})
        
    def callback_1(self, pose:PoseStamped):
        x=pose.pose.position.x
        y=pose.pose.position.y
        rot_q = pose.pose.orientation
        (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])  
        self.get_logger().info("(" + str(x) + " X " + str(y) + ")" + str(theta))
        goal_data_1["barista_1_goal"].append({"x":x, "y":y, "theta":theta})
        
    def callback_2(self, pose:PoseStamped):
        x=pose.pose.position.x
        y=pose.pose.position.y
        rot_q = pose.pose.orientation
        (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])  
        self.get_logger().info("(" + str(x) + " X " + str(y) + ")" + str(theta))
        goal_data_2["barista_2_goal"].append({"x":x, "y":y, "theta":theta})
        
    def callback_3(self, pose:PoseStamped):
        x=pose.pose.position.x
        y=pose.pose.position.y
        rot_q = pose.pose.orientation
        (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])  
        self.get_logger().info("(" + str(x) + " X " + str(y) + ")" + str(theta))
        goal_data_3["barista_3_goal"].append({"x":x, "y":y, "theta":theta})


# Creating Json files
    def final_data():
        with open(current_path + '/json/Goals.json', "w") as output:
            final_goal_data=[goal_data_0,goal_data_1,goal_data_2,goal_data_3]
            json.dump(final_goal_data, output, sort_keys=True)
          

        


def main(args=None):
    rclpy.init(args=args)
    try: 
        node = GoalSubscriber()
        rclpy.spin(node)
    except KeyboardInterrupt: 
        

        rclpy.shutdown()
    


if __name__ == '__main__':
    main()
