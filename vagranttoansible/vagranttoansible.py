# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Simple script to transform 'vagrant ssh-config' output to an inventory hosts for Ansible
"""
import subprocess
import sys
import os

from storm.parsers.ssh_config_parser import ConfigParser

DEFAULT_SSH_CONF = ".vagrant-ssh-config"


def get_vagrant_ssh_config():
    """
    Get the output of the command 'vagrant ssh-config' as a str
    :return:
    """
    try:
        response = subprocess.run(['vagrant', 'ssh-config'], stdout=subprocess.PIPE, check=True,
                                  stderr=subprocess.PIPE)

        config_str = response.stdout.decode('utf-8')
        # remove empty lines as they will be interpreted by the ConfigParser
        config_str = os.linesep.join([s for s in config_str.splitlines() if s])
        return config_str
    except subprocess.CalledProcessError as c:
        message = c.stderr.decode('utf-8') if len(c.output) == 0 else c.output.decode('utf-8')
        print(message, file=sys.stderr)
        exit(c.returncode)


def write_ssh_config(ssh_config, filename=DEFAULT_SSH_CONF):
    """
    Write the ssh config in the given file name
    :param filename:
    :param ssh_config: str representing the ssh config
    :return:
    """
    with open(filename, 'w') as f:
        f.write(ssh_config)


def parse_ssh_config(filename=DEFAULT_SSH_CONF):
    """
    Parse the ssh config and return it
    :param filename:
    :return:
    """
    parser = ConfigParser(ssh_config_file=filename)
    parser.load()
    return parser.config_data


def write_ansible_hosts(parsed_config, filename="hosts"):
    """
    Write ansible hosts
    :param filename:
    :param parsed_config:
    :return:
    """
    with open(filename, "w") as f:
        for host in parsed_config:
            host_line_format = "{host} ansible_host={hostname} ansible_user={user} ansible_ssh_common_args='-o StrictHostKeyChecking=no' " \
                               "ansible_ssh_private_key_file={private_file} ansible_port={ssh_port} \n".format(
                host=host['host'], hostname=host['options']['hostname'], user=host['options']['user'],
                ssh_port=host['options']['port'], private_file=host['options']['identityfile'][0])
            f.write(host_line_format)


def main():
    write_ssh_config(get_vagrant_ssh_config())

    config = parse_ssh_config()

    write_ansible_hosts(config)


if __name__ == "__main__":
    main()
