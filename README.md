# swarm_observers
works as a support package to calculate localization error of swarmbots.


## Run localization error observer
 
`ros2 run localization_error_observer localization_error_observer n`
- n - number of experiments to be condcted
- node save raw as well error csv in the workspace root directory

## Generate Graph
`cd src/localization_error_observer/localization_error_observer`
`python3 plot_graph.py n`
- n - number of plots to be generated 
- save the graphs manually into desired directory

## ToDo
- configure plot_graph
