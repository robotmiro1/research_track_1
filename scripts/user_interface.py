#!/usr/bin/env python3 

import rospy

# Brings in the SimpleActionClient
import actionlib

class UserInterface: 
    PROMPT = "Welcome to the User Interface created for the Research Track 1 Project\nPlease enter the (x, y coordinates you want the robot to navigate to:)"
    def __init__(self) -> None:
        # TODO Initialilze the Simple Action Client
        self.user_x_coord = 0.0
        self.user_y_coord = 0.0

    def _get_user_coord(self) -> None: 
        print(UserInterface.PROMPT)
        self.user_x_coord = input("Please enter the x coordinate: ")
        self.user_y_coord = input("Please enter the y coordinate: ")
        print(f"The given goal coordinates by the user is x: {self.user_x_coord}, y: {self.user_y_coord}")

if __name__ == "__main__": 
    rospy.init_node("user_interface")
    ui = UserInterface()
    ui._get_user_coord()


    