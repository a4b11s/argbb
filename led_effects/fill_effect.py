from led_effects.effect import Effect
import asyncio


class FillEffect(Effect):
    async def run(self, color, sleep_ms):
        self.strip.fill(color)
        self.strip.write()
        await self._sleep(sleep_ms)
