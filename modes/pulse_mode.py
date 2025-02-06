from modes.mode_base import ModeBase

class PulseMode(ModeBase):
    colors = {
        "white": (255, 255, 255),
        "red": (255, 0, 0),
        "blue": (0, 0, 255),
    }

    def __init__(self, name, effect, speed_multiplier):
        super().__init__(name, effect, speed_multiplier)

    def apply(self, color, time_pointer):
        self.effect.apply(color, time_pointer)
