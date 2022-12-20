#!/usr/bin/env python3
#Current path witten using utils.py
current_path = "/home/kut-jr/swarmbots/src/formation_error_observer/data" 

import json
import matplotlib.pyplot as mlt
import numpy as nmpi
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
import shapely.ops as so
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os

#Fetching and loading json file
pose_file = open(current_path + '/Poses.json', 'r')
goal_file = open(current_path + '/Goals.json', 'r')
pose_data = pose_file.read()
goal_data = goal_file.read()
goal = json.loads(goal_data)
pose = json.loads(pose_data)

#storing goal coordinates in arrays

#Goal Coordinates
goal_x_arr = []
goal_y_arr = []
goal_theta_arr = []

for i in range(4):
    Main = goal[i]
    goal_array = Main["barista_" + str(i) + "_goal"]
    length = len(goal_array)
    for k in range(length):
        goal_list = goal_array[k]
        if i == 0: goal_x_0 = goal_list["x"]; goal_y_0 = goal_list["y"]; goal_theta_0 = goal_list["theta"];goal_x_arr.append(goal_x_0);goal_y_arr.append(goal_y_0);goal_theta_arr.append(goal_theta_0)
        if i == 1: goal_x_1 = goal_list["x"]; goal_y_1 = goal_list["y"]; goal_theta_1 = goal_list["theta"];goal_x_arr.append(goal_x_1);goal_y_arr.append(goal_y_1);goal_theta_arr.append(goal_theta_1)
        if i == 2: goal_x_2 = goal_list["x"]; goal_y_2 = goal_list["y"]; goal_theta_2 = goal_list["theta"];goal_x_arr.append(goal_x_2);goal_y_arr.append(goal_y_2);goal_theta_arr.append(goal_theta_2)
        if i == 3: goal_x_3 = goal_list["x"]; goal_y_3 = goal_list["y"]; goal_theta_3 = goal_list["theta"];goal_x_arr.append(goal_x_3);goal_y_arr.append(goal_y_3);goal_theta_arr.append(goal_theta_3)


#Pose Coordinates
pose_x_array = []
pose_y_array = []
pose_theta_array = []
for i in range(4):
    Main = pose[i]
    pose_array = Main["barista_" + str(i) + "_pose"]
    length = len(pose_array)
    for k in range(length):
        pose_list = pose_array[k]
        if i == 0: pose_x_0 = pose_list["x"]; pose_y_0 = pose_list["y"]; pose_theta_0 = pose_list["theta"];pose_x_array.append(pose_x_0);pose_y_array.append(pose_y_0);pose_theta_array.append(pose_theta_0)
        if i == 1: pose_x_1 = pose_list["x"]; pose_y_1 = pose_list["y"]; pose_theta_1 = pose_list["theta"];pose_x_array.append(pose_x_1);pose_y_array.append(pose_y_1);pose_theta_array.append(pose_theta_1)
        if i == 2: pose_x_2 = pose_list["x"]; pose_y_2 = pose_list["y"]; pose_theta_2 = pose_list["theta"];pose_x_array.append(pose_x_2);pose_y_array.append(pose_y_2);pose_theta_array.append(pose_theta_2)
        if i == 3: pose_x_3 = pose_list["x"]; pose_y_3 = pose_list["y"]; pose_theta_3 = pose_list["theta"];pose_x_array.append(pose_x_3);pose_y_array.append(pose_y_3);pose_theta_array.append(pose_theta_3)

#Plotting goal and pose dot chart
goal_x_points = nmpi.array(goal_x_arr)
pose_x_points = nmpi.array(pose_x_array)
goal_y_points = nmpi.array(goal_y_arr)
pose_y_points = nmpi.array(pose_y_array)
mlt.figure("Goal vs Actual")
mlt.scatter(goal_x_points, goal_y_points, color='green', label='Goal')
mlt.scatter(pose_x_points, pose_y_points, color='red', label='Actual')
mlt.legend()
#Creating polygon set

goal_poly_coord={}
Pose_poly_coord={}
goal_poly_set=[]
pose_poly_set=[]

num_of_runs=  int(len(goal_x_arr)/4) #Number of runs
ig, ax = plt.subplots()
plt.suptitle('Goal vs Actual')
i=0
for l in range(num_of_runs):
    goal_poly_coord[l] =  Polygon([(goal_x_arr[i],goal_y_arr[i]),(goal_x_arr[i+num_of_runs],goal_y_arr[i+num_of_runs]),(goal_x_arr[i+(num_of_runs*2)],goal_y_arr[i+(num_of_runs*2)]),(goal_x_arr[i+(num_of_runs*3)],goal_y_arr[i+(num_of_runs*3)])])
    Pose_poly_coord[l] = Polygon([(pose_x_array[i],pose_y_array[i]),(pose_x_array[i+num_of_runs],pose_y_array[i+num_of_runs]),(pose_x_array[i+(num_of_runs*2)],pose_y_array[i+(num_of_runs*2)]),(pose_x_array[i+(num_of_runs*3)],pose_y_array[i+(num_of_runs*3)])])
    i+=1
    goal_poly_set.append(goal_poly_coord[l])
    pose_poly_set.append(Pose_poly_coord[l])

goal_polygon = MultiPolygon(goal_poly_set)
pose_polygon = MultiPolygon(pose_poly_set)

#Ploting Polygons

for poly in goal_polygon.geoms:
    xe, ye = poly.exterior.xy
    ax.plot(xe, ye, color="blue")
for poly in pose_polygon.geoms:
    xe, ye = poly.exterior.xy
    ax.plot(xe, ye, color="red")
legend = [Line2D([0], [0], color='b', label='Goal'),
          Line2D([0], [0], color='r', label='Actual')]

ax.legend(handles=legend)

ax.minorticks_on()
ax.grid(which='major', linestyle='-', linewidth='0.5')
ax.grid(which='minor',linestyle='-', linewidth='0.5')

mlt.show()
