# This Program generates plot, from the localization experiment
# Usage 'python3 plot_graph.py n'
# This programs required csv files which will be saved in the workspace when localization error observer is started, this program also saves the csv in the data folder

from matplotlib import pyplot as plt
from matplotlib import transforms

from cycler import cycler
from matplotlib import cm

from matplotlib.lines import Line2D
import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle, groupby, islice
import numpy as np 
import sys



for i in range(0,int(sys.argv[1])):
    """main function to create graphical repressentations of error propagation

    Args:
        sys args refers to number of csv files to given as input

    Usage: 
        python3 plot_graph.py n
    n - number of robots used in the case of swarm bots n = 4
    """        """"""
    
    # import dataframe from the csv and save in data
    df = pd.read_csv('../data/experiment' + str(i) +'.csv') # adjust this parameter to point to csv generated
    #df.to_csv('../data/experiment'+ str(i) + '.csv')
    # create index
    theta_rem_list = []
    for j in range(2, len(df.index), 3):
        theta_rem_list.append(j)
    #print(theta_rem_list)

    #print(df.reset_index())
    df1 = df.drop(theta_rem_list)
    df2 = df.iloc[theta_rem_list]

    df = df1 #  every 3rd row (mod 3)
    df = df.set_index(['TEST_Name','Name'])['Data']
    df2 = df2.set_index(['TEST_Name','Name'])['Data']
    list = []
    final_list = []

    
    #print(df2)
    #number of samples is directly inherited from the csv file
    #samples = len(df.index)
    #samples_theta = len(df2.index)

    #create a reference list
    #for i in range(1,int(samples/3+1)):
    #    list.append([i]*3)
    #for sub in list:
    #    for val in sub:
    #        final_list.append(val)


    #Transform function to generate x-axis
    def add_line(ax, xpos, ypos):
        line = plt.Line2D([xpos, xpos], [ypos + .1, ypos],
                        transform=ax.transAxes, color='gray')
        line.set_clip_on(False)
        ax.add_line(line)



    def label_len(my_index,level):
        labels = my_index.get_level_values(level)
        return [(k, sum(1 for i in g)) for k,g in groupby(labels)]



    def label_group_bar_table(df, legend_elements, color_cycle, y_axis_string, graph_label, j):

        samples = len(df.index)
        #create list of colors
        color_list =[]
        my_colors = islice(cycle(color_cycle), None, samples)
        for item in my_colors:
            color_list.append(item)    

        # xy plot
        fig, ax = plt.subplots(1)
        
        # xy-plot
        mylist = np.arange(1, int(samples+1)).tolist()
        

        #create axis of xy plot
        ax.scatter(mylist, df.values, c=color_list)


        #setup y axis limits and deviations change 0.5 to gain desired resolution
        plt.yticks(np.arange(df.values.min(), df.values.max(), 0.5))
        #set x axis limits
        plt.xlim(0.5,samples + 0.5)
        ax.set_xticklabels('')
        ax.set_xlabel('')
        ypos = -.1
        scale = 1./df.index.size
        #print(range(df.index.nlevels)[::-1])
        for level in range(df.index.nlevels)[::-1]:
            pos = 0
            for label, rpos in label_len(df.index,level):
                lxpos = (pos + .5 * rpos)*scale
                #print(label)
                ax.text(lxpos, ypos, label, ha='center', transform=ax.transAxes)
                add_line(ax, pos*scale, ypos)
                pos += rpos
            add_line(ax, pos*scale , ypos)
            ypos -= .1
            
        #add legend



        ax.legend(handles=legend_elements, loc='upper left')

        #add grids
        ax.minorticks_on()
        ax.grid(which='major', linestyle='-', linewidth='0.5')
        ax.grid(which='minor',linestyle='-', linewidth='0.5')

        #add labels
        ax.set_xlabel('Iterations')
        ax.set_ylabel(y_axis_string)
        ax.xaxis.set_label_coords(.5,-.3)

        figure = plt.gcf()  # get current figure
        figure.set_size_inches(32, 18)
        plt.tight_layout()
        #plt.show()
        plt.savefig('../data/epg_robot_' + str(j) + "_" + graph_label + "_" + '.png')



    color_cycle = ['b', 'r']
    color_cycle2 = ['g']
    legend_elements = [Line2D([0], [0], marker='o', color='b', label='x',
                        markerfacecolor='b', markersize=8),
                        Line2D([0], [0], marker='o', color='r', label='y',
                        markerfacecolor='r', markersize=8),
                        ]

    legend_elements2 = [Line2D([0], [0], marker='o', color='g', label='\u03F4',
                        markerfacecolor='g', markersize=8)]
    

    y_axis_string = "Error in cm"
    y_axis_string2 = "Error in \u03F4"

    graph_label = "xy"
    graph_label2 = "theta"


    label_group_bar_table(df, legend_elements, color_cycle, y_axis_string, graph_label, i)
    label_group_bar_table(df2, legend_elements2, color_cycle2, y_axis_string2, graph_label2, i)
