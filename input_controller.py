import asyncio

from wireless.http_server import HTTPServer
from wireless.wifi_manager import WiFiManager
from web_ui.web_ui_controller import WebUIController


class InputController:
    def __init__(
        self,
        wifi_manager: WiFiManager,
        http_server: HTTPServer,
        app,
    ):
        self.wifi_manager: WiFiManager = wifi_manager
        self.http_server: HTTPServer = http_server

        self.web_ui_controller = WebUIController(http_server, self)
        self.app = app

    async def run(self):
        await self.http_server.host_server()

    def synchrony_setup(self):
        asyncio.run(self.setup())

    async def setup(self):
        await self._setup_wifi()
        await self.web_ui_controller.setup_http_server()

    async def _setup_wifi(self):
        wifi_credentials = self.wifi_manager.load_credentials()
        if wifi_credentials:
            try:
                await self.wifi_manager.connect_to_wifi(
                    wifi_credentials["ssid"], wifi_credentials["password"]
                )
            except Exception as e:
                print(f"Error connecting to wifi: {e}")
                self.wifi_manager.start_access_point()
        else:
            self.wifi_manager.start_access_point()

    def set_wifi_credentials(self, ssid, password):
        self.wifi_manager.save_credentials(ssid, password)

    def next_mode(self):
        self.app.mode_controller.next_mode()

    def previous_mode(self):
        self.app.mode_controller.previous_mode()

    def next_speed(self):
        self.app.mode_controller.next_speed()

    def previous_speed(self):
        self.app.mode_controller.previous_speed()

    def previous_color(self):
        self.app.mode_controller.previous_color()

    def next_color(self):
        self.app.mode_controller.next_color()

    def set_speed(self, speed):
        if not isinstance(speed, int):
            try:
                speed = int(speed)
            except ValueError:
                return
        self.app.mode_controller.set_own_speed(speed)

    def update(self):
        self.app.update()

    def set_config(self, data):
        self.app.set_config(data)

    def set_mode(self, mode):
        self.app.mode_controller.select_mode_by_name(mode)

    def get_available_modes(self):
        return list(self.app.mode_controller.modes.keys())
