class ModeBase:
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "white": (255, 255, 255),
    }

    def __init__(self, name, effect, speed_multiplier):
        self.name = name
        self.effect = effect
        self.speed_multiplier = speed_multiplier
        self.speed_modes = [1, 1 / 2, 1 / 4]
        self.speed_pointer = 0
        self.speed = self.get_speed()

        self.colors_list = list(self.colors.values())
        self.colors_pointer = 0

    def _calculate_speed(self):
        return self.speed_modes[self.speed_pointer] * self.speed_multiplier

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def change_speed(self):
        self.speed_pointer = (self.speed_pointer + 1) % len(self.speed_modes)
        self.speed = self._calculate_speed()

    def get_color(self):
        return self.colors_list[self.colors_pointer]

    def change_color(self):
        self.colors_pointer = self._calculate_colors_pointer()

    def _calculate_colors_pointer(self):
        return (self.colors_pointer + 1) % len(self.colors_list)

    def apply(self, color, time_pointer):
        raise NotImplementedError("Subclasses should implement this method")
