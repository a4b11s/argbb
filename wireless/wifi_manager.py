import network
import utime

from wireless.setup_page import SetupPage
from wireless.http_server import HTTPServer


class WiFiManager:
    def __init__(self, hostname: str):
        self.hostname = hostname
        self.ap = self.setup_wifi_access_point(hostname)
        self.sta = self.setup_wifi()

    def setup_wifi(self):
        sta = network.WLAN(network.STA_IF)
        return sta

    def setup_wifi_access_point(self, ssid: str, password: str | None = None):
        ap = network.WLAN(network.AP_IF)
        ap.config(hostname=self.hostname)
        ap.config(essid=ssid)

        if password is not None:
            ap.config(password=password)
            ap.config(security=2)
        else:
            ap.config(security=0)

        return ap

    def connect_to_wifi(
        self, ssid: str, password: str, timeout: int = 20, interval: int = 1
    ):
        self.sta.active(True)
        self.sta.connect(ssid, password)
        start = utime.time()
        while not self.sta.isconnected():
            if utime.time() - start > timeout:
                raise TimeoutError("Connection to WiFi timed out")
            utime.sleep(interval)

        return self.sta.ipconfig()

    def _scan_wifi(self):
        if not self.sta.active():
            self.sta.active(True)
        wlans = self.sta.scan()
        return wlans

    def get_available_wifi(self):
        wlans = self._scan_wifi()
        ssids = self._parse_ssid(wlans)
        return ssids

    @staticmethod
    def _parse_ssid(wlan_list):
        ssids = []
        for wlan in wlan_list:
            ssid = wlan[0].decode("utf-8")

            if not ssid:
                continue

            ssids.append(ssid)
        return ssids
