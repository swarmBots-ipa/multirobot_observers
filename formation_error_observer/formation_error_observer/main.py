#! /usr/bin/env python3

import rclpy
from rclpy.executors import SingleThreadedExecutor
from formation_error_observer.pose_json import PoseSubscriber
from formation_error_observer.goal_json import GoalSubscriber

def main(args=None):

    rclpy.init(args=args)
    try:
        pose_json_subscriber = PoseSubscriber()
        goal_json_subscriber = GoalSubscriber()
        executor = SingleThreadedExecutor()

        executor.add_node(pose_json_subscriber)
        executor.add_node(goal_json_subscriber)


        try:
            executor.spin()
        finally:
            executor.shutdown()
            pose_json_subscriber.destroy_node()
            goal_json_subscriber.destroy_node()

    except KeyboardInterrupt:
        #For writing data into json and csv files
        GoalSubscriber.final_data()
        PoseSubscriber.final_data()


if __name__ == '__main__':
    main()

