from led_effects.effect import Effect


class TrainEffect(Effect):
    def __init__(self, strip, car_size=4):
        super().__init__(strip)
        self.car_size = car_size

    async def _run(self):
        for shift in range(self.car_size + 1):
            for i in range(len(self.strip)):
                if (i - shift) % self.car_size == 0:
                    self.strip[i] = (0, 0, 0)
                else:
                    self.strip[i] = self.color
            self.strip.write()

            await self._sleep(self.sleep_ms)
