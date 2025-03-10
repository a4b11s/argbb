from led_effects.effect import Effect


class DoubleSnakeEffect(Effect):
    def __init__(self, strip, tail_length=8):
        super().__init__(strip)
        self.tail_length = tail_length

    async def _run(self):
        for i in range(len(self.strip)):
            self.strip.fill((0, 0, 0))
            for j in range(self.tail_length):
                first_index = i + j
                second_index = len(self.strip) - i - j - 1
                if first_index >= len(self.strip):
                    continue
                if second_index < 0:
                    continue
                self.strip[first_index] = self.color
                self.strip[second_index] = self.color

            self.strip.write()
            await self._sleep(self.sleep_ms)
