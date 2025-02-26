import asyncio
from modes.mode_controller import ModeController
from wireless.wifi_manager import WiFiManager


class App:
    def __init__(
        self,
        mode_controller: ModeController,
        wifi_manager: WiFiManager,
    ):
        self.mode_controller = mode_controller
        self.wifi_manager = wifi_manager
        self.connected_to_wifi = False

    async def setup(self):
        wifi_credentials = self.wifi_manager.load_credentials()
        if wifi_credentials:
            try:
                await self.wifi_manager.connect_to_wifi(
                    wifi_credentials["ssid"], wifi_credentials["password"]
                )
                self.connected_to_wifi = True
            except TimeoutError:
                self.connected_to_wifi = False

        if not self.connected_to_wifi:
            self.wifi_manager.start_access_point()

    async def run(self):
        asyncio.create_task(self.mode_controller.run())
        while True:
            await asyncio.sleep(1)
