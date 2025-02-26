import network
import utime
from wireless.setup_page import SetupPage
from wireless.http_server import HTTPServer

class WiFiSetup:
    def __init__(self, hostname: str):
        self.hostname = hostname
        self.ap = self.setup_wifi_access_point(hostname)
        self.ap.active(True)

    def _check_wifi(
        self, ssid: str, password: str, timeout: int = 20, interval: int = 1
    ):
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        sta.connect(ssid, password)
        start = utime.time()
        print("Connecting to WiFi")
        while not sta.isconnected():
            print("connecting...")
            if utime.time() - start > timeout:
                print("connection timeout")
                return False
            print("not connected")
            utime.sleep(interval)
        print("Connected")
        print(sta.ifconfig())
        return True

    def _scan_wifi(self):
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        wlans = sta.scan()
        sta.active(False)
        return wlans

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


if __name__ == "__main__":
    wifi_setup = WiFiSetup("argb")
    sp = SetupPage("setup/wifi_setup.html", "setup/wifi_setup.css")
    http_server = HTTPServer()

    http_server.add_route(
        "/",
        lambda _, __: sp.render(wifi_setup.get_available_wifi()),
    )
    http_server.host_server()
