#! /usr/bin/env python3

import rclpy
from rclpy.executors import SingleThreadedExecutor
from mileage_observer.path_observer import PathDistance
from mileage_observer.mileage_observer import MileageObserver
from mileage_observer.mileage_observer_plotter import MileageObserverPlotter
import sys


nodes =[]
mileage_subscribers=[]
def main(args=None):
    agents=int(sys.argv[2])
    rclpy.init(args=args)
    try:
        for i in range(agents):
            node = PathDistance(sys.argv[1],robot_id=i)
            nodes.append(node)
            mileage_subscriber = MileageObserver(sys.argv[1],robot_id=i) 
            mileage_subscribers.append(mileage_subscriber)

        for node in nodes:
            executor = SingleThreadedExecutor()
            executor.add_node(node)
            executor.spin()
        for mileage_subscriber in mileage_subscribers:
            executor = SingleThreadedExecutor()    
            executor.add_node(mileage_subscriber)
            executor.spin()

        
    except KeyboardInterrupt:
        #For writing data into json and csv files
        actual_path_length = PathDistance.final_data()
        path_travelled =  MileageObserver.final_data()
        print(actual_path_length)
        print(path_travelled)
        MileageObserverPlotter.mileage_path_graph(path_travelled,actual_path_length)
        executor.shutdown()


if __name__ == '__main__':
    main()

