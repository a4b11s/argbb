import network
import socket
import utime
from setup.setup_page import SetupPage


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


class HTTPServer:
    def __init__(self, setup_page) -> None:
        self.setup_page = setup_page

    def host_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
            server.bind(addr)
            server.listen(5)
            while True:
                conn, addr = server.accept()
                print("Got a connection from %s" % str(addr))
                request = conn.recv(1024)
                request = request.decode("utf-8")
                print("Content = %s" % request)
                conn.sendall(self.setup_page.render([{"ssid": "ssid1"}]))
                conn.close()
                # if "ssid" in request:
                #     ssid, password = self._parse_request(request)
                #     wifi_status = self._check_wifi(ssid=ssid, password=password)
                #     # wifi_status = False
                #     if wifi_status:
                #         print("Connected to WiFi, exiting")
                #         break

        except KeyboardInterrupt:
            print("Server stopped")
        finally:
            server.close()

    def _parse_request(self, request):
        ssid = request.split("ssid=")[1].split("&")[0]
        password = request.split("password=")[1].split(" ")[0]
        return ssid, password


if __name__ == "__main__":
    wifi_setup = WiFiSetup("argb")
    http_server = HTTPServer(SetupPage("setup/wifi_setup.html", "setup/wifi_setup.css"))
    http_server.host_server()
