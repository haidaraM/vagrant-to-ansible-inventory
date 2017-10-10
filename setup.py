from setuptools import setup, find_packages

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
      packages=find_packages(exclude=['tests']),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
      ],
      entry_points={
          'console_scripts': [
              'vagranttoansible = vagranttoansible.vagranttoansible:main'
          ]
      })
