#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import BatteryState
import numpy as nmpi
from influxdb import InfluxDBClient
import datetime
import sys
from rclpy.executors import SingleThreadedExecutor
from tabulate import tabulate
from power_usage_observer.influxQuery import influxQueries

client = InfluxDBClient(host='localhost',port = 8086)
client.create_database('powerdb')
client.get_list_database()
client.switch_database('powerdb')
influxdata =[]

def payload(robot_id, voltage, current, temperature, charge):
    
    payload = {

            "measurement": "powerdata_"+str(robot_id),
            #"tags": { "host": "server1"},
            "time": datetime.datetime.now(),
            "fields": {'voltage': voltage, 'current': current,'temperature': temperature,'charge percentage': charge}
        }
    return payload




class PowerUsageObserver(Node):
   #Subscribing topics
    def __init__(self,robot_id=0):
        super().__init__("power_usage_observer_"+str(robot_id))
        self.get_logger().info("power usage observer "+str(robot_id) +" ready")
        self.subscription = self.create_subscription(BatteryState,'/battery_state',self.callback,10)
        self.robot_id = robot_id
        pass
    
    #Fetching current, voltage, temperaure,time, and charge percentage
    def callback(self, data:BatteryState):
        time = data.header._stamp.sec
        voltage = data.voltage
        current = data.current
        temperature = data.temperature
        charge_percentage = data.percentage

        updated_payload=payload(self.robot_id, nmpi.round(float(voltage),3), nmpi.round(float(current),3), nmpi.round(float(temperature),3), nmpi.round(float(charge_percentage),3))
        influxdata.append(updated_payload)
        self.get_logger().info("vtg = "+str(voltage) + " current =" +str(current) + " temp =" + str(temperature) + " percent = " + str(charge_percentage) + " time = " + str(time))
        
        client.write_points(influxdata, time_precision='s')
    
    
    

nodes = []
def main(args=None):
    agents = int(sys.argv[1])
    rclpy.init(args=args)
    try: 
        for i in range(agents):
         power_node = PowerUsageObserver(robot_id = i)
         nodes.append(power_node)
         global executor
        executor = SingleThreadedExecutor()
        for node in nodes:
            executor.add_node(node)
            
        executor.spin() 
    

    except KeyboardInterrupt:
        influxQueries(agents)
        executor.shutdown()



if __name__ == '__main__':
    main()