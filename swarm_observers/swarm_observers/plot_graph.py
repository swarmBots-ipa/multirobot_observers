# This Program generates plot, from the localization experiment
# Usage 'python3 plot_graph.py'
# This programs required csv file save inside doc folder it can be generated from running localization_error_observer ros node

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import transforms
import numpy as np
import pandas as pd
from cycler import cycler
from matplotlib import cm

from matplotlib.lines import Line2D
import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle, groupby, islice
import numpy as np 





# create a list of numbers from 1 to number of experiments created 
list = []
final_list = []
for i in range(1,5):
    list.append([i]*3)
for sub in list:
    for val in sub:
        final_list.append(val)
print(final_list)

#creation of synthetic data for experiment
'''
delta_dictionary = {}
delta_dictionary['x'] = {}
delta_dictionary['y'] = {}
delta_dictionary['theta'] = {}

delta_dictionary['x'] = [.54,.62,.55,.62]
delta_dictionary['y'] = [.55,.67,.54,.62]
delta_dictionary['theta'] = [.55,.62,.55,.67]
data = []
for i  in range(0,4):
    data.append(delta_dictionary['x'][i])
    data.append(delta_dictionary['y'][i])
    data.append(delta_dictionary['theta'][i])
print(data)
'''

#uncomment to create structure dataframe from only data
'''
index = np.arange(1, 5, dtype=int)
coordinates = ["x","y","\u03F4"]
new_c = []
x_axis = []
for x in index:
    for val in coordinates:
        new_c.append(val + str(x))
print(new_c)
df = pd.DataFrame({'Name':new_c,
                  'TEST_Name':final_list,
                  'Label':['Median']*12,
                  'Data':data})

df = df.set_index(['TEST_Name','Name'])['Data']#.unstack()
df.to_csv('experiment.csv')
'''


# change experiment numer to generate graphs
df = pd.read_csv('../doc/experiment3.csv')
# create index
df = df.set_index(['TEST_Name','Name'])['Data']



#Transform function to generate x-axis
def add_line(ax, xpos, ypos):
    line = plt.Line2D([xpos, xpos], [ypos + .1, ypos],
                      transform=ax.transAxes, color='gray')
    line.set_clip_on(False)
    ax.add_line(line)

def label_len(my_index,level):
    labels = my_index.get_level_values(level)
    return [(k, sum(1 for i in g)) for k,g in groupby(labels)]

def label_group_bar_table(ax, df):
    ypos = -.1
    scale = 1./df.index.size
    #print(range(df.index.nlevels)[::-1])
    for level in range(df.index.nlevels)[::-1]:
        pos = 0
        for label, rpos in label_len(df.index,level):
            lxpos = (pos + .5 * rpos)*scale
            print(label)
            ax.text(lxpos, ypos, label, ha='center', transform=ax.transAxes)
            add_line(ax, pos*scale, ypos)
            pos += rpos
        add_line(ax, pos*scale , ypos)
        ypos -= .1




#create list of colors
color_list =[]
my_colors = islice(cycle(['b', 'r', 'g']), None, 45)
for item in my_colors:
    color_list.append(item)    

fig, ax = plt.subplots(1)



#x-axis
mylist = np.arange(1, 46).tolist()

#create axis
ax.scatter(mylist, df.values, c=color_list)

#ax = df.plot(marker='o', linestyle='none', xlim=(-.5,44.5), cmap=cmap)#,ylim=(.3,1.1))
#Below 2 lines remove default labelscustom_cyclercustocustom_cyclerm_cycler

#setup axis limits
plt.yticks(np.arange(df.values.min(), df.values.max(), 0.5))
plt.xlim(0.5,45.5)
ax.set_xticklabels('')
ax.set_xlabel('')

#add x-axis values
label_group_bar_table(ax, df)

#add legend
legend_elements = [Line2D([0], [0], marker='o', color='b', label='x',
                          markerfacecolor='b', markersize=8),
                   Line2D([0], [0], marker='o', color='r', label='y',
                          markerfacecolor='r', markersize=8),
                   Line2D([0], [0], marker='o', color='g', label='\u03F4',
                          markerfacecolor='g', markersize=8)]

ax.legend(handles=legend_elements, loc='upper left')

#add grids
ax.minorticks_on()
ax.grid(which='major', linestyle='-', linewidth='0.5')
ax.grid(which='minor',linestyle='-', linewidth='0.5')

#add labels
ax.set_xlabel('Iterations')
ax.set_ylabel('Error in cm')
ax.xaxis.set_label_coords(.5,-.3)
# you may need these lines, if not working interactive
plt.tight_layout()
plt.show()