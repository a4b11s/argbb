import random

from led_effects.effect import Effect


class LightningBoltEffect(Effect):

    def __init__(
        self,
        strip,
        min_brightness=1,
        max_brightness=100,
        min_await_between_bolts=100,
        max_await_between_bolts=1000,
        min_await_between_flashes=10,
        max_await_between_flashes=50,
        min_flashes=1,
        max_flashes=5,
        min_flashes_time=1,
        max_flashes_time=200,
    ):
        super().__init__(strip)
        self.min_brightness = min_brightness
        self.max_brightness = max_brightness

        self.min_await_between_bolts = min_await_between_bolts
        self.max_await_between_bolts = max_await_between_bolts

        self.min_await_between_flashes = min_await_between_flashes
        self.max_await_between_flashes = max_await_between_flashes

        self.min_flashes = min_flashes
        self.max_flashes = max_flashes

        self.min_flashes_time = min_flashes_time
        self.max_flashes_time = max_flashes_time

    async def _run(self):
        while True:
            self.strip.fill((0, 0, 0))
            self.strip.write()
            await self.random_await(
                self.min_await_between_bolts, self.max_await_between_bolts
            )

            await self.bolt()

    async def bolt(self):
        flashes_count = random.randint(self.min_flashes, self.max_flashes)
        for _ in range(flashes_count):
            color = self.get_random_brightness()
            self.strip.fill(color)
            self.strip.write()
            await self.random_await(self.min_flashes_time, self.max_flashes_time)
            self.strip.fill((0, 0, 0))
            self.strip.write()
            await self.random_await(
                self.min_await_between_flashes, self.max_await_between_flashes
            )

    async def random_await(self, min_ms=100, max_ms=1000):
        random_ms = random.randint(min_ms, max_ms) + self.sleep_ms
        await self._sleep(random_ms)

    def get_random_brightness(self):
        return self._calc_brightness(
            self.color, random.randint(self.min_brightness, self.max_brightness) / 100
        )
