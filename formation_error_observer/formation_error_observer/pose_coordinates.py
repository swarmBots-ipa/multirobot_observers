#!/usr/bin/env python3


from geometry_msgs.msg import PoseWithCovarianceStamped
from std_msgs.msg import String
from math import atan2
from tf_transformations import euler_from_quaternion
from rclpy.node import Node
import json
import csv
from formation_error_observer.goal_coordinates import GoalSubscriber


#Setting Arrays and dict for data storage (data = pose final coordinates; BotCoord = all coordinates at an instance)
pose_data={"barista_0_pose":list(), "barista_1_pose":list(), "barista_2_pose":list(), "barista_3_pose":list()}
bot_coord = [[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]]




class PoseSubscriber(Node):
   
    #Subscriber function 
    
    def __init__(self,arg,robot_id):
    
        # for i in range(no_of_bots):
        super().__init__("Pose_subscriber")
        self.subscription = self.create_subscription(PoseWithCovarianceStamped,'/barista_'+str(robot_id)+'/amcl_pose',self.callback,10)    
        self.subscription2 = self.create_subscription(String,'/barista_'+str(robot_id)+'/goal_status',self.goal_callback,10)
        self.robot_id = robot_id
        self.i = 0
        self.iteration = int(arg)
        self.get_logger().info("Barista_Pose IS READY")

# fetching Coordinates    
    def callback(self, pose:PoseWithCovarianceStamped):
        self.time = pose.header.stamp.sec
        self._x=pose.pose.pose.position.x
        self._y=pose.pose.pose.position.y
        self.rot_q = pose.pose.pose.orientation
        (roll, pitch, self._theta) = euler_from_quaternion([self.rot_q.x, self.rot_q.y, self.rot_q.z, self.rot_q.w])  
        self.get_logger().info("(" + str(self._x) + " X " + str(self._y) + ")" + str(self._theta) + "barista_"+str(self.robot_id))
        i=self.robot_id
        bot_coord[i][0].append(self._x);bot_coord[i][1].append(self._y);bot_coord[i][2].append(self._theta);bot_coord[i][3].append(self.time)
        
    
#fetching last coordinates after successfully reaching goal

    def goal_callback(self,goal:String):
        msg= goal.data
        if msg==('goal_reached'):
            self.get_logger().info("barista_"+str(self.robot_id)+"reached goal")
            pose_data["barista_"+str(self.robot_id)+"_pose"].append({"x":self._x, "y":self._y, "theta":self._theta})
        self.iteration_counter()

    def iteration_counter(self):
        
        self.i += 1
        self.get_logger().info("Iteration " + str(self.i) + " completed for bot_" + str(self.robot_id))
        if self.i==self.iteration:
                PoseSubscriber.final_data()
                GoalSubscriber.final_data()
                self.get_logger().info("This is Final Iteration for bot_" + str(self.robot_id))
         

#Writing json and csv files
    def final_data():
        final_pose_data=[pose_data]
        with open('../data/json/Poses.json', "w") as output:
            json.dump(final_pose_data, output, sort_keys=True) 
        bot_coordinates=[]
        bot_coordinates.append(bot_coord)
        for i in range(4):
            with open('../data/csv/Robot'+ str(i) + '.csv', 'w', newline='')as f:
                field_names= ['X','Y','Theta','Timestamp']
                writer = csv.DictWriter(f, fieldnames=field_names)
                writer.writeheader()
                length = len(bot_coordinates[0][i][0])
                for j in range(length):
                    writer.writerow({'X':bot_coordinates[0][i][0][j],'Y':bot_coordinates[0][i][1][j],'Theta':bot_coordinates[0][i][2][j],'Timestamp':bot_coordinates[0][i][3][j]})



