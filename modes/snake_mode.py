from modes.mode_base import ModeBase

class SnakeMode(ModeBase):
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
    }

    def __init__(self, name, effect, speed_multiplier):
        super().__init__(name, effect, speed_multiplier)

    def apply(self, time_pointer):
        color = self.get_color()
        self.effect.apply(color, time_pointer)
