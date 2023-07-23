
<h1 align="center"> Research Track 1 </h1>

>**Author:** *Amanzhol Raisov*  
>**Student ID:** *4889656*

## Project Requirements

*What should you do here?* 
1. Create a new package, in which you will develop three nodes:
    - (a) A node that implements an action client, allowing the user to set a target (x, y) or to cancel it. The node also publishes the robot position and velocity as a custom message (x,y, vel_x, vel_z), by relying on the values published on the topic /odom. Please consider that, if you cannot implement everything in the same node, you can also develop two different nodes, one implementing the user interface and one implementing the publisher of the custom message.
    - (b) A service node that, when called, prints the number of goals reached and cancelled;
    - (c) A node that subscribes to the robot’s position and velocity (using the custom message) and prints the distance of the robot from the target and the robot’s average speed. Use a parameter to set how fast the node publishes the information. 
1. Also create a launch file to start the whole simulation. Set the value for the frequency with which node (c) publishes the information.

*Additional Requirements:*
- Only for node (a): Create a flowchart of your code, or describe it in pseudocode [(Pseudocode Examples
(unf.edu))](https://www.unf.edu/~broggio/cop2221/2221pseu.htm)
- Add some comments to the code
- Use functions to avoid having a single block of code
- Publish the new package on your own repository. The flowchart (or the pseudocode) should be added to the
ReadMe of the repository. (consider using Markdown syntax to write your readme: Basic Syntax | Markdown
Guide)
- Deadline: 09/01/2023
- In case you are participating in the 2° exam session, the deadline is postponed to 26/01/2023

## Description of the Solution Nodes
### (A) User Interface 

*__file_name__: user_interface.py*

This node gives a prompt to the user to do one of three commands; 

* Send goal 
* Cancel goal 
* Quit the Interface

if `send goal` is being selected, the interface then give a prompt to enter the x and y coordinate which the robot is required to navigate to. if `cancel goal` is being selected, it sends a cancel signal to the `reaching_goal` action server. Before doing this, it makes a check to see if the `reaching_goal` status is `ACTIVE`, if it is, it sends the cancel signal, otherwise, it does nothing. if quit interface is being selected, the `user_interface` node exit safely. *This nodes command request is put in a loop, therefore, the user can send nfinite amount of commands through the user interface, and when the user is done, the user must enter the third command to end the user interface safely. 



### (B) Goal Logger

*__file_name__: goal_logger.py*

This node subscribes to the `/reaching_goal/feedback` action feedback topic, and gets the status of the goal from the `stat` property of the message, it then uses this value to increment the value of `goal_reached` and `goal_cancelled`. The node provides a service `/goal_logger`, which when called prints and send the details of the number of goals reached and the number of goals cancelled. 


### (C) Robot State Node

*__file_name__: robot_state_pub.py*

This node subscribes to the topic `robot_state` of the custom message which contains the position (x, y) and the velocity (vel_x, vel_z). It also subscribes to the `/reaching_goal/goal` goal topic of the reaching goal action, to get the target positon in which the robot is to navigate to. It then uses this information to calculate the distance of the robot to the target. Given a set frequency from the `/pub_speed` parameter server, it prints this information with the said frequency.  



## Installation and Running Procedure

### Compile

First, you create a folder for your catkin workspace

```bash
mkdir -p ~/catkin_ws/src
```

Clone the package repository

```bash
cd ~/catkin_ws/src
git clone https://github.com/robotmiro1/research_track_1.git 
```

Clone the dependency package repository
```bash
cd ~/catkin_ws/src
git clone https://github.com/CarmineD8/assignment_2_2022.git
```


Once the packages has been successfully cloned, you then build the workspace

```bash
source /opt/ros/noetic/setup.bash
cd ~/catkin_ws/
catkin_make 
```

### Launch

Launch the simulation and all the required nodes. 
```bash
source ~/catkin_ws/devel/setup.bash
roslaunch research_track_1 sim.launch
```

Launch the User Interface to send command to the controller. 
```bash
source ~/catkin_ws/devel/setup.bash
rosrun research_track_1 user_interface.py
```
follow the instructions on the user interface to send commands to the controller. 

[Click Here](https://robotmiro1.github.io/research_track_1/) to view the html documentation of the project...