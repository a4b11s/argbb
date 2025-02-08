from led_effects.effect import Effect


class Mode:
    speed: int = 1
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "white": (255, 255, 255),
    }

    current_color_name = "red"

    def __init__(self, led_effect: Effect):
        self.led_effect = led_effect

        self.speed = 1

    def run(self):
        raise NotImplementedError("run() not implemented")

    @property
    def color(self):
        return self.colors[self.current_color_name]

    @color.setter
    def color(self, color_name):
        self.current_color_name = color_name
        self._on_color_change()

    def _on_color_change(self):
        pass
