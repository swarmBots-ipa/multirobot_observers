#!/usr/bin/env python3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
import csv
import os


class MileageObserverPlotter:
    
    def mileage_path_graph(path_travelled,actual_path_length):
        c=0

        #plotting graph
        fig, ax = plt.subplots(len(path_travelled),1,figsize = (12,10))
        for i in range(len(path_travelled)):
            def trunc(values, decs =0):
                return np.trunc(values*10**decs)/(10**decs)
            path_travelled = np.array(path_travelled)
            path_travelled =trunc(path_travelled,decs=2)
            actual_path_length = np.array(actual_path_length)
            actual_path_length = trunc(actual_path_length,decs=2)
            iteration = []
            std =[]
           
            for j in range(len(actual_path_length[i])):
                iteration.append(str(j+1))
                std.append(0.1)
                
            path_travelled_data, mileage_std = path_travelled[i], std
            actual_path_length_data, path_dist_std = actual_path_length[i], std

            ind = np.arange(len(path_travelled_data))  # the x locations for the groups
            width = 0.1 # the width of the bars
            matplotlib.rc('xtick', labelsize =13)
            matplotlib.rc('ytick', labelsize =13)
            matplotlib.rc('axes', labelsize =13)
            matplotlib.rc('figure', titlesize =20)
            #fig, ax = plt.subplots(1,len(path_travelled),figsize = (12,10))
            rects1 = ax[c].bar(ind - width/2, path_travelled_data, width, yerr=mileage_std,label='Path Travelled ')
            rects2 = ax[c].bar(ind + width/2, actual_path_length_data, width, yerr=path_dist_std,label='Path Estimated')
            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax[c].set_ylabel('Distance in meters')
            ax[c].set_xlabel('Number of Iterations')
            ax[c].set_title('Path Travelled vs Path Estimated - Agent : ' + str(i))
            ax[c].set_xticks(ind)
            ax[c].set_xticklabels(iteration)
            ax[c].legend()
            def autolabel(rects, xpos='center'):
                ha = {'center': 'center', 'right': 'left', 'left': 'right'}
                offset = {'center': 0, 'right': 1, 'left': -1}

                for rect in rects:
                    height = rect.get_height()
                    ax[c].annotate('{}'.format(height),
                                xy=(rect.get_x() + rect.get_width() / 2, height),
                                xytext=(offset[xpos]*3, 3),  # use 3 points offset
                                textcoords="offset points",  # in both directions
                                ha=ha[xpos], va='bottom')
            autolabel(rects1, "left")
            autolabel(rects2, "right")  
            fig.tight_layout()
            c=c+1
        plt.savefig(graph_path+'mileage_plot.png')

        plt.show()   


#Global Variables
#Crating and assigning paths

filename = os.path.basename(__file__)
search_dir = '/home/'
for root, dirs, files in os.walk(search_dir):
    if filename in files:
        file_location = os.path.join(root, filename)
        break
path = file_location.replace('mileage_observer/'+filename,'data')
csv_path = (path + "/csv/Robot")
graph_path = path+'/graphs/Agent_'
csv_folder= path+"/csv"
no_of_bots = 0
file_list = os.listdir(csv_folder)
for file_name in file_list:
        no_of_bots+=1
path_travelled =[]
actual_path_length =[]

#Creating empty arrays bsed on no. of bots to store data
for i in range(no_of_bots):
    path_travelled.append([])
    actual_path_length.append([])

#Fetching values from CSV
for i in range(no_of_bots):

    with open(csv_path+str(i)+'.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row.__contains__('Path Travelled'): 
             continue
            else :        
                path_travelled[i].append(float(row[2]))
                actual_path_length[i].append(float(row[1]))

def main():
     MileageObserverPlotter.mileage_path_graph(path_travelled,actual_path_length)
     
if __name__ == '__main__':
    main()
                