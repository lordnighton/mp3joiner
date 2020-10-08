import os
import shutil

if os.path.isdir("./dest"):
    shutil.rmtree("./dest")

if os.path.isdir("./source"):
    shutil.rmtree("./source")

os.mkdir("./dest")
os.mkdir("./source")