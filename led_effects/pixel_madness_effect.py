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
        index_array = self._get_index_array()
        for i in index_array:
            self._apply(self.color, i)
            await self._sleep(self.sleep_ms)
        self.strip.write()

    def _apply(self, color, i):
        if self.color_has_changed:
            self._on_color_change()

        self.strip[i] = color
        if i % self.write_every == 0:
            self.strip.write()

    def _get_index_array(self):
        index_array = list(range(len(self.strip)))
        index_array.sort(key=lambda x: random.random())
        return index_array


class PixelMadnessBiDirectEffect(PixelMadnessEffect):
    async def _run(self):
        self.strip.fill((0, 0, 0))
        index_array = self._get_index_array()
        for i in index_array:
            self._apply(self.color, i)
            await self._sleep(self.sleep_ms)
        for i in reversed(index_array):
            self._apply((0, 0, 0), i)
            await self._sleep(self.sleep_ms)
