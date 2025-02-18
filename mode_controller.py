from modes.mode import Mode
from modes.filling_mode import FillingMode
from modes.pulse_mode import PulseMode
from modes.rainbow_pulse_mode import RainbowPulseMode
import asyncio


class ModeController:
    modes = {
        "filling": RainbowPulseMode,
        "pulse": PulseMode,
        "rainbow_pulse": FillingMode,
    }
    selected_mode: Mode
    mode_pointer = 0
    task = None

    def __init__(self):
        self.select_mode(self.mode_pointer)

    def select_mode(self, mode_pointer):
        self.mode_pointer = mode_pointer
        self.selected_mode = self.modes[list(self.modes.keys())[self.mode_pointer]]()
        self._on_mode_change()

    def next_mode(self):
        self.mode_pointer = (self.mode_pointer + 1) % len(self.modes)
        self.select_mode(self.mode_pointer)

    def previous_mode(self):
        self.mode_pointer = (self.mode_pointer - 1) % len(self.modes)
        self.select_mode(self.mode_pointer)

    async def run(self):
        while True:
            await self.task()  # type: ignore it works fine

    def _on_mode_change(self):
        if self.task:
            self.task.cancel() # type: ignore it works fine
        self.task = asyncio.create_task(self.selected_mode.run())
