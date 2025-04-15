import random

from led_effects.effect import Effect


class LightningBoltEffect(Effect):

    async def _run(self):
        while True:

            min_await_between_bolts = self.config.get("min_await_between_bolts")
            max_await_between_bolts = self.config.get("max_await_between_bolts")

            self.strip.fill((0, 0, 0))
            self.strip.write()
            await self.random_await(min_await_between_bolts.value, max_await_between_bolts.value)  # type: ignore

            await self.bolt()

    async def bolt(self):
        min_flashes = int(self.config.get("min_flashes").value)  # type: ignore
        max_flashes = int(self.config.get("max_flashes").value)  # type: ignore
        min_flashes_time = int(self.config.get("min_flashes_time").value)  # type: ignore
        max_flashes_time = int(self.config.get("max_flashes_time").value)  # type: ignore

        min_await_between_flashes = int(
            self.config.get("min_await_between_flashes").value  # type: ignore
        )
        max_await_between_flashes = int(
            self.config.get("max_await_between_flashes").value  # type: ignore
        )

        flashes_count = random.randint(min_flashes, max_flashes)
        for _ in range(flashes_count):
            color = self.get_random_brightness()
            self.strip.fill(color)
            self.strip.write()
            await self.random_await(min_flashes_time, max_flashes_time)
            self.strip.fill((0, 0, 0))
            self.strip.write()
            await self.random_await(
                min_await_between_flashes, max_await_between_flashes
            )

    async def random_await(self, min_ms=100, max_ms=1000):
        random_ms = random.randint(min_ms, max_ms)
        await self._sleep(random_ms)

    def get_random_brightness(self):
        min_brightness = int(self.config.get("min_brightness").value)  # type: ignore
        max_brightness = int(self.config.get("max_brightness").value)  # type: ignore
        color = self.config.get("primary_color").value  # type: ignore
        return self._calc_brightness(
            color, random.randint(min_brightness, max_brightness) / 100
        )
