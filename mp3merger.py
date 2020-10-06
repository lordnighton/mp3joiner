import os
import natsort
import subprocess
import json
import shutil
import numpy

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

LIST_FILE_NAME = "list.txt"

with open('config.json') as json_file:
    config_dict = json.load(json_file)

print(config_dict)

# extract files from folders with some renaming
for path, subdirs, files in os.walk(r'./source'):
    for filename in files:
        f = os.path.join(path, filename)
        tokens = f.split("/")
        if len(tokens) == 4:
            os.rename(f, os.path.join("./source", tokens[2] + "_" + filename))

folders = list(os.walk("./source"))[1:]

# drop all empty folders in a source dir
for folder in folders:
    if not folder[2]:
        os.rmdir(folder[0])

all_files_unsorted = []
for path, subdirs, files in os.walk(r'./source'):
   for filename in files:
        f = os.path.join(path, filename)
        if os.path.isfile(f):
            if filename in config_dict['filtered_files']:
                print("Needs to be filtered = " + filename)
            else:
                if ".." in str(f) or "'" in str(f) or "«" in str(f) or "»" in str(f):
                    stripped_file_name = f.replace("'","").replace("«","").replace("»","").replace(".....",".").replace("....",".").replace("...",".").replace("..",".")
                    shutil.move(f, stripped_file_name)
                else:
                    stripped_file_name = f
                all_files_unsorted.append(str(stripped_file_name))

sorted_files = natsort.natsorted(all_files_unsorted,reverse=False)

shutil.rmtree(config_dict['dest_folder_name'])
if not os.path.exists(config_dict['dest_folder_name']):
    os.makedirs(config_dict['dest_folder_name'])

a = open(LIST_FILE_NAME, "w")
for f1 in sorted_files:
    a.write("file '" + str(f1) + "'" + os.linesep)
a.close()

a = open(LIST_FILE_NAME, "r")
lines = a.readlines()

lines_array = numpy.array(lines)

last_line = lines_array[-1]

print ("Last line = " + last_line)
if last_line.endswith(os.linesep):
    print("FOUND the end of line")
    lines_array[-1] = last_line[:-1]

a = open(LIST_FILE_NAME, "w")
a.writelines(lines_array)
a.close()

dest_folder_name = config_dict['dest_folder_name']
dest_file_name = config_dict['dest_file_name']

dest_file = os.path.join(config_dict['dest_folder_name'], config_dict['dest_file_name'])

if "true" == config_dict['dry_run_mode']:
    print ("DRY RUN MODE is ON")
else:
    subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", dest_file])

# drop the list file (!)
# os.remove(LIST_FILE_NAME)

audio = MP3(dest_file, ID3=ID3)

try:
    audio.add_tags()
except error:
    pass

audio.tags.add(
    APIC(
        encoding=3, # 3 is for utf-8
        mime='image/jpeg', # image/jpeg or image/png
        type=3, # 3 is for the cover image
        desc=u'Front Cover',
        data=open('./source/' + config_dict['cover_file_name'], 'rb').read()
    )
)
audio.save(v2_version=3)