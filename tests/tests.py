import os
import pytest

from vagranttoansible import write_ssh_config_to_file, parse_ssh_config, __version__
from vagranttoansible.vagranttoansible import get_args


def _read_file(filename):
    """
    Utility function
    :param filename:
    :return:
    """
    with open(filename) as f:
        return f.read()


def test_parse_args_version(capfd):
    """
    Should print the program name and version
    :param capfd:
    :return:
    """
    with pytest.raises(SystemExit):
        get_args(['-V'])

    out, err = capfd.readouterr()
    assert out == "vagranttoansible %s\n" % __version__
    assert err == ''


def test_parse_args_error(capfd):
    """
    Should fail : option provided without a filename
    :return:
    """
    with pytest.raises(SystemExit):
        get_args(['-o'])

    out, err = capfd.readouterr()
    assert out == ''


def test_write_ssh_config_to_file():
    """
    Should write ssh_config to a file
    :return:
    """
    ssh_config = 'Host machine3\n'
    filename = 'test.test'
    write_ssh_config_to_file(ssh_config, filename=filename)

    assert os.path.isfile(filename)
    assert ssh_config == _read_file(filename)

    os.remove(filename)


def test_parse_ssh_config_empty_file():
    """
    Should property parse the ssh configuration with no item
    :return:
    """
    filename = 'data/ssh_config_empty_file'

    config_list = parse_ssh_config(filename)

    assert len(config_list) == 0


def test_parse_ssh_config_simple():
    """
    Should property parse the ssh configuration with only one item
    :return:
    """
    filename = 'data/ssh_config_simple'

    config_list = parse_ssh_config(filename)

    assert len(config_list) == 1

    config = config_list[0]

    assert config['host'] == 'machine1'
    assert config['options']['hostname'] == '127.0.0.1'
    assert config['options']['user'] == 'vagrant'
    assert config['options']['port'] == '2222'
    assert config['options']['userknownhostsfile'] == '/dev/null'
    assert config['options']['stricthostkeychecking'] == 'no'
    assert config['options']['passwordauthentication'] == 'no'

    assert len(config['options']['identityfile']) == 1
    assert config['options']['identityfile'][0] == '/.vagrant/machines/machine1/virtualbox/private_key'

    assert config['options']['identitiesonly'] == 'yes'
    assert config['options']['loglevel'] == 'FATAL'
