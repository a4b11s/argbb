from led_effects.effect import Effect


class FillEffect(Effect):
    async def _run(self):
        color = self.config.get("primary_color")
        self.strip.fill(color)
        self.strip.write()
