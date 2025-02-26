import network
import utime


class WiFiManager:
    def __init__(self, hostname: str, cred_path: str):
        self.cred_path = cred_path
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

    def load_credentials(self):
        try:
            with open(self.cred_path, "r") as f:
                credentials = f.read()
                credentials = credentials.split("\n")
                return {"ssid": credentials[0], "password": credentials[1]}
        except OSError:
            return None

    def save_credentials(self, ssid: str, password: str):
        with open(self.cred_path, "w") as f:
            f.write(f"{ssid}\n{password}")

    @staticmethod
    def _parse_ssid(wlan_list):
        ssids = []
        for wlan in wlan_list:
            ssid = wlan[0].decode("utf-8")

            if not ssid:
                continue

            ssids.append(ssid)
        return ssids
