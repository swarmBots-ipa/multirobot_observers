#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class PowerUsageObserver(Node):
   
    def __init__(self):
        super().__init__("power_usage_observer")
        pass


def main(args=None):
    rclpy.init(args=args)
    try: 
        node = PowerUsageObserver()
        rclpy.spin(node)
    except KeyboardInterrupt: 
        rclpy.shutdown()
    

if __name__ == '__main__':
    main()

