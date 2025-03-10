from led_effects.effect import Effect


class FillEffect(Effect):
    async def _run(self):
        self.strip.fill(self.color)
        self.strip.write()
