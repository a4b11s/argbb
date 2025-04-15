from led_effects.effect import Effect, EffectConfig


class DoubleSnakeEffect(Effect):
    async def _run(self):
        color = self.config.get("primary_color")
        sleep_ms = self.config.get("sleep_ms")
        tail_length = self.config.get("tail_length")
        bg_color = self.config.get("bg_color")

        for i in range(len(self.strip)):
            self.strip.fill(bg_color.value)  # type: ignore
            for j in range(tail_length.value):  # type: ignore
                first_index = i + j
                second_index = len(self.strip) - i - j - 1
                if first_index >= len(self.strip):
                    continue
                if second_index < 0:
                    continue
                self.strip[first_index] = color.value  # type: ignore
                self.strip[second_index] = color.value  # type: ignore

            self.strip.write()
            await self._sleep(sleep_ms.value)  # type: ignore
