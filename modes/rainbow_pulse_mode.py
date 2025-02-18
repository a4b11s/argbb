from modes.mode import MultiColorMode
from led_effects.pulse_effect import PulseEffect
from strip import strip


class RainbowPulseMode(MultiColorMode):
    def __init__(self):
        super().__init__(PulseEffect(strip))
        self.speed = 25

    async def run(self):
        await self._loop(self.led_effect.run)
