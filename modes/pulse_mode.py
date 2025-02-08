from modes.mode import Mode
from led_effects.pulse_effect import PulseEffect
from strip import strip
import asyncio


class PulseMode(Mode):
    def __init__(self):
        super().__init__(PulseEffect(strip))
        self.speed = 25

    async def run(self):
        await self._loop(self.led_effect.run, (self.color, self.speed))

    def _on_color_change(self):
        if self.task:
            self.task.close()
