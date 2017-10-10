# Vagant to Ansible inventory

A simple script to convert `vagrant ssh-config` to an inventory file for Ansible.

## Usage
To use this script, you will need to install [stormssh](https://github.com/emre/storm) (`pip3 install stormssh`), 
a python library to manage your ssh connections.

Inside your vagrant directory, run the script `./vagrant2ansible.py` or `python3 vagrant2ansible.py`. This will create
a filed named `hosts` (Ansible inventory) in the current directory along with a file named `.vagrant-ssh-config` (the 
output of  `vagrant ssh-config`).

More options will be added. Feel free to contribute.

## TODO

 - Add some options
 - Compatibility with Python 2 (should be easy to do)
 - Maybe remove the stormssh dependency
 - Test with different Vagrant environments 
 - Put on Pypi

## Credits

Mohamed El Mouctar HAIDARA
