import os
import shutil


if os.path.exists("dist/"):
    shutil.rmtree("dist/")

if os.path.exists("pycaptions.egg-info/"):
    shutil.rmtree("pycaptions.egg-info/")

if os.path.exists("tmp/"): 
    shutil.rmtree("tmp/")

os.makedirs("tmp/") 
