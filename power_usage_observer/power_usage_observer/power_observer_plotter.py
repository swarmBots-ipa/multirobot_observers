import matplotlib.pyplot as plt
import os
import csv
import numpy as nmpi
import matplotlib

class PowerObserverPlotter:
    def Power_Graph(time_array,voltage_array,current_array,temperature_array,charge_percentage_array):
        
        plt.rc('xtick', labelsize =7)
        fig, axs = plt.subplots(4,no_of_bots,figsize = (15,10))

        


        for i in range(no_of_bots):

            fig.tight_layout(pad=3.0)
            
            

            axs[0,i].plot(time_array[i],voltage_array[i])
            axs[0,i].set_title('Agent_'+str[i]+' Battery State Observer \n \n Battery Voltage ')
            axs[0,i].set(xlabel='time (seconds)',ylabel= 'voltage (V)')
            axs[0,i].minorticks_on()
            axs[0,i].grid(which='major', linestyle='-', linewidth='0.8')
            axs[0,i].grid(which='minor',linestyle='-', linewidth='0.3')
            axs[1,i].plot(time_array[i],current_array[i],  'tab:orange')
            axs[1,i].set_title('Current Discharge')
            axs[1,i].set( xlabel='time (seconds)',ylabel= 'current (A)')
            axs[1,i].minorticks_on()
            axs[1,i].grid(which='major', linestyle='-', linewidth='0.8')
            axs[1,i].grid(which='minor',linestyle='-', linewidth='0.3')
            axs[2,i].plot(time_array[i],temperature_array[i],  'tab:green')
            axs[2,i].set_title('Battery Temperature')
            axs[2,i].set( xlabel='time (seconds)',ylabel= 'temperature (degree celsius)')
            axs[2,i].minorticks_on()
            axs[2,i].grid(which='major', linestyle='-', linewidth='0.8')
            axs[2,i].grid(which='minor',linestyle='-', linewidth='0.3')
            axs[3,i].plot(time_array[i],charge_percentage_array[i],  'tab:red')
            axs[3,i].set_title('Battery Charge Percentage')
            axs[3,i].set(xlabel='time (seconds)',ylabel= 'charge percentage (%)')
            axs[3,i].minorticks_on()
            axs[3,i].grid(which='major', linestyle='-', linewidth='0.8')
            axs[3,i].grid(which='minor',linestyle='-', linewidth='0.3')
        
        plt.savefig(graph_path+'.png')
        plt.show()

#Globbal Variables
#Setting path variables

filename = os.path.basename(__file__)
search_dir = '/home/'
for root, dirs, files in os.walk(search_dir):
    if filename in files:
        file_location = os.path.join(root, filename)
        break
path = file_location.replace('power_usage_observer/'+filename,'data')
csv_path = (path + "/csv/Robot")
graph_path = path+'/graphs/Agent'
csv_folder= path+"/csv"
no_of_bots = 0
file_list = os.listdir(csv_folder)

#Creating empty arrays to store data based on no of bots
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

#Reading data from csv
for i in range(no_of_bots):
    with open(csv_path+str(i)+'.csv', 'r') as csvfile:
             
        reader = csv.reader(csvfile)
        counter = 1
  
        for abc in reader:
            if abc.__contains__("time"):
                continue
           # time_array[i].append(counter)
            voltage_array[i].append(nmpi.round(float(abc[1]),3))
            current_array[i].append((nmpi.round(float(abc[2]),3))*(-1))
            temperature_array[i].append(nmpi.round(float(abc[3]),3))
            charge_percentage_array[i].append((nmpi.round(float(abc[4]),3))*100)
            counter = counter+1    
  

for i in range(no_of_bots):
    with open(csv_path+str(i)+'.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        first_row = rows[1][0]
        last_row = rows[-1][0]
        
        c = 1
        mean_time = (int(last_row)-int(first_row))/(counter-2)
        mean_time = round(mean_time)
        for row in rows:
            if row.__contains__("time"):
                continue
            time_array[i].append(c)
            c = c+mean_time
        
def main():
    PowerObserverPlotter.Power_Graph(time_array,voltage_array,current_array,temperature_array,charge_percentage_array)
if __name__ == '__main__':
    main()
        
        