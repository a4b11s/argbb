import asyncio
import gc

from wireless.http_server import HTTPServer
from wireless.wifi_manager import WiFiManager
from web_ui.web_ui_controller import WebUIController
from commands.mode_commands import (
    NextModeCommand,
    PreviousModeCommand,
    SetModeCommand,
    NextSpeedCommand,
    PreviousSpeedCommand,
    NextColorCommand,
    PreviousColorCommand,
    SetSpeedCommand,
)


class InputController:
    def __init__(
        self,
        wifi_manager: WiFiManager,
        http_server: HTTPServer,
        app,
    ):
        self.wifi_manager: WiFiManager = wifi_manager
        self.http_server: HTTPServer = http_server
        self.web_ui_controller: WebUIController = WebUIController(http_server, self)
        self.app = app

        self.command_registry = self._initialize_commands()

    def _initialize_commands(self):
        return {
            "next_mode": NextModeCommand,
            "previous_mode": PreviousModeCommand,
            "next_speed": NextSpeedCommand,
            "previous_speed": PreviousSpeedCommand,
            "next_color": NextColorCommand,
            "previous_color": PreviousColorCommand,
            "set_speed": SetSpeedCommand,
            "set_mode": SetModeCommand,
        }

    def execute_command(self, command_name, *args):
        command = self.command_registry.get(command_name)
        mode_controller = self.app.mode_controller
        if not command:
            raise ValueError("Command not found")

        if args:  # Handle commands requiring arguments
            command = command(mode_controller, *args)
        else:
            command = command(mode_controller)

        command.execute()
        del command
        gc.collect()

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
        self.execute_command("next_mode")

    def previous_mode(self):
        self.execute_command("previous_mode")

    def next_speed(self):
        self.execute_command("next_speed")

    def previous_speed(self):
        self.execute_command("previous_speed")

    def next_color(self):
        self.execute_command("next_color")

    def previous_color(self):
        self.execute_command("previous_color")

    def set_speed(self, speed):
        self.execute_command("set_speed", speed)

    def set_mode(self, mode):
        self.execute_command("set_mode", mode)

    def update(self):
        self.app.update()

    def set_config(self, data):
        self.app.set_config(data)

    def get_available_modes(self):
        return self.app.mode_controller.get_available_modes()
