import neopixel
from .config import LED_PIN, NUM_LEDS  # Import configuration


class LedEffects:
    def __init__(self, pin=LED_PIN, num_leds=NUM_LEDS):  # Use default config values
        self.pixels = neopixel.NeoPixel(pin, num_leds)
        self.num_leds = num_leds
        self.pixels.fill((0, 0, 0))
        self.pixels.write()

    def fill(self, color):
        self.pixels.fill(color)
        self.pixels.write()

    def pulse_step(self, color, step=0):
        # Normalize step to be within 0-511
        step = step % 512
        # Reflect step to create a pulsing effect
        step = step if step < 256 else 511 - step
        # Scale color by the step value
        color = tuple(int(c * step / 255) for c in color)
        self.fill(color)

    def snake(self, color, length=5, step=0, background=(0, 0, 0)):
        if length > self.num_leds:
            raise ValueError("Length should be less than the number of LEDs")
        if isinstance(color, list) and len(color) != length:
            raise ValueError("Length of color list should be equal to length")

        # Calculate the maximum index for the snake movement
        max_index = (self.num_leds - length + 1) * 2
        step = step % max_index

        self.pixels.fill(background)
        forward = step <= self.num_leds - length
        for i in range(length):
            index = self._calculate_index(i, length, step, forward)
            if isinstance(color, tuple):
                self.pixels[index] = color  # type: ignore
            elif isinstance(color, list):
                self.pixels[index] = color[i]  # type: ignore
        self.pixels.write()

    def _calculate_index(self, i, length, step, forward):
        if forward:
            return step + i
        else:
            return self.num_leds - step - i - 1

    def clear(self):
        self.fill((0, 0, 0))
