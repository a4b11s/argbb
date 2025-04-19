import asyncio

from led_effects.effect import Effect


class Mode:
    task = None
    speeds = [25, 10, 5, 1]
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "white": (255, 255, 255),
    }
    _current_color_name = "red"
    self_color_managing = False

    def __init__(self, led_effect: Effect, colors=None, speeds=None):
        if colors:
            self.colors = colors
        if speeds:
            self.speeds = speeds

        self._speed = self.speeds[0]

        self.led_effect = led_effect
        self.color_names = list(self.colors.keys())

    def run(self):
        return self._loop(self.led_effect.run)

    @property
    def color(self):
        return self.colors[self._current_color_name]

    @color.setter
    def color(self, color_name):
        self._current_color_name = color_name
        self._on_color_change()

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value
        self._on_speed_change()

    def _on_speed_change(self):
        self.led_effect.config.update_fields({"sleep_ms": self.speed})

    def _on_color_change(self):
        self.led_effect.config.update_fields({"primary_color": self.color})
        self.led_effect.color_has_changed = True

    def update_mode_config(self, data: dict):
        self.led_effect.config.update_fields(data)

    def get_config(self):
        return self.led_effect.config.get_json()

    async def _loop(self, coroutine):
        while True:
            self.task = coroutine()
            await self.task
            await asyncio.sleep(0)
            self._on_loop_iteration()

    def _on_loop_iteration(self):
        pass
