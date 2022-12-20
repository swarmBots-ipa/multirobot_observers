# multirobot_observers
Observer stack with multiple observers for the multi-robot fleet monitoring.

# 1. localization_error_observer
## Start the observers
 
`ros2 run localization_error_observer localization_error_observer n`
- n - number of experiments to be condcted
- node save raw as well error csv in the workspace root directory

## Generate visualizations 
`cd src/localization_error_observer/localization_error_observer`
`python3 plot_graph.py n`
- n - number of plots to be generated 
- save the graphs manually into desired directory

# 2. formation_error_observer

## Fix path in all python files:
Open terminal and navigate to "<workspace>/src/formation_error_observer/"

```
python3 utils.py

```
## Start the observers

```
ros2 run formation_error_observer main

```
Press 'ctrl+c' at the end of execution to save the data to Json and CSV

## Generate visualizations

```
ros2 run formation_error_observer plotter

```

Json and CSV files can be found in "<workspace>/src/formation_error_observer/data" folder
