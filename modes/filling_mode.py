from modes.mode import Mode
from led_effects.filling_effect import FillingEffect
from strip import strip


class FillingMode(Mode):
    def __init__(self):
        super().__init__(FillingEffect(strip))
        self.speed = 25

    async def run(self):
        await self._loop(self.led_effect.run)
