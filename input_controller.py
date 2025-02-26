import asyncio
from wireless import wifi_manager, http_server, setup_page


class InputController:
    def __init__(
        self,
        wifi_manager: wifi_manager.WiFiManager,
        http_server: http_server.HTTPServer,
        next_mode_callback=None,
        previous_mode_callback=None,
        next_speed_callback=None,
        previous_speed_callback=None,
        next_color_callback=None,
    ):
        self.next_mode_callback = next_mode_callback
        self.previous_mode_callback = previous_mode_callback
        self.next_speed_callback = next_speed_callback
        self.previous_speed_callback = previous_speed_callback
        self.next_color_callback = next_color_callback

        self.wifi_manager = wifi_manager
        self.http_server = http_server

    async def run(self):
        while True:
            print("Running input controller")
            await self.http_server.host_server()
            await asyncio.sleep(1)

    def synchrony_setup(self):
        asyncio.run(self.setup())

    async def setup(self):
        await self._setup_wifi()
        await self._setup_http_server()

    async def _setup_http_server(self):
        self.http_server.add_route(
            "/wifi",
            self._callback_wrapper(self.set_wifi_credentials, ["ssid", "password"]),
        )
        self.http_server.add_route("/next_mode", self._callback_wrapper(self.next_mode))
        self.http_server.add_route(
            "/previous_mode", self._callback_wrapper(self.previous_mode)
        )
        self.http_server.add_route(
            "/next_speed", self._callback_wrapper(self.next_speed)
        )
        self.http_server.add_route(
            "/previous_speed", self._callback_wrapper(self.previous_speed)
        )
        self.http_server.add_route(
            "/next_color", self._callback_wrapper(self.next_color)
        )
        self.http_server.add_route("/", lambda method, body: "Hello World")

    async def _setup_wifi(self):
        wifi_credentials = self.wifi_manager.load_credentials()
        if wifi_credentials:
            try:
                await self.wifi_manager.connect_to_wifi(
                    wifi_credentials["ssid"], wifi_credentials["password"]
                )
            except TimeoutError:
                self.wifi_manager.start_access_point()
        else:
            self.wifi_manager.start_access_point()

    def _callback_wrapper(self, callback, callback_args_keys=None):
        def wrapper(method, body):
            if method == "POST":
                if callback_args_keys:
                    callback_args = [body[key] for key in callback_args_keys]
                    callback(callback_args)
                else:
                    callback()
                return self.http_server.created({})
            return self.http_server.not_found()

        return wrapper

    def wifi_endpoint(self, method, body):
        if method == "POST":
            self.set_wifi_credentials(body["ssid"], body["password"])
            return self.http_server.created({"message": "Credentials saved"})
        elif method == "GET":
            return setup_page.SetupPage().render(self.wifi_manager.get_available_wifi())
        return self.http_server.not_found

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

    def next_color(self):
        if self.next_color_callback:
            self.next_color_callback()
