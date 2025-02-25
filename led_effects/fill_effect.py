from led_effects.effect import Effect


class FillEffect(Effect):
    async def run(self, color, sleep_ms):
        self.strip.fill(color)
        self.strip.write()
