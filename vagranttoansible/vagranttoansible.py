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

__version__ = "1.0.0"

# temporary file to store the ssh configuration
TMP_SSH_CONF_FILE_NAME = ".vagrant-ssh-config"
DEFAULT_OUTPUT = "stdout"

DEFAULT_LINE_FORMAT = "{host} ansible_ssh_host={ssh_hostname} ansible_ssh_user={user} ansible_ssh_common_args='-o StrictHostKeyChecking={stricthostkeychecking}' " \
                      "ansible_ssh_private_key_file={private_file} ansible_ssh_port={ssh_port}"

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


def write_ansible_inventory(parsed_config, output_file_name, verbose=False):
    """
    Write ansible inventory
    :param verbose:
    :param output_file_name: the filename to write the inventory
    :param parsed_config: the ssh config parsed by stormssh
    :return:
    """

    hosts_list = []

    counter = 0

    if verbose:
        print(green_color + "[INFO] Reading the parsed ssh conf..." + end_color)

    for host_config in parsed_config:
        try:

            ssh_host = host_config['host']
            port = host_config['options']['port']
            user = host_config['options']['user']
            ssh_hostname = host_config['options']['hostname']
            identityfile = host_config['options']['identityfile'][0]
            strict_host_keychecking = host_config['options']['stricthostkeychecking']

            # we use the old variables ansible_ssh_user, ansible_ssh_host and ansible_ssh_port to support Ansible < 2.0
            host_line_format = DEFAULT_LINE_FORMAT.format(host=ssh_host, ssh_hostname=ssh_hostname, user=user,
                                                          ssh_port=port, private_file=identityfile,
                                                          stricthostkeychecking=strict_host_keychecking)
            if verbose:
                print(green_color + "[INFO] Writing host : {}".format(host_line_format) + end_color)

            hosts_list.append(host_line_format)

            counter += 1
        except KeyError as ke:
            if verbose:
                error = orange_color + '[WARNING] Could not find the key {} in the ssh config when writing to the inventory. Skipping...'.format(
                    ke) + end_color
                print(error, file=sys.stderr)

    if output_file_name == DEFAULT_OUTPUT:
        print("\n".join(hosts_list))
    else:
        with open(output_file_name, "w") as f:
            for ansible_inventory_line in hosts_list:
                f.write(ansible_inventory_line)
                f.write("\n")

    if verbose:
        print(green_color + "[INFO] {} host(s) has been successfully writen to '{}'".format(counter,
                                                                                            output_file_name) + end_color)


def main(hosts_filename, verbose=False):
    write_ssh_config(get_vagrant_ssh_config(), verbose=verbose)

    config = parse_ssh_config(verbose=verbose)

    write_ansible_inventory(config, hosts_filename, verbose=verbose)

    try:
        os.remove(TMP_SSH_CONF_FILE_NAME)
    except FileNotFoundError:
        pass


def cli():
    parser = argparse.ArgumentParser(description=__doc__, prog="vagranttoansible")

    parser.add_argument("-V", "--version", dest="version", action="version", version='%(prog)s ' + __version__,
                        help="Print version and exits")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="Print more information")

    parser.add_argument("-o", "--output-file-name", dest="output_file_name", default=DEFAULT_OUTPUT,
                        help="The inventory file name to write hosts to. Default: " + DEFAULT_OUTPUT)

    args = parser.parse_args()

    main(args.output_file_name, verbose=args.verbose)


if __name__ == "__main__":
    cli()
