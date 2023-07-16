
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