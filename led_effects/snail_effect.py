from led_effects.effect import Effect


class SnailEffect(Effect):
    async def _run(self):
        color = self.config.get("primary_color")
        sleep_ms = self.config.get("sleep_ms")
        tail_length = self.config.get("tail_length")
        bg_color = self.config.get("bg_color")
        self.strip.fill(bg_color.value)  # type: ignore
        for i in range(tail_length.value, len(self.strip)):  # type: ignore
            for j in range(tail_length.value):  # type: ignore
                index = i - j
                if index < 0:
                    continue
                self.strip[index] = color.value  # type: ignore

            self.strip[i - tail_length.value] = self._calc_brightness(color.value, 0.05)  # type: ignore

            self.strip.write()
            await self._sleep(sleep_ms.value) # type: ignore
