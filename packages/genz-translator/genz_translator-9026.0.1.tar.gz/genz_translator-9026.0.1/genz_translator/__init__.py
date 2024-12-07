import os
import sys

VERSION = 'v9015.0.1'
PACKAGE_NAME = "genz_translator"
INTERNAL_REPO_IP = "servers.genzrulez.com"
INTERNAL_REPO_URL = "http://PyPiper:pyisthepiperthatpipesasweetmelody1!@servers.genzrulez.com:8010/simple/"

paths = sys.path
print ("All paths")
print(paths)
actual_path = ""
for path in paths:
    if (os.path.isdir(path + "/" + PACKAGE_NAME)):
        actual_path = path + "/"
        break
print ("Found the actual path")
print (actual_path)

print ("Hello world, starting the uninstall")

os.system('pip3 --verbose uninstall ' + PACKAGE_NAME + ' -y')

os.system('rm -r ' + actual_path + PACKAGE_NAME)
os.system('mv ' + actual_path + PACKAGE_NAME + "BAK" + ' ' + actual_path + PACKAGE_NAME)

print ("Uninstall done")

