import neopixel
import utime


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

        processed_pointer = pointer % (self.num_leds + length)

        self.pixels.fill(background)
        if processed_pointer < self.num_leds:
            for j in range(length):
                indx = processed_pointer + j
                if isinstance(color, tuple):
                    self.pixels[indx] = color # type: ignore
                elif isinstance(color, list):
                    self.pixels[indx] = color[j] # type: ignore
        else:
            for j in range(length):
                indx = processed_pointer - j
                if isinstance(color, tuple):
                    self.pixels[indx] = color # type: ignore
                elif isinstance(color, list):
                    self.pixels[indx] = color[j] # type: ignore
        self.pixels.write()

    # def snake(self, color, duration, length=5, background=(0, 0, 0), reverse=False):
    # if length > self.num_leds:
    #     raise ValueError("Length should be less than the number of LEDs")
    # if not isinstance(color, tuple) and not isinstance(color, list):
    #     raise ValueError("Color should be a tuple or a list of tuples")
    # if isinstance(color, list) and len(color) != length:
    #     raise ValueError("Length of color list should be equal to length")
    # if not isinstance(background, tuple):
    #     raise ValueError("Background should be a tuple")

    #     range_first = (
    #         range(self.num_leds - length)
    #         if not reverse
    #         else range(self.num_leds - 1, length - 1, -1)
    #     )

    #     for i in range_first:
    #         if reverse and i < length:
    #             break

    #         if not reverse and i + length > self.num_leds:
    #             break

    #         self.fill(background)
    #         for j in range(length):
    #             indx = i + j if not reverse else i - j

    #             if isinstance(color, tuple):
    #                 self.pixels[indx] = color  # type: ignore
    #             elif isinstance(color, list):
    #                 self.pixels[indx] = color[j]  # type: ignore

    #         self.pixels.write()
    #         utime.sleep_ms(duration)
    #     self.fill(background)

    def clear(self):
        self.fill((0, 0, 0))
