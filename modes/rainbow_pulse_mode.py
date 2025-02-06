from modes.mode_base import ModeBase


class RainbowPulseMode(ModeBase):
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
    }

    def __init__(self, name, effect, speed_multiplier):
        super().__init__(name, effect, speed_multiplier)
        self.color_changed = False
        
    def apply(self, time_pointer):
        color = self.get_color()
        if self.effect._normalize_step(time_pointer) >= 0 and self.effect._normalize_step(time_pointer) < 10 and not self.color_changed:
            self.colors_pointer = self._calculate_colors_pointer()           
            self.color_changed = True
            
        if self.effect._normalize_step(time_pointer) >= 100:
            self.color_changed = False
        
        self.effect.apply(color, time_pointer)

    def change_color(self):
        pass