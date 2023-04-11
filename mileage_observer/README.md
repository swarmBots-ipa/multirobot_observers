# mileage_observer
This package is used to observe the differences between the distance travelled by the agents vs the distance given initially by the path planner. The actual distance travelled by the agent to reach the command pose is obtained from the topic "barista_agent-id/odom" and the initial distance suggested by the path planner is obtained from the topic "/barista_agent-id/plan".
## To run the simulation 

```
ros2 launch multirobot_bringup multirobot_bringup.launch.xml

```
## To run the agents

```
ros2 run multirobot_formation agent_formation <Number of agents>
```
## Launching observers

```
ros2 run mileage_observer main <Number of iterations> <Number of agents>

```
## Generate visualizations 

```
ros2 run mileage_observer mileage_observer_plotter

```

Json and CSV files and graphs can be found in "<workspace>/src/multirobot_observers/mileage_observer/data" folder

## Results
![](Agent_mileage_plot.png)