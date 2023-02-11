#! /usr/bin/env python3

import rclpy
from rclpy.executors import SingleThreadedExecutor
from mileage_observer.distance_calculator import PathDistance
from mileage_observer.mileage_observer import MileageObserver
from mileage_observer.graph_plotter import MileageObserverPlotter



import sys

def main(args=None):

    rclpy.init(args=args)
    try:
        node_0= PathDistance(sys.argv[1],robot_id=0)
        node_1= PathDistance(sys.argv[1],robot_id=1)
        node_2= PathDistance(sys.argv[1],robot_id=2)
        node_3= PathDistance(sys.argv[1],robot_id=3)
        mileage_subscriber_0 = MileageObserver(sys.argv[1],robot_id=0) 
        mileage_subscriber_1 = MileageObserver(sys.argv[1],robot_id=1)
        mileage_subscriber_2 = MileageObserver(sys.argv[1],robot_id=2)
        mileage_subscriber_3 = MileageObserver(sys.argv[1],robot_id=3)
        executor = SingleThreadedExecutor()
        executor.add_node(node_0)
        executor.add_node(node_1)
        executor.add_node(node_2)
        executor.add_node(node_3)
        executor.add_node(mileage_subscriber_0)
        executor.add_node(mileage_subscriber_1)
        executor.add_node(mileage_subscriber_2)
        executor.add_node(mileage_subscriber_3)
        executor.spin()
        
    except KeyboardInterrupt:
        #For writing data into json and csv files
        path_arr = PathDistance.final_data()
        mil_arr =  MileageObserver.final_data()
        print(path_arr)
        print(mil_arr)
        MileageObserverPlotter.mil_path_graph(mil_arr,path_arr)
        executor.shutdown()


if __name__ == '__main__':
    main()

