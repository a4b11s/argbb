from modes.mode import MonoColorMode
from led_effects.pulse_effect import PulseEffect
from strip import strip


class PulseMode(MonoColorMode):
    def __init__(self):
        super().__init__(PulseEffect(strip))
        self.speed = 25

    async def run(self):
        await self._loop(self.led_effect.run, (self.color, self.speed))
