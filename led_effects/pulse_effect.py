from led_effects.effect import Effect
import asyncio


class PulseEffect(Effect):
    def __init__(self, strip):
        super().__init__(strip)
        self._brightness_steps = 100

    @property
    def brightness_steps(self):
        return self._brightness_steps

    @brightness_steps.setter
    def brightness_steps(self, value):
        self._brightness_steps = value

    async def run(self, color, sleep_ms):
        for i in range(1, self._brightness_steps):
            await self._step(color, i, sleep_ms)
        for i in range(self._brightness_steps, 0, -1):
            await self._step(color, i, sleep_ms)

    def _calculate_brightness(self, color, brightness):
        br_percent = brightness / self._brightness_steps
        return tuple(int(channel * br_percent) for channel in color)

    async def _step(self, color, step, sleep_ms):
        br_color = self._calculate_brightness(color, step)
        self.strip.fill(br_color)
        self.strip.write()
        await self._sleep(sleep_ms)

    async def _sleep(self, sleep_ms):
        await asyncio.sleep(sleep_ms / 1000)
