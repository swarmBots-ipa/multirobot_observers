#!/usr/bin/env python3
#Current path witten using utils.py

import json
import matplotlib.pyplot as mlt
import numpy as nmpi
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from ament_index_python.packages import get_package_share_directory
import shapely.ops as so
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os

class FormationObserverPlotter:
    def Goal_Pose_Graph():
        filename = os.path.basename(__file__)
        search_dir = '/home/'
        for root, dirs, files in os.walk(search_dir):
            if filename in files:
                file_location = os.path.join(root, filename)
                break
        path = file_location.replace('formation_error_observer/'+filename,'data')

        pose_file = open(path + '/json/Poses.json', 'r')
        goal_file = open(path + '/json/Goals.json', 'r')
        pose_data = pose_file.read()
        goal_data = goal_file.read()
        goal = json.loads(goal_data)
        pose = json.loads(pose_data)
        # print(goal)
        # print(pose)
        #storing goal coordinates in arrays

        #goal Coordinates
        goal_x_arr = []
        goal_y_arr = []
        goal_theta_arr = []


        Main = goal[0]
        no_of_bots = len(Main)
        for i in range(no_of_bots):
            goal_array = Main["barista_" + str(i) + "_goal"]
            length = len(goal_array)
            for k in range(length):
                goal_list = goal_array[k]
                goal_x = goal_list["x"]; goal_y= goal_list["y"]; goal_theta = goal_list["theta"];goal_x_arr.append(goal_x);goal_y_arr.append(goal_y);goal_theta_arr.append(goal_theta)


        #pose Coordinates
        pose_x_array = []
        pose_y_array = []
        pose_theta_array = []

        Main = pose[0]
        for i in range(no_of_bots): 
            pose_array = Main["barista_" + str(i) + "_pose"]
            length = len(pose_array)
            for k in range(length):
                pose_list = pose_array[k]
                pose_x = pose_list["x"]; pose_y = pose_list["y"]; pose_theta = pose_list["theta"];pose_x_array.append(pose_x);pose_y_array.append(pose_y);pose_theta_array.append(pose_theta)
                                                         
        #Plotting goal and pose dot chart
        if no_of_bots == 1:
            goal_x_points = nmpi.array(goal_x_arr)
            pose_x_points = nmpi.array(pose_x_array)
            goal_y_points = nmpi.array(goal_y_arr)
            pose_y_points = nmpi.array(pose_y_array)
            mlt.figure("command_pose vs attained_pose")
            mlt.scatter(goal_x_points, goal_y_points, color='green', label='command_pose')
            mlt.scatter(pose_x_points, pose_y_points, color='red', label='attained_pose')
            mlt.savefig(path + '/graphs/dotgraph.png')
            mlt.legend()
            
        #Creating polygon set

        goal_poly_coord={}
        pose_poly_coord={}
        goal_poly_set=[]
        pose_poly_set=[]

        
        if no_of_bots>1:
            num_of_runs=  int(len(goal_x_arr)/no_of_bots) #Number of runs
            ig, ax = plt.subplots()
            plt.suptitle('command_pose vs attained_pose')
            i=0
            goal_poly_arr = []
            pose_poly_arr = []
            for l in range(num_of_runs):

                for j in range(no_of_bots):
                    if no_of_bots >= 3:
                        goal_poly_arr.append(((goal_x_arr[i+num_of_runs*j]),(goal_y_arr[i+num_of_runs*j])))
                        pose_poly_arr.append(((pose_x_array[i+num_of_runs*j]),(pose_y_array[i+num_of_runs*j]))) 
                    else:
                        goal_poly_arr.append(((goal_x_arr[i+num_of_runs*j]),(goal_y_arr[i+num_of_runs*j])))
                        pose_poly_arr.append(((pose_x_array[i+num_of_runs*j]),(pose_y_array[i+num_of_runs*j]))) 
                        if j==1:
                            goal_poly_arr.append(((goal_x_arr[i+num_of_runs*j]),(goal_y_arr[i+num_of_runs*j])))
                            pose_poly_arr.append(((pose_x_array[i+num_of_runs*j]),(pose_y_array[i+num_of_runs*j]))) 
            
                goal_poly_coord[l] =  Polygon(goal_poly_arr)
                pose_poly_coord[l] = Polygon(pose_poly_arr)
                i+=1
                goal_poly_set.append(goal_poly_coord[l])
                pose_poly_set.append(pose_poly_coord[l])

                goal_poly_arr =[]
                pose_poly_arr =[]

            goal_polygon = MultiPolygon(goal_poly_set)
            pose_polygon = MultiPolygon(pose_poly_set)

            
            #Ploting Polygons

            goal_x_points = nmpi.array(goal_x_arr)
            pose_x_points = nmpi.array(pose_x_array)
            goal_y_points = nmpi.array(goal_y_arr)
            pose_y_points = nmpi.array(pose_y_array)
            error = nmpi.round(nmpi.sqrt(nmpi.square(goal_x_points-pose_x_points)+nmpi.square(goal_y_points-pose_y_points)),3)
            #print(error) 

            mlt.scatter(goal_x_points, goal_y_points, color='blue', label='goal',marker=(5, 1))
            mlt.scatter(pose_x_points, pose_y_points, color='red', label='attained_pose')
            for i, txt in enumerate(error):
                 mlt.annotate(txt, (pose_x_points[i], pose_y_points[i]))

            
            for poly in goal_polygon.geoms:
                xe, ye = poly.exterior.xy
                ax.plot(xe, ye, color="blue")
            for poly in pose_polygon.geoms:
                xe, ye = poly.exterior.xy
                ax.plot(xe, ye, color="red")

            legend = [Line2D([0], [0], color='b', label='command_pose'),Line2D([0], [0], color='r', label='attained_pose')]

            ax.legend(handles=legend)

            ax.minorticks_on()
            ax.grid(which='major', linestyle='-', linewidth='0.5')
            ax.grid(which='minor',linestyle='-', linewidth='0.5')
            plt.savefig(path+'/graphs/Polygraph.png')

        mlt.show()
def main():
	FormationObserverPlotter.Goal_Pose_Graph()
if __name__ == '__main__':
    main()
