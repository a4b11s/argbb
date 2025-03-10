from led_effects import effect

class OffEffect(effect.Effect):
    async def _run(self):
        self.strip.fill((0, 0, 0))
        self.strip.write()
        await self._sleep(self.sleep_ms)