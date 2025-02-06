from modes.mode_base import ModeBase
from led_effects.fill_effect import FillEffect
from led_effects.pulse_effect import PulseEffect
from led_effects.snake_effect import SnakeEffect

class ModeController:
    def __init__(self, controller):
        self.modes = [
            ModeBase("Snake", SnakeEffect(controller), 100),
            ModeBase("Fill", FillEffect(controller), 10),
            ModeBase("Pulse", PulseEffect(controller), 10),
        ]
        self.speed_modes = [1, 1 / 2, 1 / 4]
        self.mode_pointer = 0
        self.speed_pointer = 0

    def get_current_mode(self):
        return self.modes[self.mode_pointer]

    def get_speed(self):
        return (
            self.speed_modes[self.speed_pointer]
            * self.modes[self.mode_pointer].speed_multiplier
        )

    def change_speed(self):
        self.speed_pointer = (self.speed_pointer + 1) % len(self.speed_modes)

    def change_mode(self):
        self.mode_pointer = (self.mode_pointer + 1) % len(self.modes)
