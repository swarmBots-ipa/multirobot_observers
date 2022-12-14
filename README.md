# swarm_observers
works as a support package to calculate localization error of swarmbots.


## Run localization error observer
 
`ros2 run localization_error_observer localization_error_observer`

- currently requires 15 samples of goal poses to work. 
- creates graph with iterations in x-axis and error values in y-axis
- support only manual saving of desired size images



## ToDo
- Save graphs automatically
- pass parameter to change sample size
