import os

VERSION = 'v9015.0.1'
PACKAGE_NAME = "genz_translator"
INTERNAL_REPO_IP = "servers.genzrulez.com"
INTERNAL_REPO_URL = "http://PyPiper:pyisthepiperthatpipesasweetmelody1!@servers.genzrulez.com:8010/simple/"

print ("Hello world, starting the uninstall")

os.system('pip3 --verbose uninstall ' + PACKAGE_NAME + ' -y')

print ("Uninstall done")

