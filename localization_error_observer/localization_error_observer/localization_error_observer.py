import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Bool
from rclpy.executors import SingleThreadedExecutor
from rcl_interfaces.msg import ParameterDescriptor, ParameterValue
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import atan2
from itertools import groupby
from matplotlib.lines import Line2D
from itertools import cycle, groupby, islice
import sys
import csv


class LocalizationError(Node):
    """Module subscribes to the amcl pose,  Goal pose
    and calculates the delta between them
    Args:
        Node (rclpy.node): rclpy node
    """

    def __init__(self, arg, robot_id):
        super().__init__('localization_error_observer_'+str(robot_id))
        # parameter : number of goals = iterations
        #my_parameter_descriptor = ParameterDescriptor(description='Number of Iterations')
        self.iterations = int(arg)
        print(self.iterations)
        self.raw_x = []
        self.raw_y = []
        self.raw_theta = []
        self.x_position = []
        self.y_position = []
        self.theta_position = []
        self.goal_position_x = []
        self.goal_position_y = []
        self.goal_position_theta = []
        self.i = 1
        self.delta_dictionary = {}
        self.delta_dictionary["x"] = []
        self.delta_dictionary["y"] = []
        self.delta_dictionary["theta"] = []
        self.data = []
        self.robot_number = str(robot_id)
        # generate x_axis
        self.index = np.arange(1, int(self.iterations)+1, dtype=int)
        self.coordinates = ["x", "y", "\u03F4"]
        self.x_axis = []
        for x in self.index:
            for val in self.coordinates:
                self.x_axis.append(val + str(x))

        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            'barista_'+str(robot_id)+'/amcl_pose',
            self.robot_agent_amcl_callback,
            10)
        self.subscription
        self.subscription2 = self.create_subscription(
            PoseStamped,
            'barista_'+str(robot_id)+'/send_pose',
            self.robot_agent_goal_callback,
            10)
        self.subscription2
        self.subscription3 = self.create_subscription(
            Bool,
            '/barista_'+str(robot_id)+'/goal_status',
            self.status_check,
            10)
        self.subscription3

    def robot_agent_amcl_callback(self, msg):
        """callback to the amcl_pose subsriber

        Args:
            msg (PoseWithCovarianceStamped): AMCL pose of the robot agent
        """        """"""
        self.x_position.append(msg.pose.pose.position.x)
        self.y_position.append(msg.pose.pose.position.y)

        t3 = +2.0 * (msg.pose.pose.orientation.w * msg.pose.pose.orientation.z +
                     msg.pose.pose.orientation.x * msg.pose.pose.orientation.y)
        t4 = +1.0 - 2.0 * (msg.pose.pose.orientation.y * msg.pose.pose.orientation.y +
                           msg.pose.pose.orientation.z * msg.pose.pose.orientation.z)
        yaw = atan2(t3, t4)
        self.theta_position.append(yaw)

    def robot_agent_goal_callback(self, msg):
        """Callback to the robot agent requested Goal pose

        Args:
            msg (PoseStamped): Goal pose send to the robot agent
        """
        self.goal_position_x.append(msg.pose.position.x)

        self.goal_position_y.append(msg.pose.position.y)
        t3 = +2.0 * (msg.pose.orientation.w * msg.pose.orientation.z +
                     msg.pose.orientation.x * msg.pose.orientation.y)
        t4 = +1.0 - 2.0 * (msg.pose.orientation.y * msg.pose.orientation.y +
                           msg.pose.orientation.z * msg.pose.orientation.z)
        yaw = atan2(t3, t4)
        self.goal_position_theta.append(yaw)

    def status_check(self, msg):
        """Checking wheather the robot has completed the navigation to Goal

        Args:
            msg (String): goal status message
        """
        if msg.data == True:
            print("stopped")

            self.delta_x = round(
                float(self.goal_position_x[-1]) - float(self.x_position[-1]), 5)
            self.raw_x.append(self.x_position[-1])
            self.delta_y = round(
                float(self.goal_position_y[-1]) - float(self.y_position[-1]), 5)
            self.raw_y.append(self.y_position[-1])
            # convert the quaternion to angle
            self.delta_theta = round(
                float(self.goal_position_theta[-1]) - float(self.theta_position[-1]), 5)
            self.raw_theta.append(self.theta_position[-1])
            print("delta_x : ", self.delta_x, "delta_y : ", self.delta_y, "delta_theta : ",
                  self.delta_theta)
            self.update_robot_agent(
                self.delta_x, self.delta_y, self.delta_theta)

    def update_robot_agent(self, x, y, t):
        """_summary_

        Args:
            x (float): x axis in cm
            y (float): y axis in cm
            t (float): theta in radians

        Returns:
            _type_: create a dictionary with the delta pose
        """
        self.delta_dictionary["x"].append(x)
        self.delta_dictionary["y"].append(y)
        self.delta_dictionary["theta"].append(t)
        self.robot_agent_delta_dictionary = self.delta_dictionary
        
        
        if self.i == self.iterations:
            for i in range(0, self.iterations):
                self.data.append(self.delta_dictionary["x"][i])
                self.data.append(self.delta_dictionary["y"][i])
                self.data.append(self.delta_dictionary["theta"][i])
            print(self.data)
            list = []
            final_list = []
            for i in range(1, int(self.iterations)+1):
                list.append([i]*3)
            for sub in list:
                for val in sub:
                    final_list.append(val)
            # print(final_list)
            df = pd.DataFrame({'Name': self.x_axis,
                               'TEST_Name': final_list,
                               'Label': ['Median']*(3*self.iterations),
                               'Data': self.data})
            df = df.set_index(['TEST_Name', 'Name'])['Data']  # .unstack()
            # print(df)
            df.to_csv('experiment' + self.robot_number + '.csv')
            # Save raw data
            self.raw_dict = {"amcl_x": self.raw_x, "amcl_y": self.raw_y, "amcl_theta": self.raw_theta,
                                "goal_x":self.goal_position_x, "goal_y":self.goal_position_y, "goal_theta":self.goal_position_theta}
            self.raw_df = pd.DataFrame(self.raw_dict) 
            self.raw_df.to_csv('raw_data' + self.robot_number + '.csv')
            self.get_logger().info("Data collection Experiment completed data has been stored in workspace home ctrl+c to end the experiment")
            

        self.i += 1
        print(self.robot_agent_delta_dictionary)

            # comment from this block if only csv is required
