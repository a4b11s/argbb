from web_ui.router import Router


class WebUIController:
    def __init__(self, http_server, input_controller):
        self.http_server = http_server
        self.input_controller = input_controller
        self.router = Router(
            http_server,
            input_controller,
        )

    def setup_http_server(self):
        self.router.register_routes()
