from led_effects.effect import Effect


class FillingEffect(Effect):
    def _on_color_change(self, indx):
        for j in range(indx):
            self.strip[j] = self.color
        self.strip.write()
        self.color_has_changed = False

    async def _run(self):
        self.strip.fill((0, 0, 0))
        for i in range(len(self.strip)):

            if self.color_has_changed:
                self._on_color_change(i)

            self.strip[i] = self.color
            await self._sleep(self.sleep_ms)
            self.strip.write()
