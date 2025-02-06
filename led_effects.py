import neopixel
from config import LED_PIN, NUM_LEDS  # Import configuration


class LedController:
    def __init__(self, pin=LED_PIN, num_leds=NUM_LEDS):  # Use default config values
        self.pixels = neopixel.NeoPixel(pin, num_leds)
        self.num_leds = num_leds
        self.clear()

    def fill(self, color):
        self.pixels.fill(color)
        self.pixels.write()

    def clear(self):
        self.fill((0, 0, 0))


class BaseEffect:
    def __init__(self, controller: LedController):
        self.controller = controller

    def apply(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this method")


class PulseEffect(BaseEffect):
    def apply(self, color, step=0):
        # Normalize step to be within 0-511
        step = step % 512
        # Reflect step to create a pulsing effect
        step = step if step < 256 else 511 - step
        # Scale color by the step value
        color = tuple(int(c * step / 255) for c in color)
        self.controller.fill(color)


class SnakeEffect(BaseEffect):
    def apply(self, color, length=5, step=0, *args, **kwargs):
        step = step % (self.controller.num_leds + length)
        backward = step >= self.controller.num_leds
        step = step % self.controller.num_leds
        self.controller.clear()
        for j in range(length):
            index = step - j if not backward else step + j
            if 0 <= index < self.controller.num_leds:
                self.controller.pixels[index] = color # type: ignore
        self.controller.pixels.write()

class FillEffect(BaseEffect):
    def apply(self, color, *args, **kwargs):
        self.controller.fill(color)