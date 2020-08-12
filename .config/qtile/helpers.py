from subprocess import Popen, PIPE
import os
import iwlib


def get_interface_status(interface_name):
    interface = iwlib.get_iwconfig(interface_name)
    if 'stats' not in interface:
        return None, None
    quality = interface['stats']['quality']
    essid = bytes(interface['ESSID']).decode()
    return essid, quality


def _bash(arg):
    return Popen(
        arg,
        shell=True,
        stdout=PIPE
    ).communicate()[0].decode('utf-8').strip()


def bash_script(path):
    return _bash(os.path.expanduser(path))


def bash_command(command):
    return _bash(command)


def get_interface():
    return bash_command("nmcli device status | grep wifi | awk '{print $1}' | sed 1q")
