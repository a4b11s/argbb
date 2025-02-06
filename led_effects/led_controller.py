import neopixel


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
