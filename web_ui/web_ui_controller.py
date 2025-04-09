from web_ui.router import Router
from web_ui.html_preprocessor import HTMLPreprocessor


class WebUIController:
    def __init__(self, http_server, input_controller):
        self.http_server = http_server
        self.input_controller = input_controller
        self.router = Router(
            http_server,
            input_controller,
        )

    async def setup_http_server(self):
        self.router.register_routes()
