from led_effects.effect import Effect
import random


class MeteorEffect(Effect):
    def __init__(self, strip):
        super().__init__(strip)
        self.trail_length = 50
        self.fade_factor = (0.8, 0.9)
        self.spark_probability = 0.1

    async def run(self, color, sleep_ms):
        NUM_PIXELS = len(self.strip)
        pixels = [(0, 0, 0)] * NUM_PIXELS

        for i in range(NUM_PIXELS + self.trail_length):
            if i < NUM_PIXELS:
                pixels[i] = color

            self._apply_fade_effect(pixels)
            self._update_strip(pixels)

            await self._sleep(sleep_ms)

    def _apply_fade_effect(self, pixels):
        for j in range(len(pixels)):
            is_spark = random.random() < self.spark_probability
            fade_multiplayer = random.uniform(*self.fade_factor)

            if is_spark:
                fade_multiplayer = 1 + 1 - fade_multiplayer

            r, g, b = pixels[j]
            pixels[j] = (
                int(r * fade_multiplayer),
                int(g * fade_multiplayer),
                int(b * fade_multiplayer),
            )

    def _update_strip(self, pixels):
        # pixels = pixels.reverse()

        for k in range(len(self.strip)):
            self.strip[k] = pixels[k]
        self.strip.write()
