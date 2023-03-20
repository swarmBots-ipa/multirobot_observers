import matplotlib.pyplot as plt
import os
import csv
import numpy as nmpi
import matplotlib

class PowerObserverPlotter:
    def Power_Graph(time_array,voltage_array,current_array,temperature_array,charge_percentage_array):
        
        for i in range(no_of_bots):

            fig, axs = plt.subplots(2, 2,figsize = (15,10))
            fig.tight_layout(pad=5.0)
        

            axs[0, 0].plot(voltage_array[i], time_array[i])
            axs[0, 0].set_title('Voltage Graph')
            axs[0, 0].set(xlabel= 'voltage', ylabel='time')
            axs[0, 1].plot(current_array[i], time_array[i], 'tab:orange')
            axs[0, 1].set_title('Current Graph')
            axs[0, 1].set(xlabel= 'current', ylabel='time')
            axs[1, 0].plot(temperature_array[i], time_array[i], 'tab:green')
            axs[1, 0].set_title('Temperature Graph')
            axs[1, 0].set(xlabel= 'temperature', ylabel='time')
            axs[1, 1].plot(charge_percentage_array[i], time_array[i], 'tab:red')
            axs[1, 1].set_title('Charge Percentage Graph')
            axs[1, 1].set(xlabel= 'charge percentage', ylabel='time')
        
            plt.savefig(graph_path+str(i)+'.png')
        plt.show()


filename = os.path.basename(__file__)
search_dir = '/home/'
for root, dirs, files in os.walk(search_dir):
    if filename in files:
        file_location = os.path.join(root, filename)
        break
path = file_location.replace('power_usage_observer/'+filename,'data')
csv_path = (path + "/csv/Robot")
graph_path = path+'/graphs/Barista_'
csv_folder= path+"/csv"
no_of_bots = 0
file_list = os.listdir(csv_folder)
for file_name in file_list:
        no_of_bots+=1
time_array = []
voltage_array = []
current_array = []
temperature_array = []
charge_percentage_array = []

for i in range(no_of_bots):
    time_array.append([])
    voltage_array.append([])
    current_array.append([])
    temperature_array.append([])
    charge_percentage_array.append([])


for i in range(no_of_bots):
    with open(csv_path+str(i)+'.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row.__contains__("time"):
                continue
            time_array[i].append(row[0])
            voltage_array[i].append(nmpi.round(float(row[1]),3))
            current_array[i].append(nmpi.round(float(row[2]),3))
            temperature_array[i].append(nmpi.round(float(row[3]),3))
            charge_percentage_array[i].append(nmpi.round(float(row[4]),3))
PowerObserverPlotter.Power_Graph(time_array,voltage_array,current_array,temperature_array,charge_percentage_array)
        
        