from libqtile.widget.volume import Volume
from libqtile.widget.sensors import ThermalSensor
from libqtile.widget.wlan import Wlan
from libqtile.widget.net import Net
from libqtile.widget import base
import helpers
import requests
import re
import xmltodict


class Volume(Volume):
    def __init__(self, **config):
        base._TextBox.__init__(self, "0", **config)
        self.add_defaults(Volume.defaults)
        self.surfaces = {}
        self.volume = None

    def _update_drawer(self):
        if self.volume == -1:
            self.text = ""
        elif self.volume == 0:
            self.text = " {}%".format(self.volume)
        elif self.volume < 10:
            self.text = " {}%".format(self.volume)
        elif self.volume <= 30:
            self.text = " {}%".format(self.volume)
        elif self.volume < 80:
            self.text = " {}%".format(self.volume)
        elif self.volume < 100:
            self.text = " {}%".format(self.volume)
        else:
            self.text = " {}%".format(self.volume)
        self.text = self.text.center(8)


class ThermalSensor(ThermalSensor):
    def poll(self):
        temp_values = self.get_temp_sensors()
        if temp_values is None:
            return False
        text = ""
        text += "".join(temp_values.get(self.tag_sensor, ["N/A"]))
        temp_value = float(temp_values.get(self.tag_sensor, [0])[0])
        if temp_value > self.threshold:
            self.layout.colour = self.foreground_alert
        else:
            self.layout.colour = self.foreground_normal
        text = " " + re.sub(r"\.\d", "", text)
        return text.center(8)


class Wlan(Wlan):
    def poll(self):
        try:
            vpn = helpers.bash_command(
                "nmcli con show --active | grep -i vpn | awk '{print $3}'"
            )
            if helpers.bash_command(
                "nmcli device status | grep ethernet | grep connected"
            ):
                return self.format.format(essid="", icon=" ", vpn=vpn)
            essid, quality = helpers.get_interface_status(self.interface)
            disconnected = essid is None

            if disconnected:
                return ""
            if quality < 20:
                icon = ""
            elif quality < 60:
                icon = ""
            else:
                icon = ""
            if vpn:
                vpn = " " + vpn
            return self.format.format(essid=essid, icon=icon, vpn=vpn)
        except EnvironmentError:
            return


class Net(Net):
    def _format(self, down, down_letter, up, up_letter):
        down = str(int(down))
        up = str(int(up))
        return down, up

    def poll(self):
        try:
            for intf in self.interface:
                new_stats = self.get_stats()
                down = new_stats[intf]["down"] - self.stats[intf]["down"]
                up = new_stats[intf]["up"] - self.stats[intf]["up"]

                down = down / self.update_interval
                up = up / self.update_interval
                down, down_letter = self.convert_b(down)
                up, up_letter = self.convert_b(up)
                down, up = self._format(down, down_letter, up, up_letter)
                self.stats[intf] = new_stats[intf]
                down = down + down_letter
                up = up + up_letter

            return down.rjust(5) + "  " + up.ljust(5)

        except Exception:
            return


def get_bluetooth():
    result = helpers.bash_script("~/.config/qtile/bluetooth.sh")
    if result == "No devices":
        return "  "
    elif not result:
        return "  "
    else:
        return "  " + result + " "


def get_ex():
    GBP_API_URL = "https://www.dahsing.com/dsb_common/fx/en/FXRateOutput.xml"
    res = requests.get(GBP_API_URL)
    root = xmltodict.parse(res.content)
    gbp = float(root["FxRate"]["FxRateItem"][6]["bankSellHK"])
    return " /" + str(round(gbp, 3)) + " "


def get_im():
    im = helpers.bash_command(
        'if [ $(fcitx5-remote) == "2" ]; then echo ZH; else echo EN; fi'
    )
    enabled = helpers.bash_command(
        'if [ $(cat ~/.keyboard) == "enabled" ]; then echo " "; else echo ; fi'
    )
    return " " + enabled + " " + im + " "


def get_insync():
    status = helpers.bash_command(
        "insync-headless status | grep status | awk '{print $3}'"
    )
    return "  " + status.capitalize() + " "
