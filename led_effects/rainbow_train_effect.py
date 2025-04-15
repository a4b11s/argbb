from led_effects.effect import Effect


class RainbowTrainEffect(Effect):
    async def _run(self):
        i = 0

        sleep_ms = self.config.get("sleep_ms")

        while True:
            rainbow = self._generate_rainbow(len(self.strip), i)
            i = i + 1
            for j, color in enumerate(rainbow):
                self.strip[j] = color
            self.strip.write()
            await self._sleep(sleep_ms.value)  # type: ignore

    def _generate_rainbow(self, length, shift=0):
        rainbow = []
        for i in range(length):
            rainbow.append(self._wheel((i + shift) % 256))

        return rainbow

    def _wheel(self, pos):
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)
