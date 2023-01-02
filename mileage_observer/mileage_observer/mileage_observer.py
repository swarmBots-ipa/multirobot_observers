#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class MileageObserver(Node):
   
    def __init__(self):
        super().__init__("mileage_observer")
        pass

def main(args=None):
    rclpy.init(args=args)
    try: 
        node = MileageObserver()
        rclpy.spin(node)
    except KeyboardInterrupt: 
        rclpy.shutdown()
    

if __name__ == '__main__':
    main()
