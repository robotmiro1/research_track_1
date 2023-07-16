#!/usr/bin/env python3

import rospy
from math import sqrt

# importing the required ros message types
from research_track_1.msg import MyRobotOdom
from assignment_2_2022.msg import PlanningActionGoal

class OdomPublisher:
    """This class subscribes to the robot's position and velocity (using the
    custom message) and prints the distance of the robot from the target and
    the robot's average speed.)
    """
 
    def __init__(self) -> None:
        self.current_position_x =  0.0
        self.current_position_y =  0.0
        self.velocity_x = 0.0
        self.velocity_z = 0.0
        self.target_cord_x = 0.0
        self.target_cord_y = 0.0

        # check if the parameter server exists
        if rospy.has_param("/pub_speed"): 
            frequency = int(rospy.get_param("/pub_speed/frequency"))
        else:
            frequency = 1 

        rate = rospy.Rate(frequency)
        rospy.Subscriber("robot_state", MyRobotOdom, self._get_robot_state)
        rospy.Subscriber("/reaching_goal/goal", PlanningActionGoal, self._get_new_target)
        while True:
            self._print_status_report()
            rate.sleep()

    def _get_distance_to_target(self):
        """This method calculates the distance of the robot to the set
        target. 

        Returns:
            float: the value of the distance of the robot to the target
        """
        dist_x = self.target_cord_x - self.current_position_x
        dist_y = self.target_cord_y - self.current_position_y
        return sqrt((dist_x * dist_x) + (dist_y * dist_y))
    
    def _get_new_target(self, goal):
        """The is a callback function that gets the target send to the 
        `reaching_goal` action server and saves it as a parameter in the class

        Args:
            goal (PlanningActionGoal): the goal sent from the user interface as 
                the target to be reached. 
        """
        self.target_cord_x = goal.goal.target_pose.pose.position.x
        self.target_cord_y = goal.goal.target_pose.pose.position.y

    def _get_robot_state(self, robot_state):
        """This is a callback function that gets the robot (x, y) coordinates, 
        and the average speed of the robot and saves it as a property in the class

        Args:
            robot_state (MyRobotOdom): the position and velocity of the robot
        """
        self.current_position_x  = robot_state.x
        self.current_position_y  = robot_state.y
        self.velocity_x = robot_state.vel_x
        self.velocity_z = robot_state.vel_z

    def _print_status_report(self):
        """A method that prints a report with all the details about the status of the
        robot and the goal given by the user. 
        """
        print(f"\nThe distance of the robot to the target position is: {self._get_distance_to_target()}")
        print(f"The average linear speed of the robot is: {self.velocity_x}")
        print(f"The average rotation speed of the robot is: {self.velocity_z}\n")
 
if __name__ == "__main__": 
    rospy.init_node("robot_state")
    OdomPublisher()