import machine
import network
import utime
import asyncio

from mdns_client import Client  # type: ignore
from mdns_client.responder import Responder  # type: ignore


class WiFiManager:
    def __init__(self, hostname: str, cred_path: str):
        self.cred_path = cred_path
        self.hostname = hostname

        network.hostname(hostname)
        ap_ssid = hostname or machine.unique_id().hex()

        print(f"AP SSID: {ap_ssid}")

        self.ap = self.setup_wifi_access_point(ap_ssid)
        self.sta = self.setup_wifi()

    def setup_wifi(self):
        sta = network.WLAN(network.STA_IF)
        return sta

    def setup_wifi_access_point(self, ssid: str, password: str | None = None):
        ap = network.WLAN(network.AP_IF)
        ap.config(essid=ssid)

        if password is not None:
            ap.config(password=password)
            ap.config(security=2)
        else:
            ap.config(security=0)

        return ap

    def start_access_point(self):
        self.ap.active(True)

    async def connect_to_wifi(
        self, ssid: str, password: str, timeout: int = 20, interval: int = 1
    ):
        self.sta.active(True)
        self.sta.connect(ssid, password)
        start = utime.time()
        print(f"Starting connection to {ssid}...")
        while not self.sta.isconnected():
            print("Connecting to WiFi...")
            if utime.time() - start > timeout:
                raise TimeoutError("Connection to WiFi timed out")
            await asyncio.sleep(interval)

        await self._setup_mdns()

    async def _setup_mdns(self):
        own_ip_address = self.sta.ifconfig()[0]
        client = Client(own_ip_address)
        responder = Responder(
            client,
            own_ip=lambda: own_ip_address,
            host=lambda: self.hostname,
        )

        responder.advertise("_argbb", "_tcp", 80)

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
            with open(
                self.cred_path, "r", encoding="utf-8"
            ) as f:  # Read with UTF-8 encoding
                credentials = f.read().split("\n")
                return {"ssid": credentials[0], "password": credentials[1]}
        except OSError:
            return None

    def save_credentials(self, ssid: str, password: str):
        print(f"Saving credentials: {ssid}, {password}")
        with open(
            self.cred_path, "w", encoding="utf-8"
        ) as f:  # Write with UTF-8 encoding
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
