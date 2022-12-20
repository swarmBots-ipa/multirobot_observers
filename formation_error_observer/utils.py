import os

#to get current system path
current_path = os.getcwd()
line_num= 2
path = 'current_path = "' + current_path + '/data" \n'
package_name = '/formation_error_observer'

#to write path to pose_json.py file
with open (current_path + package_name +'/pose_json.py', 'r') as b:
    lines = b.readlines()
    lines[line_num] = path
with open(current_path + package_name +'/pose_json.py','w') as b:
    b.writelines(lines)
b.close()


#to write path to pose_json.py file
with open (current_path + package_name +'/goal_json.py', 'r') as b:
    lines = b.readlines()
    lines[line_num] = path
with open(current_path + package_name +'/goal_json.py','w') as b:
     b.writelines(lines)
b.close()


#to write path to plotter.py file
with open (current_path + package_name +'/plotter.py', 'r') as b:
    lines = b.readlines()
    lines[line_num] = path
with open(current_path + package_name +'/plotter.py','w') as b:
    b.writelines(lines)
b.close()
