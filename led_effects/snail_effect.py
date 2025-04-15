from led_effects.effect import Effect


class SnailEffect(Effect):
    async def _run(self):
        color = self.config.get("primary_color")
        sleep_ms = int(self.config.get("sleep_ms"))
        tail_length = int(self.config.get("tail_length"))
        bg_color = self.config.get("bg_color")
        self.strip.fill(bg_color)
        for i in range(tail_length, len(self.strip)):
            for j in range(tail_length):
                index = i - j
                if index < 0:
                    continue
                self.strip[index] = color

            self.strip[i - tail_length] = self._calc_brightness(color, 0.05)

            self.strip.write()
            await self._sleep(sleep_ms)
