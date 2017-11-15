from setuptools import setup, find_packages
from vagranttoansible.vagranttoansible import __version__

try:
    long_description = open('README.md').read()
except:
    long_description = None

setup(name="vagranttoansible",
      version=__version__,
      description="Simple script to transform 'vagrant ssh-config' output to an inventory hosts for Ansible",
      long_description=long_description,
      url="https://github.com/haidaraM/vagranttoansibleinventory",
      author="HAIDARA Mohamed El Mouctar",
      author_email="elmhaidara@gmail.com",
      license="MIT",
      install_requires=['stormssh==0.6.9'],
      tests_requires=['pytest'],
      packages=find_packages(exclude=['tests']),
      download_url="https://github.com/haidaraM/vagranttoansibleinventory/archive/v" + __version__ + ".tar.gz",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 2.7',
      ],
      entry_points={
          'console_scripts': [
              'vagranttoansible = vagranttoansible.vagranttoansible:cli'
          ]
      })
