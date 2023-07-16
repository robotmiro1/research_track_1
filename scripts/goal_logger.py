#!/usr/bin/env python3
import rospy

from assignment_2_2022.msg import PlanningActionFeedback
from std_srvs.srv import Trigger, TriggerResponse

test = PlanningActionFeedback()

class GoalLogger:
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
        if goal_feedback.feedback.stat == "Target reached!":
            self.goal_reached += 1
        elif goal_feedback.feedback.stat == "Target cancelled!":
            self.goal_cancelled += 1

    def _print_goal_log(self, dummy):
        response =  TriggerResponse()
        response.success = True
        response.message = f"Goals Logs: \nNumber of Goal(s) Reached: {self.goal_reached}\nNumber of Goal(s) Cancelled: {self.goal_cancelled}"
        print(response.message)
        return response

if __name__ == "__main__": 
    rospy.init_node("goal_logger")
    GoalLogger()