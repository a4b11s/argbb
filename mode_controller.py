from modes.mode import Mode
from modes.filling_mode import FillingMode
from modes.pulse_mode import PulseMode
from modes.rainbow_pulse_mode import RainbowPulseMode
import asyncio
from utils import calc_pointer


class ModeController:
    modes = {
        "filling": FillingMode,
        "pulse": PulseMode,
        "rainbow_pulse": RainbowPulseMode,
    }
    selected_mode: Mode
    mode_pointer = 0
    task = None

    _color_pointer = 0

    def __init__(self):
        self.select_mode(self.mode_pointer)

    def select_mode_by_name(self, mode_name):
        if mode_name in self.modes:
            mode_pointer = list(self.modes.keys()).index(mode_name)
            self.select_mode(mode_pointer)
        else:
            raise ValueError(f"Mode '{mode_name}' not found in available modes.")

    def select_mode(self, mode_pointer):
        self.mode_pointer = mode_pointer
        self.selected_mode = self.modes[list(self.modes.keys())[self.mode_pointer]]()
        self._on_mode_change()

    def next_mode(self):
        mode_pointer = calc_pointer(self.mode_pointer, 1, len(self.modes))
        self.select_mode(mode_pointer)

    def previous_mode(self):
        mode_pointer = calc_pointer(self.mode_pointer, -1, len(self.modes))
        self.select_mode(mode_pointer)

    def next_color(self):
        if self.selected_mode.self_color_managing:
            return
        self._color_pointer = calc_pointer(
            self._color_pointer, 1, len(self.selected_mode.color_names)
        )
        self.selected_mode.color = self.selected_mode.color_names[self._color_pointer]

    async def run(self):
        while True:
            await self.task  # type: ignore it works fine

    def _on_mode_change(self):
        if self.task:
            self.task.cancel()  # type: ignore it works fine
        self.task = asyncio.create_task(self.selected_mode.run())
