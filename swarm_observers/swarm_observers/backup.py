import rclpy
from rclpy.node import Node

from lifecycle_msgs.msg import TransitionEvent
from std_msgs.msg import String
from nav2_msgs.msg import BehaviorTreeStatusChange  
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
import numpy as np
import matplotlib.pyplot as plt
from math import atan2
class localization_error(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.x_position = []
        self.y_position = []    
        #self.z_position = [] 
        #self.w_position = [] 
        self.theta_position = []
        self.goal_position_x = []
        self.goal_position_y = []
        #self.goal_position_z = []
        #self.goal_position_w = []
        self.goal_position_theta = []
        self.i=1
        self.delta_dictionary = {}
        self.delta_dictionary["x"] = []
        self.delta_dictionary["y"] = []
        #self.delta_dictionary["z"] = []
        #self.delta_dictionary["w"] = []
        self.delta_dictionary["theta"] = []
        self.index = np.arange(1, 4, dtype=int)
        self.coordinates = ["x","z","\u03A9"]
        for x in self.index:
            for val in self.coordinates:
                val = val + x
    
        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            'barista_0/amcl_pose',
            self.barista_0_amcl_callback,
            10)
        self.subscription  
        self.subscription2 = self.create_subscription(
            PoseStamped,
            'barista_0/goal_pose',
            self.barista_0_goal_callback,
            10)
        self.subscription2
        self.subscription3 = self.create_subscription(
            Twist,    
            '/barista_0/cmd_vel',
            self.status_check,
            10) 
        self.subscription3
        """         
        self.subscription3 = self.create_subscription(
            PoseWithCovarianceStamped,
            'barista_1/amcl_pose',
            self.barista_1_amcl_callback,
            10)
        self.subscription3  
        self.subscription4 = self.create_subscription(
            PoseStamped,
            'barista_1/goal_pose',
            self.self.barista_1_goal_callback,
            10)
        self.subscription4
        self.subscription5 = self.create_subscription(
            PoseWithCovarianceStamped,
            'barista_2/amcl_pose',
            self.barista_2_amcl_callback,
            10)
        self.subscription5  
        self.subscription6 = self.create_subscription(
            PoseStamped,
            'barista_2/goal_pose',
            self.barista_1_goal_callback,
            10)
        self.subscription6
        self.subscription7 = self.create_subscription(
            PoseWithCovarianceStamped,
            'barista_1/amcl_pose',
            self.barista_3_amcl_callback,
            10)
        self.subscription7  
        self.subscription8 = self.create_subscription(
            PoseStamped,
            'barista_1/goal_pose',
            self.barista_3_goal_callback,
            10)
        self.subscription8
        """
    def barista_0_amcl_callback(self, msg):          
        self.x_position.append(msg.pose.pose.position.x)
         
        self.y_position.append(msg.pose.pose.position.y)

        t3 = +2.0 * (msg.pose.pose.orientation.w * msg.pose.pose.orientation.z +
                    msg.pose.pose.orientation.x * msg.pose.pose.orientation.y)
        t4 = +1.0 - 2.0 * (msg.pose.pose.orientation.y * msg.pose.pose.orientation.y +
                           msg.pose.pose.orientation.z * msg.pose.pose.orientation.z)
        yaw = atan2(t3, t4) 
        #self.x_orientation_position.append(msg.pose.pose.orientation.x)

        #self.y_orientation_position.append(msg.pose.pose.orientation.y)   
        self.theta_position.append(yaw)
        #self.z_position.append(msg.pose.pose.orientation.z)
        #self.w_position.append(msg.pose.pose.orientation.w)
    def barista_0_goal_callback(self, msg):
        self.goal_position_x.append(msg.pose.position.x)
         
        self.goal_position_y.append(msg.pose.position.y)
        t3 = +2.0 * (msg.pose.orientation.w * msg.pose.orientation.z +
                    msg.pose.orientation.x * msg.pose.orientation.y)
        t4 = +1.0 - 2.0 * (msg.pose.orientation.y * msg.pose.orientation.y +
                           msg.pose.orientation.z * msg.pose.orientation.z)
        yaw = atan2(t3, t4)
        self.goal_position_theta.append(yaw)
        #self.goal_position_z.append(msg.pose.orientation.z)
          
        #self.goal_position_w.append(msg.pose.orientation.w)
    
    def status_check(self, msg):
        if msg.linear.x == 0 and msg.angular.z == 0:
            print("stopped")
            self.delta_x = round(float(self.goal_position_x[0]) - float(self.x_position[-1]) ,5)
            self.delta_y = round(float(self.goal_position_y[0]) - float(self.y_position[-1]) ,5)

                # convert the quaternion to angle
            self.delta_theta = round(float(self.goal_position_theta[0]) - float(self.theta_position[-1]) ,5)
            #self.delta_z = round(float(self.goal_position_z[0]) - float(self.y_position[-1]) ,5)
            #self.delta_w = round(float(self.goal_position_w[0]) - float(self.y_position[-1]) ,5)
            print("delta_x : ", self.delta_x, "delta_y : ", self.delta_y, "delta_theta : ", self.delta_theta) #self.delta_z, "delta_w : ", self.delta_w)
            self.update_barista_0(self.delta_x, self.delta_y, self.delta_theta)#self.delta_z, self.delta_w)

    
    def update_barista_0(self, x,y,t):
        self.delta_dictionary["x"].append(x)
        self.delta_dictionary["y"].append(y)
        self.delta_dictionary["theta"].append(t)
        #self.delta_dictionary["z"].append(z)
        #self.delta_dictionary["w"].append(w)
        self.barista_0_delta_dictionary = self.delta_dictionary
        if self.i == 3:
            fig, axs = plt.subplots(2, 1)
            axs[0, 0].plot(self.index, self.barista_0_delta_dictionary["x"])
            axs[0, 0].set_title('Axis x')
            axs[0, 1].plot(self.index, self.barista_0_delta_dictionary["y"], 'tab:orange')
            axs[0, 1].set_title('Axis y')
            axs[1, 0].plot(self.index, self.barista_0_delta_dictionary["theta"], 'tab:green')
            axs[1, 0].set_title('Axis t')
        #    axs[1, 1].plot(self.index, self.barista_0_delta_dictionary["w"], 'tab:red')
        #    axs[1, 1].set_title('Axis w')

            for ax in axs.flat:
                ax.set(xlabel='x-label', ylabel='y-label')


            for ax in axs.flat:
                ax.label_outer()
            plt.show()
        self.i += 1
        print(self.barista_0_delta_dictionary)


            
            

             




def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = localization_error()

    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()