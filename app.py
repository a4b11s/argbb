import asyncio
from input_controller import InputController
from modes.mode_controller import ModeController
from multicast import broadcast_me
from wireless.http_server import HTTPServer
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
        http_server = HTTPServer()
        self.input_controller = InputController(wifi_manager, http_server, self)

    def setup(self):
        self.input_controller.setup()

    async def run(self):
        asyncio.create_task(self.input_controller.run())
        asyncio.create_task(self.mode_controller.run())
        asyncio.create_task(broadcast_me())
        while True:
            await asyncio.sleep(1)

    def update(self):
        from ota.ota_updater import OTAUpdater
        import gc
        import machine

        try:
            import rp2

            rp2.PIO(0).remove_program()
            rp2.PIO(1).remove_program()
            print("PIO programs removed")
        except Exception as e:
            if e != "Module not found":
                print(f"Error removing PIO programs: {e}")
        del self
        gc.collect()
        print("Updating firmware...")
        otaUpdater = OTAUpdater(
            "https://github.com/a4b11s/argbb",
            main_dir="/",
            exclude_files=["wificred", "/", "config.json"],
        )

        otaUpdater.install_update_if_available()
        del otaUpdater
        machine.reset()

    def set_config(self, data):
        import json
        from config import config
        import machine

        if not isinstance(data, dict):
            data = json.loads(data)

        for key, value in data.items():
            config.set(key, value)

        machine.reset()
