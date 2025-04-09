import asyncio

from led_effects.effect import Effect
from utils import calc_pointer


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
        self.led_effect.set_sleep_ms(self.speed)

    def _on_color_change(self):
        self.led_effect.set_color(self.color)

    async def _loop(self, coroutine):
        while True:
            self.task = coroutine(self.color, self.speed)
            await self.task
            await asyncio.sleep(0)
            self._on_loop_iteration()

    def _on_loop_iteration(self):
        pass


class MultiColorMode(Mode):
    _current_color_index = 0
    self_color_managing = True

    def __init__(self, led_effect: Effect):
        super().__init__(led_effect)

    def _on_loop_iteration(self):
        self.next_color()

    def next_color(self):
        self.current_color_index = calc_pointer(
            self.current_color_index, 1, len(self.colors)
        )

    @property
    def current_color_index(self):
        return self._current_color_index

    @current_color_index.setter
    def current_color_index(self, value):
        self._current_color_index = value
        self._on_color_change()

    @property
    def color(self):
        return self.colors[self.color_names[self.current_color_index]]

    @color.setter
    def color(self, color_name):
        self._current_color_index = self.color_names.index(color_name)
        self._on_color_change()
