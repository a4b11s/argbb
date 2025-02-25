from led_effects.effect import Effect
import random


class MeteorEffect(Effect):
    def __init__(self, strip, trail_length=50, fade_factor=(0.7, 0.9), spark_probability=0.1):
        super().__init__(strip)
        self.trail_length = 50
        self.fade_factor = fade_factor
        self.spark_probability = spark_probability

    async def run(self, color, sleep_ms):
        pixels = [(0, 0, 0)] * len(self.strip)

        for i in range(len(self.strip) + self.trail_length):
            if i < len(self.strip):
                pixels[i] = color

            self._apply_fade_effect(pixels)
            self._update_strip(pixels)

            await self._sleep(sleep_ms)

    def _apply_fade_effect(self, pixels):
        for j in range(len(pixels)):

            fade_multiplayer = self._calc_fade_multiplayer()

            r, g, b = pixels[j]
            pixels[j] = (
                int(r * fade_multiplayer),
                int(g * fade_multiplayer),
                int(b * fade_multiplayer),
            )

    def _calc_fade_multiplayer(self):
        fade_multiplayer = random.uniform(*self.fade_factor)

        if random.random() < self.spark_probability:
            fade_multiplayer = 2 - fade_multiplayer

        return fade_multiplayer

    def _update_strip(self, pixels):
        for k in range(len(self.strip)):
            self.strip[k] = pixels[k]

        self.strip.write()
