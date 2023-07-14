#!/usr/bin/env python3

import rospy

import actionlib
import assignment_2_2022.msg
from nav_msgs.msg import Odometry
from research_track_1.msg import MyRobotOdom


class UserInterface:
    PROMPT = "Welcome to the User Interface created for the Research Track 1 Project\nPlease enter the (x, y coordinates you want the robot to navigate to:)"

    def __init__(self) -> None:
        # TODO Initialilze the Simple Action Client
        self.reaching_client = actionlib.SimpleActionClient(
            "/reaching_goal", assignment_2_2022.msg.PlanningAction
        )

        # Initialize the subscriber for odometry topic
        rospy.Subscriber("/odom", Odometry, self._pub_robot_state)

        self.robot_state_pub = rospy.Publisher(
            "robot_state", MyRobotOdom, queue_size=10
        )
        self.robot_state = MyRobotOdom()

        self.user_x_coord = 0.0
        self.user_y_coord = 0.0

    def _get_user_command(self) -> None:
        print(UserInterface.PROMPT)
        self.user_x_coord = input("Please enter the x coordinate: ")
        self.user_y_coord = input("Please enter the y coordinate: ")
        print(
            f"The given goal coordinates by the user is x: {self.user_x_coord}, y: {self.user_y_coord}"
        )

    def _send_reaaching_goal(self):
        # wait for the action server.
        self.reaching_client.wait_for_server()

        # Create a goal to send to the action server.
        goal = assignment_2_2022.msg.PlanningActionGoal()
        goal.goal.target_pose.pose.position.x = self.user_x_coord
        goal.goal.target_pose.pose.position.y = self.user_y_coord

        # Sends the goal to the action server.
        self.reaching_client.send_goal(goal)

    def _cancel_reaching_goal(self):
        # wait for the action server.
        try:
            self.reaching_client.wait_for_server(timeout=2)
        except Exception as e:
            pass

        if self.reaching_client.get_state() == actionlib.GoalStatus.ACTIVE:
            self.reaching_client.cancel_goal()

    def _pub_robot_state(self, odom_msg):
        # Position
        self.robot_state.x = odom_msg.pose.pose.position.x
        self.robot_state.y = odom_msg.pose.pose.position.y

        # Velocity
        self.robot_state.vel_x = odom_msg.twist.twist.linear.x
        self.robot_state.vel_z = odom_msg.twist.twist.linear.z

        # Publish the robot state message
        self.robot_state_pub.publish(self.robot_state)

    def _print_goal_details(self):
        print(
            f"The number of goal that has been reached is: {self.goal_reached} and the number of goals that has been cancelled is: {self.goal_cancelled}"
        )


if __name__ == "__main__":
    rospy.init_node("user_interface")
    ui = UserInterface()
