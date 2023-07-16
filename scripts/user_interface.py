#!/usr/bin/env python3

# import the ros api
import rospy
import actionlib

# importing the required ros message types
import assignment_2_2022.msg
from nav_msgs.msg import Odometry
from research_track_1.msg import MyRobotOdom


class UserInterface:
    """A node that allows a user to set the target (x, y) or to cancel it. The node also
    publishes the robot position and velocity as a custom message (x, y, vel_x, vel_z)
    by relying on the values published on the topic `/odom`
    """

    PROMPT = "Welcome to the User Interface created for the Research Track 1 Project\n"

    def __init__(self) -> None:
        # Initialilze the Simple Action Client
        self.reaching_client = actionlib.SimpleActionClient(
            "/reaching_goal", assignment_2_2022.msg.PlanningAction
        )

        # Initialize the subscriber for odometry topic
        rospy.Subscriber("/odom", Odometry, self._pub_robot_state)

        # Initialize the publisher for custom message
        self.robot_state_pub = rospy.Publisher(
            "robot_state", MyRobotOdom, queue_size=10
        )
        self.robot_state = MyRobotOdom()

        self.user_x_coord = 0.0
        self.user_y_coord = 0.0
        self.trial = 0 # to count the amount of time the user enters the wrong command
        self.timeout = rospy.Duration(1)
        print(UserInterface.PROMPT)
        while True:
            if self.trial == 3:
                break
            self._get_user_command()

    def _get_user_command(self) -> None:
        """This method takes input of the user command and saves it as a property in the class"""
        self.user_action = input(
            "\nEnter 1 to set a new goal, 2 to cancel an ongoing goal, 3 to quit the interface: "
        )
        if self.user_action == "1":
            self.user_x_coord = int(input("Please enter the x coordinate: "))
            self.user_y_coord = int(input("Please enter the y coordinate: "))
            print(
                f"You have given a target of x: {self.user_x_coord} and y: {self.user_y_coord}"
            )
            self._send_reaaching_goal()
        elif self.user_action == "2":
            self._cancel_reaching_goal()

        elif self.user_action == "3":
            self.trial = 3
        else:
            print("You have entered the wrong command, try again!")
            print(f"Failed Trial {self.trial} out of 3\n")

    def _send_reaaching_goal(self):
        """This method sends the target set by the user to the `reachine_goal` action
        server.
        """
        # wait for the action server.
        # if (self.reaching_client.wait_for_server(timeout=self.timeout)):
        self.reaching_client.wait_for_server(timeout=self.timeout)
        # Create a goal to send to the action server.
        goal = assignment_2_2022.msg.PlanningActionGoal()
        goal.goal.target_pose.pose.position.x = self.user_x_coord
        goal.goal.target_pose.pose.position.y = self.user_y_coord

        # Sends the goal to the action server.
        self.reaching_client.send_goal(goal.goal)
        print("The goal has been sent sucessfully")
        # else:
        #     print(f"The goal failed to send because the server is not yet available.")

    def _cancel_reaching_goal(self):
        """This method sends a cancel signal to the reaching_goal action server to
        preempt a goal
        """
        # wait for the action server.
        self.reaching_client.wait_for_server(timeout=self.timeout)
        if self.reaching_client.get_state() == actionlib.GoalStatus.ACTIVE:
            self.reaching_client.cancel_goal()

    def _pub_robot_state(self, odom_msg):
        """This method publishes the robot position and velocity on a topic as a custom
        message type

        Args:
            odom_msg (MyRobotOdom): the position and velocity of the robot
        """
        # Position
        self.robot_state.x = odom_msg.pose.pose.position.x
        self.robot_state.y = odom_msg.pose.pose.position.y

        # Velocity
        self.robot_state.vel_x = odom_msg.twist.twist.linear.x
        self.robot_state.vel_z = odom_msg.twist.twist.linear.z

        # Publish the robot state message
        self.robot_state_pub.publish(self.robot_state)


if __name__ == "__main__":
    rospy.init_node("user_interface")
    ui = UserInterface()
