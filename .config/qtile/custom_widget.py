from libqtile import widget, bar, hook, pangocffi
from subprocess import CalledProcessError, Popen, PIPE
import os
import iwlib
# pylint: disable=maybe-no-member


class Volume(widget.Volume):
    def __init__(self, **config):
        widget.base._TextBox.__init__(self, '0', **config)
        self.add_defaults(Volume.defaults)
        self.surfaces = {}
        self.volume = None

    def _update_drawer(self):
        if self.volume == -1:
            self.text = '     '
        elif self.volume == 0:
            self.text = '    {}%'.format(self.volume)
        elif self.volume < 10:
            self.text = '    {}%'.format(self.volume)
        elif self.volume <= 30:
            self.text = '   {}%'.format(self.volume)
        elif self.volume < 80:
            self.text = '   {}%'.format(self.volume)
        elif self.volume < 100:
            self.text = '   {}%'.format(self.volume)
        else:
            self.text = ' {}%'.format(self.volume)


class ThermalSensor(widget.ThermalSensor):
    def poll(self):
        temp_values = self.get_temp_sensors()
        if temp_values is None:
            return False
        text = ""
        if self.show_tag and self.tag_sensor is not None:
            text = self.tag_sensor + ": "
        text += "".join(temp_values.get(self.tag_sensor, ['N/A']))
        temp_value = float(temp_values.get(self.tag_sensor, [0])[0])
        if temp_value > self.threshold:
            self.layout.colour = self.foreground_alert
        else:
            self.layout.colour = self.foreground_normal
        return ' ' + text


def get_status(interface_name):
    interface = iwlib.get_iwconfig(interface_name)
    if 'stats' not in interface:
        return None, None
    quality = interface['stats']['quality']
    essid = bytes(interface['ESSID']).decode()
    return essid, quality


class Wlan(widget.Wlan):
    def poll(self):
        try:
            essid, quality = get_status(self.interface)
            disconnected = essid is None
            if disconnected:
                return ''
            if quality < 20:
                icon = ''
            elif quality < 60:
                icon = ''
            else:
                icon = ''
            return self.format.format(
                essid=essid,
                icon=icon
            )
        except EnvironmentError:
            return


def call_script(path):
    return Popen(
        os.path.expanduser(path),
        shell=True,
        stdout=PIPE,
        universal_newlines=True
    ).communicate()[0].strip()
