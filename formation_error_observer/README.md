# formation_error_observer

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
