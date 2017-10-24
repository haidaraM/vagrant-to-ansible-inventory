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

__version__ = "0.1.1"

# temporary file to store the ssh configuration
TMP_SSH_CONF_FILE_NAME = ".vagrant-ssh-config"
DEFAULT_HOSTS_FILE = "hosts"

red_color = "\033[91m"
green_color = "\033[92m"
orange_color = "\033[93m"
end_color = "\033[0m"


def get_vagrant_ssh_config(verbose=False):
    """
    Get the output of the command 'vagrant ssh-config' as a str
    :param verbose:
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
        print(
            red_color + "[ERROR]: There was an error when executing 'vagrant ssh-config'. See the output below.\n" + end_color,
            file=sys.stderr)
        print(red_color + message + end_color, file=sys.stderr)
        exit(c.returncode)
    except OSError as oe:
        error = "[ERROR]: Verify that vagrant is correctly installed. "
        print(red_color + error + end_color, file=sys.stderr)
        exit(oe.errno)


def write_ssh_config(ssh_config, filename=TMP_SSH_CONF_FILE_NAME, verbose=False):
    """
    Write the ssh config in the given file name
    :param verbose:
    :param filename:
    :param ssh_config: str representing the ssh config
    :return:
    """
    with open(filename, 'w') as f:
        f.write(ssh_config)


def parse_ssh_config(filename=TMP_SSH_CONF_FILE_NAME, verbose=False):
    """
    Parse the ssh config and return it as list of hosts (dict)
    :param verbose:
    :param filename:
    :return: the ssh conf parsed

    """
    parser = ConfigParser(ssh_config_file=filename)
    parser.load()
    return parser.config_data


def write_ansible_inventory(parsed_config, dest_filename, verbose=False):
    """
    Write ansible inventory
    :param verbose:
    :param dest_filename: the filename to write the inventory
    :param parsed_config: the ssh config parsed by stormssh
    :return:
    """
    with open(dest_filename, "w") as f:

        counter = 0

        if verbose:
            print(green_color + "[INFO] Reading the parsed ssh conf..." + end_color)

        for host in parsed_config:
            try:
                # we use the old variables ansible_ssh_user, ansible_ssh_host and ansible_ssh_port to support Ansible < 2.0
                host_line_format = "{host} ansible_ssh_host={hostname} ansible_ssh_user={user} ansible_ssh_common_args='-o StrictHostKeyChecking=no' " \
                                   "ansible_ssh_private_key_file={private_file} ansible_ssh_port={ssh_port} \n".format(
                    host=host['host'], hostname=host['options']['hostname'], user=host['options']['user'],
                    ssh_port=host['options']['port'], private_file=host['options']['identityfile'][0])
                if verbose:
                    print(green_color + "[INFO] Writing host : {}".format(host_line_format) + end_color)

                f.write(host_line_format)

                counter += 1
            except KeyError as ke:
                if verbose:
                    error = orange_color + '[WARNING] Could not find the key {} in the ssh config when writing to the inventory. Skipping...'.format(
                        ke) + end_color
                    print(error, file=sys.stderr)

    if verbose:
        print(green_color + "[INFO] {} host(s) has been successfully writen to '{}'".format(counter,
                                                                                            dest_filename) + end_color)


def main(hosts_filename, verbose=False):
    write_ssh_config(get_vagrant_ssh_config(), verbose=verbose)

    config = parse_ssh_config(verbose=verbose)

    write_ansible_inventory(config, hosts_filename, verbose=verbose)

    try:
        os.remove(TMP_SSH_CONF_FILE_NAME)
    except FileNotFoundError:
        pass


def cli():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("-V", "--version", dest="version", action="store_true", help="Print version and exits")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="Print more information")

    parser.add_argument("hosts_filename", nargs="?", default=DEFAULT_HOSTS_FILE,
                        help="The inventory file name to write hosts to. Default: " + DEFAULT_HOSTS_FILE)

    args = parser.parse_args()

    if args.version:
        print(__version__)
    else:
        main(args.hosts_filename, verbose=args.verbose)


if __name__ == "__main__":
    cli()
