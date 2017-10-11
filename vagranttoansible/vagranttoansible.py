# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple script to transform 'vagrant ssh-config' output to an inventory hosts for Ansible.

This script must be run in your vagrant folder.
"""

from __future__ import print_function

import subprocess
import sys
import os
import argparse
from storm.parsers.ssh_config_parser import ConfigParser

__version__ = "0.0.2"

DEFAULT_SSH_CONF = ".vagrant-ssh-config"
DEFAULT_HOSTS_FILE = "hosts"


def get_vagrant_ssh_config():
    """
    Get the output of the command 'vagrant ssh-config' as a str
    :return:
    """
    try:
        output = subprocess.check_output(['vagrant', 'ssh-config'], stderr=subprocess.STDOUT)

        config_str = output.decode('utf-8')
        # remove empty lines as they will be interpreted by the ConfigParser
        config_str = os.linesep.join([s for s in config_str.splitlines() if s])
        return config_str
    except subprocess.CalledProcessError as c:
        message = c.output.decode('utf-8')
        print(message, file=sys.stderr)
        exit(c.returncode)
    except OSError as oe:
        print("There was an error when executing the vagrant ssh-config. Verify that vagrant is correctly installed.",
              file=sys.stderr)
        exit(oe.errno)


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
    Parse the ssh config and return it as list of hosts (dict)
    :param filename:
    :return: the ssh conf parsed

    """
    parser = ConfigParser(ssh_config_file=filename)
    parser.load()
    return parser.config_data


def write_ansible_hosts(parsed_config, filename):
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


def main(hosts_filename):
    write_ssh_config(get_vagrant_ssh_config())

    config = parse_ssh_config()

    write_ansible_hosts(config, hosts_filename)


def cli():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("-v", "--version", dest="version", action="store_true", help="Print version and exits")

    parser.add_argument("hosts_filename", nargs="?", default=DEFAULT_HOSTS_FILE,
                        help="The inventory file name to write hosts to.")

    args = parser.parse_args()

    if args.version:
        print(__version__)
    else:
        main(args.hosts_filename)


if __name__ == "__main__":
    cli()
