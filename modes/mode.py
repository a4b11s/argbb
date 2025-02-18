from led_effects.effect import Effect
from utils import calc_pointer

class Mode:
    task = None
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
    _current_color_name = "red"
    self_color_managing = False

    def __init__(self, led_effect: Effect):
        self.led_effect = led_effect
        self.color_names = list(self.colors.keys())

        self.speed = 1

    def run(self):
        raise NotImplementedError("run() not implemented")

    @property
    def color(self):
        return self.colors[self._current_color_name]

    @color.setter
    def color(self, color_name):
        self._current_color_name = color_name
        self._on_color_change()

    def _on_color_change(self):
        self._close_task()

    def _close_task(self):
        if self.task:
            self.task.close()


class MonoColorMode(Mode):
    async def _loop(self, coroutine, args=()):
        while True:
            self.task = coroutine(*args)
            await self.task


class MultiColorMode(Mode):
    _current_color_index = 0
    self_color_managing = True

    def __init__(self, led_effect: Effect):
        super().__init__(led_effect)

    def next_color(self):
        self.current_color_index = calc_pointer(self.current_color_index, 1, len(self.colors))

    async def _loop(self, coroutine, args=()):
        while True:
            self.task = coroutine(self.color, *args)
            await self.task
            self.next_color()

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
