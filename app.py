import asyncio
from input_controller import InputController
from modes.mode_controller import ModeController
from multicast import broadcast_me
from wireless.wifi_manager import WiFiManager


class App:
    def __init__(
        self,
        mode_controller: ModeController,
        wifi_manager: WiFiManager,
        input_controller: InputController,
    ):
        self.mode_controller = mode_controller
        self.wifi_manager = wifi_manager
        self.connected_to_wifi = False
        self.input_controller = input_controller

    def synchrony_setup(self):
        self.input_controller.synchrony_setup()

    async def setup(self):
        await self.input_controller.setup()

    async def run(self):
        asyncio.create_task(self.input_controller.run())
        asyncio.create_task(self.mode_controller.run())
        asyncio.create_task(broadcast_me())
        while True:
            await asyncio.sleep(1)
