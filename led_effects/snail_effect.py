from led_effects.effect import Effect


class SnailEffect(Effect):
    def __init__(self, strip, tail_length=4):
        super().__init__(strip)
        self.tail_length = tail_length
        self.sleep_ms = 1000

    async def _run(self):
        self.strip.fill((0, 0, 0))
        for i in range(self.tail_length, len(self.strip)):
            for j in range(self.tail_length):
                index = i - j
                if index < 0:
                    continue
                self.strip[index] = self.color

            for j in range(0, i - self.tail_length):
                index = j
                if index >= len(self.strip):
                    continue
                self.strip[index] = self._calc_brightness(self.color, 0.05)
            self.strip.write()
            await self._sleep(self.sleep_ms)
