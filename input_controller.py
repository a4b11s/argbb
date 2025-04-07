import asyncio

from wireless import wifi_manager, http_server
from web_ui.web_ui_controller import WebUIController


class InputController:
    def __init__(
        self,
        mode_controller,
        wifi_manager: wifi_manager.WiFiManager,
        http_server: http_server.HTTPServer,
        next_mode_callback=None,
        previous_mode_callback=None,
        next_speed_callback=None,
        previous_speed_callback=None,
        next_color_callback=None,
        previous_color_callback=None,
        set_speed_callback=None,
        update_callback=None,
        set_config_callback=None,
    ):
        self.mode_controller = mode_controller
        self.next_mode_callback = next_mode_callback
        self.previous_mode_callback = previous_mode_callback
        self.next_speed_callback = next_speed_callback
        self.previous_speed_callback = previous_speed_callback
        self.next_color_callback = next_color_callback
        self.previous_color_callback = previous_color_callback
        self.set_speed_callback = set_speed_callback

        self.wifi_manager = wifi_manager
        self.http_server = http_server
        self.update_callback = update_callback
        self.set_config_callback = set_config_callback
        self.web_ui_controller = WebUIController(http_server, self)

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
        if self.next_mode_callback:
            self.next_mode_callback()

    def previous_mode(self):
        if self.previous_mode_callback:
            self.previous_mode_callback()

    def next_speed(self):
        if self.next_speed_callback:
            self.next_speed_callback()

    def previous_speed(self):
        if self.previous_speed_callback:
            self.previous_speed_callback()

    def previous_color(self):
        if self.previous_color_callback:
            self.previous_color_callback()

    def next_color(self):
        if self.next_color_callback:
            self.next_color_callback()

    def set_speed(self, speed):
        if not isinstance(speed, int):
            try:
                speed = int(speed)
            except ValueError:
                return
        if self.set_speed_callback:
            self.set_speed_callback(speed / 10)

    def update(self):
        if self.update_callback:
            self.update_callback()

    def set_config(self, data):
        if self.set_config_callback:
            self.set_config_callback(data)

    def set_mode(self, mode):
        self.mode_controller.select_mode_by_name(mode)
