from led_effects.effect import Effect


class TrainEffect(Effect):
    def __init__(self, strip, car_size=4):
        super().__init__(strip)
        self.car_size = car_size

    async def _run(self):
        for i in range(self.car_size):
            self.strip.fill(self.color)
            self.strip.write()
            for j in range(0, len(self.strip), self.car_size):
                self.strip[i + j] = (0, 0, 0)
                self.strip.write()
            await self._sleep(self.sleep_ms)
