#!/usr/bin/env python3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np



class MileageObserverPlotter:
    
    def mil_path_graph(mil_arr,path_arr):
        for i in range(len(mil_arr)):
            def trunc(values, decs =0):
                return np.trunc(values*10**decs)/(10**decs)
            mil_arr = np.array(mil_arr)
            mil_arr =trunc(mil_arr,decs=2)
            path_arr = np.array(path_arr)
            path_arr = trunc(path_arr,decs=2)
            iteration = []
            std =[]
            for j in range(len(path_arr[i])):
                iteration.append('Iteration'+str(j+1))
                std.append(0.2)

            mileage, mileage_std = mil_arr[i], std
            path_dist, path_dist_std = path_arr[i], std

            ind = np.arange(len(mileage))  # the x locations for the groups
            width = 0.35  # the width of the bars

            fig, ax = plt.subplots()
            rects1 = ax.bar(ind - width/2, mileage, width, yerr=mileage_std,label='Mileage')
            rects2 = ax.bar(ind + width/2, path_dist, width, yerr=path_dist_std,label='Path distance')

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax.set_ylabel('Distance')
            ax.set_title('Mileage vs Path distance')
            ax.set_xticks(ind)
            
            

            ax.set_xticklabels(iteration)
            ax.legend()


            def autolabel(rects, xpos='center'):
                ha = {'center': 'center', 'right': 'left', 'left': 'right'}
                offset = {'center': 0, 'right': 1, 'left': -1}

                for rect in rects:
                    height = rect.get_height()
                    ax.annotate('{}'.format(height),
                                xy=(rect.get_x() + rect.get_width() / 2, height),
                                xytext=(offset[xpos]*3, 3),  # use 3 points offset
                                textcoords="offset points",  # in both directions
                                ha=ha[xpos], va='bottom')


            autolabel(rects1, "left")
            autolabel(rects2, "right")

            fig.tight_layout()
            plt.savefig('../data/graphs/barista_'+str(i)+'.png')
        plt.show()    
    
