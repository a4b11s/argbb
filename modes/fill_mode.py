from modes.mode_base import ModeBase

class FillMode(ModeBase):
    colors = {
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
    }

    def __init__(self, name, effect, speed_multiplier):
        super().__init__(name, effect, speed_multiplier)

    def apply(self, color, time_pointer):
        self.effect.apply(color, time_pointer)
