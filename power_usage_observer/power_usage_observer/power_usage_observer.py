#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import BatteryState
import csv
import sys
import os
from rclpy.executors import SingleThreadedExecutor

#Global Variables,
#Creating empty arrays to store data based on no. of bots
no_of_bots = int(sys.argv[1])

time_array = []
voltage_array = []
current_array = []
temperature_array = []
charge_percentage_array = []
for n in range(no_of_bots):
    time_array.append([])
    voltage_array.append([])
    current_array.append([])
    temperature_array.append([])
    charge_percentage_array.append([])

#Creating and assigning paths
filename = os.path.basename(__file__)
search_dir = '/home/'
for root, dirs, files in os.walk(search_dir):
    if filename in files:
        file_location = os.path.join(root, filename)
       # print(file_location)
        break
path = file_location.replace('power_usage_observer/'+filename,'data')
csv_path = path + "/csv/Robot"
csv_folder= path+"/csv"
graph_folder = path+"/graphs"

#Clearing old Data
def clear_old_data(folder_path):
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)
clear_old_data(csv_folder)
clear_old_data(graph_folder)


class PowerUsageObserver(Node):
   #Subscribing topics
    def __init__(self,robot_id):
        super().__init__("power_usage_observer_"+str(robot_id))
        self.get_logger().info("power usage observer "+str(robot_id) +" ready")
        self.subscription3 = self.create_subscription(BatteryState,'/battery_state',self.callback,10)
        self.robot_id = robot_id
        pass
    
    #Frtching current, voltage, temperaure,time, and chhhhharge percentage
    def callback(self, data:BatteryState):
        time = data.header._stamp.sec
        voltage = data.voltage
        current = data.current
        temperature = data.temperature
        charge_percentage = data.percentage
        time_array[self.robot_id].append(time)
        voltage_array[self.robot_id].append(voltage)
        current_array[self.robot_id].append(current)
        temperature_array[self.robot_id].append(temperature)
        charge_percentage_array[self.robot_id].append(charge_percentage)
        self.get_logger().info("vtg = "+str(voltage) + " current =" +str(current) + " temp =" + str(temperature) + " percent = " + str(charge_percentage) + " time = " + str(time))
        self.csv_data()
    
    #Storing values into a csv
    def csv_data(self):
        for i in range(no_of_bots):
            with open( csv_path + str(i) + '.csv', 'w', newline='')as f:
                field_names= ['time','voltage','current','temperature','charge_percentage']
                writer = csv.DictWriter(f, fieldnames=field_names)
                writer.writeheader()
                length = len(voltage_array[i])
               # print(voltage_array)
                for j in range(length):
                    writer.writerow({'time':time_array[i][j],'voltage':voltage_array[i][j],'current':current_array[i][j],'temperature':temperature_array[i][j],'charge_percentage':charge_percentage_array[i][j]})   

    
