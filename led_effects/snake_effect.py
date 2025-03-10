from led_effects.effect import Effect


class SnakeEffect(Effect):
    def __init__(self, strip, tail_length=4):
        super().__init__(strip)
        self.tail_length = tail_length

    async def _run(self):
        for i in range(len(self.strip)):
            self.strip.fill((0, 0, 0))
            for j in range(self.tail_length):
                index = i + j
                if index >= len(self.strip):
                    continue
                self.strip[index] = self.color
            self.strip.write()
            await self._sleep(self.sleep_ms)
