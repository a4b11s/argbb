import neopixel


class LedEffects:
    def __init__(self, pin, num_leds):
        self.pixels = neopixel.NeoPixel(pin, num_leds)
        self.num_leds = num_leds
        self.pixels.fill((0, 0, 0))
        self.pixels.write()

    def fill(self, color):
        self.pixels.fill(color)
        self.pixels.write()

    def pulse_step(self, color, pointer=0):
        processed_pointer = pointer % 512

        processed_pointer = (
            processed_pointer if processed_pointer < 256 else 511 - processed_pointer
        )

        color = tuple(map(lambda x: int(x * processed_pointer / 255), color))
        self.fill(color)

    def snake(
        self,
        color,
        length=5,
        pointer=0,
        background=(0, 0, 0),
    ):
        if length > self.num_leds:
            raise ValueError("Length should be less than the number of LEDs")
        if isinstance(color, list) and len(color) != length:
            raise ValueError("Length of color list should be equal to length")

        index_max = self.num_leds - length + 1
        index_max *= 2
        processed_pointer = int(pointer % index_max)

        self.pixels.fill(background)
        if processed_pointer <= self.num_leds - length:
            self._snake_forward(color, length, processed_pointer)
        else:
            self._snake_backward(color, length, processed_pointer)
        self.pixels.write()

    def _snake_forward(self, color, length, processed_pointer):
        self._snake_common(color, length, processed_pointer, forward=True)

    def _snake_backward(self, color, length, processed_pointer):
        self._snake_common(color, length, processed_pointer, forward=False)

    def _snake_common(self, color, length, processed_pointer, forward):
        for j in range(length):
            if forward:
                index = processed_pointer + j
            else:
                index = (
                    self.num_leds - (processed_pointer - (self.num_leds - length)) + j
                )
            if isinstance(color, tuple):
                self.pixels[index] = color  # type: ignore
            elif isinstance(color, list):
                self.pixels[index] = color[j]  # type: ignore

    def clear(self):
        self.fill((0, 0, 0))
