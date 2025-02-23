import network
import socket
import utime
import machine


class WiFiSetup:
    def __init__(self, hostname: str):
        self.hostname = hostname
        self.page = self._setup_page()
        self.ap = self.setup_wifi_spot(hostname)
        self.ap.active(True)
        print("WiFi AP started")

    def _check_wifi(
        self, ssid: str, password: str, timeout: int = 20, interval: int = 1
    ):
        print("Connecting to WiFi")
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        sta.connect(ssid, password)
        start = utime.time()
        print("Started connection at ", start)
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
        sta.deinit()
        return wlans

    def setup_wifi_spot(self, ssid: str):
        ap = network.WLAN(network.AP_IF)
        ap.config(hostname=self.hostname)
        ap.config(essid=ssid)
        ap.config(security=0)
        return ap

    def host_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
            server.bind(addr)
            server.listen(5)
            print(f"Server started at {self.ap.ifconfig()}")
            while True:
                conn, addr = server.accept()
                print("Got a connection from %s" % str(addr))
                request = conn.recv(1024)
                request = request.decode("utf-8")
                print("Content = %s" % request)
                conn.sendall(self.page)
                conn.close()
                if "ssid" in request:
                    ssid, password = self._parse_request(request)
                    wifi_status = self._check_wifi(ssid=ssid, password=password)
                    # wifi_status = False
                    if wifi_status:
                        print("Connected to WiFi, exiting")
                        break

        except KeyboardInterrupt:
            print("Server stopped")
        finally:
            server.close()

    def _parse_request(self, request):
        ssid = request.split("ssid=")[1].split("&")[0]
        password = request.split("password=")[1].split(" ")[0]
        return ssid, password

    def _setup_page(self):
        ssid_list = [ssid[0].decode("utf-8") for ssid in self._scan_wifi()]

        select_options = "".join(
            [f'<option value="{wifi}">{wifi}</option>' for wifi in ssid_list]
        )

        css = """
        <style>
            body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
            color: #333;
            }
            .container {
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            }
            h1 {
            text-align: center;
            color: #4CAF50;
            }
            label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            }
            input, select {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
            }
            button {
            width: 100%;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            }
            button:hover {
            background-color: #45a049;
            }
            @media (max-width: 600px) {
            .container {
                width: 90%;
                margin: 20px auto;
                padding: 10px;
            }
            h1 {
                font-size: 24px;
            }
            button {
                font-size: 14px;
            }
            }
            </style>"""

        html = f"""<!DOCTYPE html>
        <html>
        <head>
            {css}
            <title>WiFi Setup</title>
            <meta charset="utf-8">
            <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
            <meta http-equiv="content-type" content="application/json; charset=utf-8" />
        </head>
        <body>
            <div class="container">
                <h1>WiFi Setup</h1>
                <form action="/connect" method="post">
                    <label for="ssid">SSID:</label>
                    <select id="ssid" name="ssid">
                    {select_options}
                    </select>
                    <label for="password">Password:</label>
                    <input type="text" id="password" name="password" required>
                    <button type="submit">Connect</button>
                </form>
            </div>
        </body>
        </html>
        """
        return html


if __name__ == "__main__":
    wifi_setup = WiFiSetup("argb")
    # print(wifi_setup._scan_wifi())
    wifi_setup.host_server()
