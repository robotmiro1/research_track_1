#!/usr/bin/env python3

"""
.. module:: goal_logger
    :platform: Unix
    :synopsis: Python module that logs the goal reached and cancelled

.. moduleauthor:: Amanzhol Raisov cornytravel@gmail.com

This module subcribes to the action client message `reaching_goal/feedback`,
it then use the messages on this topic to log the number of goals that is
reached and the number of goals that is cancelled. The node initializes a
ros server with the name `/goal_logger`, when a request is being sent to this
server, it prints the value of the number of goals reached and cancel that has
already been logged.

Subscribes to:
    `/reaching_goal/feedback`

Service:
    `/goal_logger`
"""

import rospy

# importing the require ros message types 
from assignment_2_2022.msg import PlanningActionFeedback 
from std_srvs.srv import Trigger, TriggerResponse


class GoalLogger:
    """Logs the number of goals that are reached and the number of goals that are
    cancelled.
    """

    def __init__(self) -> None:
        self.goal_reached = 0
        self.goal_cancelled = 0

        # Initialize a subscriber for ros action feedback
        rospy.Subscriber(
            "/reaching_goal/feedback", PlanningActionFeedback, self._goal_logger
        )
        rospy.Service("/goal_logger", Trigger, self._print_goal_log)
        rospy.spin()

    def _goal_logger(self, goal_feedback):
        """A callback function that gets the feedback from the `reaching_goal`
        action, it then takes the stats of the target reached and target cancelled
        and saves it in the appropriate property of the class

        Args:
            goal_feedback (PlanningActionFeedback): an object that contains the stat
                data of the number of target reached and target cancelled
        """
        if goal_feedback.feedback.stat == "Target reached!":
            self.goal_reached += 1
        elif goal_feedback.feedback.stat == "Target cancelled!":
            self.goal_cancelled += 1

    def _print_goal_log(self, dummy):
        """A callback function that prints the stats of goals reached and goals
        cancelled when triggered

        Args:
            dummy (str): it's an empty string, just used for the trigger

        Returns:
            str: the response of the stats of the number of goals reached and cancelled
        """
        response = TriggerResponse()
        response.success = True
        response.message = f"Goals Logs: \nNumber of Goal(s) Reached: {self.goal_reached}\nNumber of Goal(s) Cancelled: {self.goal_cancelled}"
        print(response.message)
        return response


if __name__ == "__main__":
    rospy.init_node("goal_logger")
    GoalLogger()
