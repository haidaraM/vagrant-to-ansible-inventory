from setuptools import setup

try:
    long_description = open('README.md').read()
except:
    long_description = None

setup(name="vagranttoansible",
      version="0.0.1",
      description="Simple script to transform 'vagrant ssh-config' output to an inventory hosts for Ansible",
      url="https://github.com/haidaraM/vagranttoansibleinventory",
      author="HAIDARA Mohamed El Mouctar",
      author_email="elmhaidara@gmail.com",
      license="MIT",
      install_requires=['stormssh'],
      entry_points={
          'console_scripts': [
              'vagranttoansible = vagranttoansible.vagranttoansible:main'
          ]
      })
