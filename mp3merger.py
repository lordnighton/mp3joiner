import os
import natsort
import subprocess
import json

LIST_FILE_NAME = "list.txt"

with open('config.json') as json_file:
    config_dict = json.load(json_file)

print(config_dict)

all_files_unsorted = []
for path, subdirs, files in os.walk(r'./source'):
   for filename in files:
        f = os.path.join(path, filename)
        if os.path.isfile(f):
            if filename in config_dict['filtered_files']:
                print("Needs to be filtered = " + filename)
            else:
                all_files_unsorted.append(str(f))

sorted_files = natsort.natsorted(all_files_unsorted,reverse=False)

if not os.path.exists(config_dict['dest_folder_name']):
    os.makedirs(config_dict['dest_folder_name'])

print(sorted_files)

# a = open(LIST_FILE_NAME, "w")
# for f1 in sorted_files:
#     a.write("file '" + str(f1) + "'" + os.linesep)

dest_folder_name = config_dict['dest_folder_name']
dest_file_name = config_dict['dest_file_name']

dest_file = os.path.join(config_dict['dest_folder_name'], config_dict['dest_file_name'])

subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", dest_file])

# drop the list file (!)
# os.remove(LIST_FILE_NAME)