import asyncio

from modes.mode import Mode
from modes.mode_change_strategy import DefaultModeChangeStrategy, ModeChangeStrategy
from modes.mode_factory import ModeFactory
from modes.speed_change_strategy import DefaultSpeedChangeStrategy, SpeedChangeStrategy


class ModeController:
    selected_mode: Mode
    mode_index = 0
    task = None

    def __init__(
        self,
        mode_factory: ModeFactory,
        mode_change_strategy: ModeChangeStrategy | None = None,
        speed_change_strategy: SpeedChangeStrategy | None = None,
    ):
        self.mode_factory = mode_factory
        self.mode_change_strategy = (
            mode_change_strategy
            if mode_change_strategy
            else DefaultModeChangeStrategy(self)
        )
        self.speed_change_strategy = (
            speed_change_strategy
            if speed_change_strategy
            else DefaultSpeedChangeStrategy(self)
        )

        self.mode_change_strategy.change_mode(self.mode_index)
        self.speed_change_strategy.change_speed(0)

    def change_speed(self, speed_index):
        self.speed_change_strategy.change_speed(speed_index)

    def next_speed(self):
        self.speed_change_strategy.next_speed()

    def previous_speed(self):
        self.speed_change_strategy.previous_speed()

    def set_own_speed(self, speed):
        self.speed_change_strategy.set_own_speed(speed)

    def select_mode_by_name(self, mode_name):
        self.mode_change_strategy.select_mode_by_name(mode_name)

    def next_mode(self):
        self.mode_change_strategy.next_mode()

    def previous_mode(self):
        self.mode_change_strategy.previous_mode()

    def next_color(self):
        self.mode_change_strategy.next_color()

    def previous_color(self):
        self.mode_change_strategy.previous_color()

    def get_available_modes(self):
        return self.mode_factory.get_available_modes()

    def get_current_mode_config(self):
        return self.selected_mode.get_config()

    def update_mode_config(self, data: dict):
        return self.selected_mode.update_mode_config(data)

    async def run(self):
        while True:
            await self.task  # type: ignore it works fine

    def _on_mode_change(self):
        if self.task:
            self.task.cancel()  # type: ignore it works fine
        self.task = asyncio.create_task(self.selected_mode.run())
