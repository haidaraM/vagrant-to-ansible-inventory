import os
import pytest

from vagranttoansible import write_ssh_config_to_file, __version__
from vagranttoansible.vagranttoansible import _parse_args


def _read_file(filename):
    with open(filename) as f:
        return f.read()


def test_parse_args_version(capfd):
    """
    Should print the program name and version
    :param capfd:
    :return:
    """
    with pytest.raises(SystemExit):
        _parse_args(['-V'])

    out, err = capfd.readouterr()
    assert out == "vagranttoansible %s\n" % __version__


def test_parse_args_error(capfd):
    """
    Should fail : option provided without a filename
    :param capfd:
    :return:
    """
    with pytest.raises(SystemExit):
        _parse_args(['-o'])


def test_write_ssh_config_to_file():
    ssh_config = 'Host machine3\n'
    filename = 'test.test'
    write_ssh_config_to_file(ssh_config, filename=filename)

    assert os.path.isfile(filename)
    assert ssh_config == _read_file(filename)

    os.remove(filename)
