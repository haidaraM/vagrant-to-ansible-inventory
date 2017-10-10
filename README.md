# Vagant to Ansible inventory

A simple script to convert `vagrant ssh-config` to an inventory file for Ansible.

## Usage
To use this script, you will need to install [stormssh](https://github.com/emre/storm) (`pip3 install stormssh`), 
a python library to manage your ssh connections.

Inside your vagrant directory, run the script `./vagrant2ansible.py` or `python3 vagrant2ansible.py`. This will create
a filed named `hosts` (Ansible inventory) in the current directory along with a file named `.vagrant-ssh-config` (the 
output of  `vagrant ssh-config`).

## Example
This configuration:
```yaml
Host machine1
  HostName 127.0.0.1
  User vagrant
  Port 2222
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  PasswordAuthentication no
  IdentityFile /home/mha-dw/Projets/ansible/.vagrant/machines/machine1/virtualbox/private_key
  IdentitiesOnly yes
  LogLevel FATAL
Host machine2
  HostName 127.0.0.1
  User vagrant
  Port 2200
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  PasswordAuthentication no
  IdentityFile /home/mha-dw/Projets/ansible/.vagrant/machines/machine2/virtualbox/private_key
  IdentitiesOnly yes
  LogLevel FATAL
Host machine3
```
will be 
```ini
machine1 ansible_host=127.0.0.1 ansible_user=vagrant ansible_ssh_common_args='-o StrictHostKeyChecking=no' ansible_ssh_private_key_file=/home/mha-dw/Projets/ansible/.vagrant/machines/machine1/virtualbox/private_key ansible_port=2222 
machine2 ansible_host=127.0.0.1 ansible_user=vagrant ansible_ssh_common_args='-o StrictHostKeyChecking=no' ansible_ssh_private_key_file=/home/mha-dw/Projets/ansible/.vagrant/machines/machine2/virtualbox/private_key ansible_port=2200
```

**Note that for the moment StrictHostKeyChecking is allays at no in the inventory file.**

## TODO

 - Add some options
 - Compatibility with Python 2 (should be easy to do)
 - Maybe remove the stormssh dependency
 - Test with different Vagrant environments 
 - Put on Pypi

More options will be added. Feel free to contribute.

## Credits

Mohamed El Mouctar HAIDARA
