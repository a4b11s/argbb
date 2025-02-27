from led_effects import effect

class OffEffect(effect.Effect):
    async def run(self, color, sleep_ms):
        self.strip.fill((0, 0, 0))
        self.strip.write()
        await self._sleep(sleep_ms)