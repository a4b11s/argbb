from led_effects.effect import Effect, EffectConfig


class DoubleSnakeEffect(Effect):
    async def _run(self):
        color = self.config.get("primary_color")
        sleep_ms = int(self.config.get("sleep_ms"))
        tail_length = int(self.config.get("tail_length"))
        bg_color = self.config.get("bg_color")
        for i in range(len(self.strip)):
            self.strip.fill(bg_color)
            for j in range(tail_length):
                first_index = i + j
                second_index = len(self.strip) - i - j - 1
                if first_index >= len(self.strip):
                    continue
                if second_index < 0:
                    continue
                self.strip[first_index] = color
                self.strip[second_index] = color

            self.strip.write()
            await self._sleep(sleep_ms)
