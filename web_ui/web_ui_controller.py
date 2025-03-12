from wireless import setup_page


class WebUIController:
    def __init__(self, http_server, input_controller):
        self.http_server = http_server
        self.input_controller = input_controller

    async def setup_http_server(self):
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
            "/set_speed",
            self._callback_wrapper(self.input_controller.set_speed, ["speed"]),
        )

        index_page = """
        <html>
            <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                }
                Button {
                    background-color: #4CAF50;
                    border: none;
                    color: white;
                    padding: 15px 32px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                }
                div {
                    width: 100%;
                    display: flex;
                    justify-content: center;
                    border-top: 1px solid #000;
                    padding: 22px;
                }
                .slider {
                    -webkit-appearance: none;
                    width: 100%;
                    height: 25px;
                    background: #d3d3d3;
                    outline: none;
                    opacity: 0.7;
                    -webkit-transition: .2s;
                    transition: opacity .2s;
                }
            </style>
                <title>ARGbb</title>
            </head>
            <body>
                <h1>ARGbb</h1>
                <a href="/wifi">Wifi</a>
                <div>
                <label>Speed:
                <input type="range" min=1" max="2500" value="1250" class="slider" id="speed" onchange="fetch('/set_speed',{method: 'POST',headers: {'Content-Type': 'application/json' }, body: JSON.stringify({speed: this.value})})">
                </label>
                </div>
                <div>
                <button onclick="fetch('/next_mode', {method: 'POST'})">Next Mode</button>
                <button onclick="fetch('/previous_mode', {method: 'POST'})">Previous Mode</button>
                </div>
                <div>
                <button onclick="fetch('/next_speed', {method: 'POST'})">Next Speed</button>
                <button onclick="fetch('/previous_speed', {method: 'POST'})">Previous Speed</button>
                </div>
                <button onclick="fetch('/next_color', {method: 'POST'})">Next Color</button>
            </body>
        </html>        
        """
        self.http_server.add_route("/", lambda method, body: index_page)

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
