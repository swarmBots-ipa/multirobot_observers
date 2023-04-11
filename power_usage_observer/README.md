# power_usage_observer
This package is used observe the change in Battery voltage, Current discharge, Battery temperature and Battery charge percentage over time. The mentioned parameters are obtained from the topic "/battery_state".
Note: This package does not work on simulation

## Start the observers
```
ros2 run power_usage_observer main <Number of agents>

```

## Generate visualizations 
```
ros2 run power_usage_observer mileage_observer_plotter

```

Json and CSV files and graphs can be found in "<workspace>/src/multirobot_observers/power_usage_observer/data" folder

## Results
![](Agent.png)
