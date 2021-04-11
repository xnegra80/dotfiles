from libqtile.widget.volume import Volume
from libqtile.widget.sensors import ThermalSensor
from libqtile.widget.wlan import Wlan
from libqtile.widget.net import Net
from libqtile.widget import base
from pycoingecko import CoinGeckoAPI
import helpers
import requests
import re
import datetime
import xmltodict
import sys


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
            self.text = ""
        elif self.volume < 10:
            self.text = ""
        elif self.volume <= 30:
            self.text = ""
        elif self.volume < 80:
            self.text = ""
        elif self.volume < 100:
            self.text = ""
        else:
            self.text = ""


class ThermalSensor(ThermalSensor):
    def poll(self):
        temp_values = self.get_temp_sensors()
        if temp_values is None:
            return False
        text = " "
        text += "".join(temp_values.get(self.tag_sensor, ["N/A"]))
        temp_value = float(temp_values.get(self.tag_sensor, [0])[0])
        if temp_value > self.threshold:
            self.layout.colour = self.foreground_alert
        else:
            self.layout.colour = self.foreground_normal
        text = re.sub(r"\.\d", "", text)
        return text.center(4)


class Wlan(Wlan):
    def poll(self):
        try:
            vpn = helpers.bash_command(
                "nmcli con show --active | grep -i vpn | awk '{print $3}'"
            )
            if helpers.bash_command(
                "nmcli device status | grep ethernet | grep connected"
            ):
                return self.format.format(essid="", icon="", vpn=vpn)
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

            return down.rjust(5) + "" + up.ljust(5)

        except Exception:
            return


def get_spotify():
    status = helpers.bash_command("playerctl status")
    if not status == "Playing":
        return ""
    else:
        artist = helpers.bash_command("playerctl metadata xesam:artist")
        title = helpers.bash_command("playerctl metadata xesam:title")
        title = re.sub(r" \([^()]*\)", "", title)
        return f" {artist} - {title}"


def get_crypto():
    cryptos = dict(
        btc="bitcoin",
        eth="ethereum",
        bnb="binancecoin",
        ada="cardano",
        cro="crypto-com-chain",
        nexo="nexo",
        cake="pancakeswap-token",
        bifi="beefy-finance",
        kebab="kebab-token",
        btd="bolt-true-dollar",
        watch="yieldwatch",
        salt="saltswap",
        safemoon="safemoon",
    )

    try:
        cg = CoinGeckoAPI()
        symbol = list(cryptos.keys())[datetime.datetime.now().minute % len(cryptos)]
        crypto = cryptos[symbol]

        price = cg.get_price(
            ids=crypto, vs_currencies="hkd", include_24hr_change="true"
        )
        price, change = price[crypto]["hkd"], price[crypto]["hkd_24h_change"]
        if change > 0:
            change = "+" + str(round(change, 1))
        else:
            change = str(round(change, 1))
        return symbol.upper() + ":$" + str(price) + " " + change + "%"
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message + crypto


def get_ex():
    try:
        GBP_API_URL = "https://www.dahsing.com/dsb_common/fx/en/FXRateOutput.xml"
        res = requests.get(GBP_API_URL)
        root = xmltodict.parse(res.content)
        gbp = float(root["FxRate"]["FxRateItem"][6]["bankSellHK"])
        return " " + str(round(gbp, 3))
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message


def get_im():
    im = helpers.bash_command(
        'if [ $(fcitx5-remote) == "2" ]; then echo ZH; else echo EN; fi'
    )
    enabled = helpers.bash_command(
        'if [ $(cat ~/.keyboard) == "enabled" ]; then echo ""; else echo ; fi'
    )
    return enabled + im