'''
            def add_line(ax, xpos, ypos):
                line = plt.Line2D([xpos, xpos], [ypos + .1, ypos],
                                  transform=ax.transAxes, color='gray')
                line.set_clip_on(False)
                ax.add_line(line)

            def label_len(my_index, level):
                labels = my_index.get_level_values(level)
                return [(k, sum(1 for i in g)) for k, g in groupby(labels)]

            def label_group_bar_table(ax, df):
                ypos = -.1
                scale = 1./df.index.size
                # print(range(df.index.nlevels)[::-1])
                for level in range(df.index.nlevels)[::-1]:
                    pos = 0
                    for label, rpos in label_len(df.index, level):
                        lxpos = (pos + .5 * rpos)*scale
                        print(label)
                        ax.text(lxpos, ypos, label, ha='center',
                                transform=ax.transAxes)
                        add_line(ax, pos*scale, ypos)
                        pos += rpos
                    add_line(ax, pos*scale, ypos)
                    ypos -= .1

            # print(df)
            # ax = df.plot(marker='o', linestyle='none',)#, xlim=(-.5,11.5))
            color_list = []
            my_colors = islice(cycle(['b', 'r', 'g']), None, 45)
            for item in my_colors:
                color_list.append(item)

            fig, ax = plt.subplots(1)

            # x-axis
            x_list = np.arange(1, 46).tolist()
            # create axis
            ax.scatter(x_list, df.values, c=color_list)
            # Below 2 lines remove default labels
            plt.yticks(np.arange(df.values.min(), df.values.max(), 0.5))
            plt.xlim(0.5, 45.5)
            ax.set_xticklabels('')
            ax.set_xlabel('')

            # add x-axis values
            label_group_bar_table(ax, df)

            # add legend
            legend_elements = [Line2D([0], [0], marker='o', color='b', label='x',
                                      markerfacecolor='b', markersize=8),
                               Line2D([0], [0], marker='o', color='r', label='y',
                                      markerfacecolor='r', markersize=8),
                               Line2D([0], [0], marker='o', color='g', label='\u03F4',
                                      markerfacecolor='g', markersize=8)]

            ax.legend(handles=legend_elements, loc='upper left')

            # add grids
            ax.minorticks_on()
            ax.grid(which='major', linestyle='-', linewidth='0.5')
            ax.grid(which='minor', linestyle='-', linewidth='0.5')

            # add labels
            ax.set_xlabel('Iterations')
            ax.set_ylabel('Error in cm')
            ax.xaxis.set_label_coords(.5, -.3)
            plt.tight_layout()
            plt.show()
'''




def main(args=None):
    rclpy.init(args=args)
    try:
        error_subscriber_0 = LocalizationError(sys.argv[1], robot_id=0)
        error_subscriber_1 = LocalizationError(sys.argv[1], robot_id=1)
        error_subscriber_2 = LocalizationError(sys.argv[1], robot_id=2)
        error_subscriber_3 = LocalizationError(sys.argv[1], robot_id=3)
        executor = SingleThreadedExecutor()

        executor.add_node(error_subscriber_0)
        executor.add_node(error_subscriber_1)
        executor.add_node(error_subscriber_2)
        executor.add_node(error_subscriber_3)
        try:
            executor.spin()
        finally:
            executor.destroy_node()
    
    except KeyboardInterrupt:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
