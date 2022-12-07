import numpy as np
from matplotlib import pyplot as plt
from matplotlib import transforms
import numpy as np
import pandas as pd
from cycler import cycler
index = np.arange(1, 5, dtype=int)
coordinates = ["x","y","\u03F4"]
new_c = []
x_axis = []
for x in index:
    for val in coordinates:
        new_c.append(val + str(x))
print(new_c)
'''
start = 0
end = len(new_c)
step = 1
for i in range(start, end, step):
    x = i
    x_axis.append(new_c[x:x+step])

print(x_axis)
'''

import pandas as pd
import matplotlib.pyplot as plt
from itertools import groupby
import numpy as np 
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
custom_cycler =(cycler(color=['c','m','y']))
df = pd.DataFrame({'Name':new_c,
                  'TEST_Name':['1']*3+['2']*3+['3']*3+['4']*3,
                  'Label':['Median']*12,
                  'Data':data})
df = df.set_index(['TEST_Name','Name'])['Data']#.unstack()
print(df)
df.to_csv('experiment.csv')
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

ax = df.plot(marker='o', linestyle='none', colormap='Paired', xlim=(-.5,11.5), ylim=(.3,1.1))
#Below 2 lines remove default labelscustom_cyclercustocustom_cyclerm_cycler

ax.set_xticklabels('')
ax.set_xlabel('')
label_group_bar_table(ax, df)
ax.set_prop_cycle(custom_cycler)
ax.set_xlabel('Iterations')
ax.set_ylabel('Error')
ax.xaxis.set_label_coords(.5,-.3)
# you may need these lines, if not working interactive
plt.tight_layout()
plt.show()
'''
labels = ['apples', 'bananas', 'coconuts', 'dates', 'elderberries', 'figs', 'grapes']
years = [2017, 2018, 2019]
df = pd.DataFrame({'Iterations': np.tile(index, len(coordinates)),
                   'coordinates': np.tile(coordinates, len(index)),
                   'Amount': np.random.uniform(1.5, 5, len(index)*len(coordinates))})
print(df)

fig, ax = plt.subplots(figsize=(12, 4))

ax = sns.scatterplot(x='Iterations', y='Amount', hue='coordinates', palette='Reds', data=df, ax=ax)
print(ax.patches)
year_pos = np.sort( [p.get_x() + p.get_width()/2  for p in ax.patches])
print(year_pos)
ax.set_xticks(year_pos)
ax.set_xticklabels(np.tile(coordinates, len(index)), rotation=0)
ax.get_legend().remove()
ax.set_xlabel('') # remove default xlabel
fruit_pos = year_pos.reshape(-1, len(years)).mean(axis=1)
print(fruit_pos)
trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)

for pos, label in zip(fruit_pos, index):
    ax.text(pos, -0.25,  label, transform=trans, ha='center', va='bottom', color='steelblue', fontsize=14)
for pos in (fruit_pos[:-1] + fruit_pos[1:]) / 2:
    ax.axvline(pos, 0, -0.25, color='steelblue', ls=':' , clip_on=False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.show()
'''