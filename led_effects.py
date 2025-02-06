import neopixel
from config import LED_PIN, NUM_LEDS  # Import configuration


class LedControllerInterface:
    num_leds: int
    pin: int
    pixels: neopixel.NeoPixel

    def fill(self, color):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError


class LedController(LedControllerInterface):
    def __init__(self, pin, num_leds):
        self.pixels = neopixel.NeoPixel(pin, num_leds)
        self.num_leds = num_leds
        self.clear()

    def fill(self, color):
        self.pixels.fill(color)
        self.pixels.write()

    def clear(self):
        self.fill((0, 0, 0))

    def write(self):
        self.pixels.write()

    def __setitem__(self, key, value):
        self.pixels[key] = value  # type: ignore


class BaseEffect:
    def __init__(self, controller: LedControllerInterface):
        self.controller = controller

    def apply(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this method")


class PulseEffect(BaseEffect):
    def apply(self, color, step=0):
        step = self._normalize_step(step)
        color = self._scale_color(color, step)
        self.controller.fill(color)

    def _normalize_step(self, step):
        return step % 512

    def _scale_color(self, color, step):
        step = step if step < 256 else 511 - step
        return tuple(int(c * step / 255) for c in color)


class SnakeEffect(BaseEffect):
    def apply(self, color, length=5, step=0, *args, **kwargs):
        step, backward = self._calculate_step(step, length)
        self.controller.clear()
        self._draw_snake(color, length, step, backward)
        self.controller.write()

    def _calculate_step(self, step, length):
        step = step % (self.controller.num_leds + length)
        backward = step >= self.controller.num_leds
        step = step % self.controller.num_leds
        return step, backward

    def _draw_snake(self, color, length, step, backward):
        for j in range(length):
            index = step - j if not backward else step + j
            if 0 <= index < self.controller.num_leds:
                self.controller[index] = color  # type: ignore


class FillEffect(BaseEffect):
    def apply(self, color, *args, **kwargs):
        self.controller.fill(color)
