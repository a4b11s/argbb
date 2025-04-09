import json
from utils import make_http_response
from wireless import setup_page
from web_ui.html_preprocessor import HTMLPreprocessor
from config import config


class WebUIController:
    def __init__(self, http_server, input_controller):
        self.http_server = http_server
        self.input_controller = input_controller

        self.index_page = HTMLPreprocessor.from_file("/web_ui/pages/index.html")
        self.setting_page = HTMLPreprocessor.from_file("/web_ui/pages/settings.html")

    async def setup_http_server(self):
        config_data = config.config
        modes_list = self.input_controller.get_available_modes()

        self.http_server.add_route("/wifi", self.wifi_endpoint)
        self.http_server.add_route(
            "/next_mode", self._callback_wrapper(self.input_controller.next_mode)
        )
        self.http_server.add_route(
            "/previous_mode",
            self._callback_wrapper(self.input_controller.previous_mode),
        )
        self.http_server.add_route(
            "/next_speed", self._callback_wrapper(self.input_controller.next_speed)
        )
        self.http_server.add_route(
            "/previous_speed",
            self._callback_wrapper(self.input_controller.previous_speed),
        )
        self.http_server.add_route(
            "/next_color", self._callback_wrapper(self.input_controller.next_color)
        )
        self.http_server.add_route(
            "/previous_color",
            self._callback_wrapper(self.input_controller.previous_color),
        )
        self.http_server.add_route(
            "/set_speed",
            self._callback_wrapper(self.input_controller.set_speed, ["speed"]),
        )
        self.http_server.add_route(
            "/update",
            self._callback_wrapper(self.input_controller.update),
        )
        self.http_server.add_route(
            "/set_config",
            self._callback_wrapper(self.input_controller.set_config, ["data"]),
        )

        self.http_server.add_route(
            "/set_mode",
            self._callback_wrapper(self.input_controller.set_mode, ["mode"]),
        )

        index_page = self.index_page.render(
            {"title": config.get("name"), "modes": modes_list}
        )

        setting_page = self.setting_page.render(
            {
                "name": config.get("name"),
                "led_pin": config.get("led_pin"),
                "num_leds": config.get("num_leds"),
            }
        )

        self.http_server.add_route("/", lambda _, __: index_page)
        self.http_server.add_route("/settings", lambda _, __: setting_page)
        self.http_server.add_route(
            "/get_state",
            lambda _, __: make_http_response(
                body=json.dumps({"config": config_data, "modes": modes_list})
            ),
        )

    def _callback_wrapper(self, callback, callback_args_keys=None):
        def wrapper(method, body):
            if method == "POST":
                if callback_args_keys:
                    callback_args = [body[key] for key in callback_args_keys]
                    callback(*callback_args)
                else:
                    callback()
                return self.http_server.created({})
            return self.http_server.not_found()

        return wrapper

    def wifi_endpoint(self, method, body):
        if method == "POST":
            self.input_controller.set_wifi_credentials(body["ssid"], body["password"])
            return self.http_server.created({"message": "Credentials saved"})
        elif method == "GET":
            return setup_page.SetupPage().render(
                self.input_controller.wifi_manager.get_available_wifi()
            )
        return self.http_server.not_found
