from modes.snake_mode import SnakeMode
from modes.fill_mode import FillMode
from modes.pulse_mode import PulseMode
from modes.rainbow_pulse_mode import RainbowPulseMode
from led_effects.fill_effect import FillEffect
from led_effects.pulse_effect import PulseEffect
from led_effects.snake_effect import SnakeEffect


class ModeController:
    def __init__(self, controller):
        self.modes = [
            RainbowPulseMode("Rainbow Pulse", PulseEffect(controller), 10),
            FillMode("Fill", FillEffect(controller), 10),
            PulseMode("Pulse", PulseEffect(controller), 10),
        ]
        self.mode_pointer = 0

    def get_current_mode(self):
        return self.modes[self.mode_pointer]

    def change_mode(self):
        self.mode_pointer = (self.mode_pointer + 1) % len(self.modes)
