import random
from led_effects.effect import Effect


class PixelMadnessEffect(Effect):
    write_every = 2
    def _on_color_change(self):
        for j in range(len(self.strip)):
            if self.strip[j] != (0, 0, 0):
                self.strip[j] = self.color

        self.strip.write()
        self.color_has_changed = False

    async def _run(self):
        self.strip.fill((0, 0, 0))
        index_array = list(range(len(self.strip)))
        index_array.sort(key=lambda x: random.random())
        for i in index_array:
            if self.color_has_changed:
                self._on_color_change()

            self.strip[i] = self.color
            if i % self.write_every == 0:
                self.strip.write()
            await self._sleep(self.sleep_ms)
        self.strip.write()
        