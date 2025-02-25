from modes.mode import Mode
import asyncio
from mode_change_strategy import ModeChangeStrategy, DefaultModeChangeStrategy
from speed_change_strategy import SpeedChangeStrategy, DefaultSpeedChangeStrategy


class ModeController:
    selected_mode: Mode
    mode_index = 0
    task = None

    def __init__(
        self,
        modes=None,
        mode_change_strategy: ModeChangeStrategy | None = None,
        speed_change_strategy: SpeedChangeStrategy | None = None,
    ):
        self.modes = modes if modes else {}
        self.mode_change_strategy = (
            mode_change_strategy
            if mode_change_strategy
            else DefaultModeChangeStrategy()
        )
        self.speed_change_strategy = (
            speed_change_strategy
            if speed_change_strategy
            else DefaultSpeedChangeStrategy()
        )
        self.select_mode(self.mode_index)
        self.speed_change_strategy.change_speed(self, 0)

    def change_speed(self, speed_index):
        self.speed_change_strategy.change_speed(self, speed_index)

    def next_speed(self):
        self.speed_change_strategy.next_speed(self)

    def previous_speed(self):
        self.speed_change_strategy.previous_speed(self)

    def set_own_speed(self, speed):
        self.speed_change_strategy.set_own_speed(self, speed)

    def add_mode(self, mode_name, mode):
        self.modes[mode_name] = mode

    def select_mode_by_name(self, mode_name):
        self.mode_change_strategy.select_mode_by_name(self, mode_name)

    def select_mode(self, mode_index):
        self.mode_change_strategy.change_mode(self, mode_index)

    def next_mode(self):
        self.mode_change_strategy.next_mode(self)

    def previous_mode(self):
        self.mode_change_strategy.previous_mode(self)

    def next_color(self):
        self.mode_change_strategy.next_color(self)

    async def run(self):
        while True:
            await self.task  # type: ignore it works fine

    def _on_mode_change(self):
        if self.task:
            self.task.cancel()  # type: ignore it works fine
        self.task = asyncio.create_task(self.selected_mode.run())
