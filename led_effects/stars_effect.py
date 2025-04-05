from led_effects.effect import Effect
import random


class StarsEffect(Effect):
    def __init__(self, strip, fade_factor=0.95):
        super().__init__(strip)
        self.fade_factor = fade_factor
        self.sleep_ms = 1000

    def _on_color_change(self, pixels):
        for i in range(len(pixels)):
            if pixels[i] == (0, 0, 0):
                continue
            else:

                old_red = pixels[i][0]

                feed_multiplayer = old_red / 255

                n_r, n_g, n_b = self.color
                pixels[i] = (
                    int(n_r * feed_multiplayer),
                    int(n_g * feed_multiplayer),
                    int(n_b * feed_multiplayer),
                )

        self.color_has_changed = False
        return pixels

    async def _run(self):
        pixels = [(0, 0, 0)] * len(self.strip)
        strip_length = len(self.strip)

        for i in range(strip_length):
            if random.randint(0, 100) < 50:
                continue
            pixels[i] = self._calc_brightness(self.color, random.randint(0, 100))
        self._update_strip(pixels)

        while True:
            if self.color_has_changed:
                pixels = self._on_color_change(pixels)

            if random.randint(0, 100) < 60:
                index = random.randint(0, strip_length - 1)
                new_pixel = self._calc_brightness(self.color, random.randint(50, 100))
                pixels[index] = new_pixel

            self._apply_fade_effect(pixels)
            self._update_strip(pixels)

            await self._sleep(self.sleep_ms)

    def _apply_fade_effect(self, pixels):
        fade_factor = self.fade_factor * 100
        for j in range(len(pixels)):
            
            if random.randint(0, 100) < 20:
                continue
            
            new_pixel = self._calc_brightness(pixels[j], fade_factor)
            pixels[j] = new_pixel

    def _update_strip(self, pixels):
        for k in range(len(self.strip)):
            self.strip[k] = pixels[k]

        self.strip.write()

    def _calc_brightness(self, color, brightness):
        return super()._calc_brightness(color, brightness)


async def main():
    from neopixel import NeoPixel  # Example import, adjust as necessary
    import machine
    import utime

    strip = NeoPixel(machine.Pin(15), 300)  # Example pin and number of LEDs

    strip.fill((255, 0, 0))  # Clear the strip
    strip.write()  # Update the strip
    effect = StarsEffect(strip)

    utime.sleep_ms(2000)  # Wait for 2 seconds
    strip.fill((0, 0, 0))  # Clear the strip again
    strip.write()  # Update the strip

    effect.color = (255, 255, 255)  # Set the color to white
    effect.sleep_ms = 10  # Set the sleep time to 100 ms
    await effect._run()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
