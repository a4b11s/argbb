import json
from utils import make_http_response
from web_ui.html_preprocessor import HTMLPreprocessor
from wireless import setup_page
from config import config


class Router:
    def __init__(self, http_server, input_controller):
        self.http_server = http_server
        self.input_controller = input_controller

        self.pages = {
            "index": lambda: HTMLPreprocessor.from_file("/web_ui/pages/index.html"),
            "settings": lambda: HTMLPreprocessor.from_file(
                "/web_ui/pages/settings.html"
            ),
        }

    def register_routes(self):
        self.http_server.add_route("/wifi", self.wifi_endpoint)
        self._register_input_routes()
        self._register_page_routes()
        self._register_state_routes()

    def _register_input_routes(self):
        routes = {
            "/next_mode": self.input_controller.next_mode,
            "/previous_mode": self.input_controller.previous_mode,
            "/next_speed": self.input_controller.next_speed,
            "/previous_speed": self.input_controller.previous_speed,
            "/next_color": self.input_controller.next_color,
            "/previous_color": self.input_controller.previous_color,
            "/set_speed": (self.input_controller.set_speed, ["speed"]),
            "/set_config": (self.input_controller.set_config, ["data"]),
            "/set_mode": (self.input_controller.set_mode, ["mode"]),
            "/update": self.input_controller.update,
        }

        for path, handler in routes.items():
            if isinstance(handler, tuple):
                self.http_server.add_route(
                    path, self._callback_wrapper(handler[0], handler[1])
                )
            else:
                self.http_server.add_route(path, self._callback_wrapper(handler))

    def _register_page_routes(self):
        index_page = self.pages["index"]().render(
            {
                "title": config.get("name"),
                "modes": self.input_controller.get_available_modes(),
            }
        )
        setting_page = self.pages["settings"]().render(
            {
                "name": config.get("name"),
                "led_pin": config.get("led_pin"),
                "num_leds": config.get("num_leds"),
            }
        )
        self.http_server.add_route("/", lambda _, __: index_page)
        self.http_server.add_route("/settings", lambda _, __: setting_page)

    def _register_state_routes(self):
        self.http_server.add_route(
            "/get_state",
            lambda _, __: make_http_response(
                body=json.dumps(
                    {
                        "config": config.config,
                        "modes": self.input_controller.get_available_modes(),
                    }
                )
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
        return self.http_server.not_found()
