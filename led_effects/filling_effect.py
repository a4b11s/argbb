from led_effects.effect import Effect


class FillingEffect(Effect):
    async def run(self, color, sleep_ms):
        self.strip.fill((0, 0, 0))
        for i in range(len(self.strip)):
            self.strip[i] = color
            await self._sleep(sleep_ms)
            self.strip.write()
