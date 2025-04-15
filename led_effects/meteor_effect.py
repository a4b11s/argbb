import random

from led_effects.effect import Effect


class MeteorEffect(Effect):
    def _on_color_change(self, pixels, indx):
        color = self.config.get("primary_color")

        for i in range(indx if indx < len(pixels) else len(pixels)):
            if pixels[i] == (0, 0, 0):
                continue
            else:

                old_red = pixels[i][0]

                feed_multiplayer = old_red / 255

                n_r, n_g, n_b = color
                pixels[i] = (
                    int(n_r * feed_multiplayer),
                    int(n_g * feed_multiplayer),
                    int(n_b * feed_multiplayer),
                )

        self.color_has_changed = False
        return pixels

    async def _run(self):
        color = self.config.get("primary_color")
        tail_length = self.config.get("tail_length")
        sleep_ms = int(self.config.get("sleep_ms"))
        pixels = [(0, 0, 0)] * len(self.strip)

        for i in range(len(self.strip) + tail_length):
            if self.color_has_changed:
                pixels = self._on_color_change(pixels, i)

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

        fade_factor = self.config.get("fade_factor")
        spark_probability = self.config.get("spark_probability")

        fade_multiplayer = random.uniform(*fade_factor)

        if random.random() < spark_probability:
            fade_multiplayer = 2 - fade_multiplayer

        return fade_multiplayer

    def _update_strip(self, pixels):
        for k in range(len(self.strip)):
            self.strip[k] = pixels[k]

        self.strip.write()
