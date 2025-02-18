import asyncio
from mode_controller import ModeController


class App:
    def __init__(
        self,
        mode_controller: ModeController,
    ):
        self.mode_controller = mode_controller

    async def run(self):
        asyncio.create_task(self.mode_controller.run())
        while True:
            await asyncio.sleep(1)
