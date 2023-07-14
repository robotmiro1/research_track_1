#!/usr/bin/env python3

import rospy
from math import sqrt
from research_track_1.msg import MyRobotOdom
from assignment_2_2022.msg import PlanningActionGoal

class OdomPublisher:
    def __init__(self) -> None:
        self.current_position_x =  0.0
        self.current_position_y =  0.0
        self.velocity_x = 0.0
        self.velocity_z = 0.0
        self.target_cord_x = 0.0
        self.target_cord_y = 0.0
        rospy.has_param(/)
        rospy.Rate()
        rospy.Subscriber("robot_state", MyRobotOdom, self._get_robot_state)
        rospy.Subscriber("/reaching_goal/goal", PlanningActionGoal, self._get_new_target)

    def _get_distance_to_target(self, target):
        dist_x = self.target.cord_x - self.current_position_x
        dist_y = self.target.cord_y - self.current_position_y
        return sqrt((dist_x * dist_x) + (dist_y * dist_y))
    
    def _get_new_target(self, goal):
        self.target_cord_x = goal.target_pose.pose.position.x
        self.target_cord_y = goal.target_pose.pose.position.y

    def _get_robot_state(self, robot_state):
        self.current_position_x  = robot_state.x
        self.current_position_y  = robot_state.y
        self.velocity_x = robot_state.vel_x
        self.velocity_z = robot_state.vel_z

    def _print_status_report(self):
        print(f"The distance of the robot to the target position is: {self._get_distance_to_target()}")
        print(f"The average linear speed of the robot is: {self.velocity_x}")
        print(f"The average rotation speed of the robot is: {self.velocity_z}")
 