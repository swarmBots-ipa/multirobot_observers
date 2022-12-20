# localization_error_observer
## Start the observers
 
`ros2 run localization_error_observer localization_error_observer n`
- n - number of experiments to be condcted
- node save raw as well error csv in the workspace root directory

## Generate visualizations 
`cd src/localization_error_observer/localization_error_observer`
`python3 plot_graph.py n`
- n - number of plots to be generated 
- save the graphs manually into desired directory