#! /usr/bin/env python3

import rclpy
from rclpy.executors import SingleThreadedExecutor
from multirobot_observers.mileage_observer.mileage_observer.path_observer import PathObserver
from mileage_observer.mileage_observer import MileageObserver
from multirobot_observers.mileage_observer.mileage_observer.mileage_observer_plotter import MileageObserverPlotter



import sys
nodes =[]
mileage_subscribers=[]
def main(args=None):

    rclpy.init(args=args)
    try:
        for i in range(4):
            node = PathObserver(sys.argv[1],robot_id=i)
            nodes.append(node)
            mileage_subscriber = MileageObserver(sys.argv[1],robot_id=i) 
            mileage_subscribers.append(mileage_subscriber)

        #node_0= PathObserver(sys.argv[1],robot_id=0)
        #node_1= PathObserver(sys.argv[1],robot_id=1)
        #node_2= PathObserver(sys.argv[1],robot_id=2)
        #node_3= PathObserver(sys.argv[1],robot_id=3)
        #mileage_subscriber_0 = MileageObserver(sys.argv[1],robot_id=0) 
        #mileage_subscriber_1 = MileageObserver(sys.argv[1],robot_id=1)
        #mileage_subscriber_2 = MileageObserver(sys.argv[1],robot_id=2)
        #mileage_subscriber_3 = MileageObserver(sys.argv[1],robot_id=3)

        for node in nodes:
            executor = SingleThreadedExecutor()
            executor.add_node(node)
            executor.spin()
        for mileage_subscriber in mileage_subscribers:
            executor = SingleThreadedExecutor()    
            executor.add_node(mileage_subscriber)
            executor.spin()
        #executor = SingleThreadedExecutor()
        #executor.add_node(node_0)
        #executor.add_node(node_1)
        #executor.add_node(node_2)
        #executor.add_node(node_3)
        #executor.add_node(mileage_subscriber_0)
        #executor.add_node(mileage_subscriber_1)
        #executor.add_node(mileage_subscriber_2)
        #executor.add_node(mileage_subscriber_3)
        #executor.spin()
        
    except KeyboardInterrupt:
        #For writing data into json and csv files
        actual_path_length = PathObserver.final_data()
        path_travelled =  MileageObserver.final_data()
        print(actual_path_length)
        print(path_travelled)
        MileageObserverPlotter.mileage_path_graph(path_travelled,actual_path_length)
        executor.shutdown()


if __name__ == '__main__':
    main()

