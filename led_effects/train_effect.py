from led_effects.effect import Effect


class TrainEffect(Effect):
    async def _run(self):
        car_size = self.config.get("car_size")
        gap = self.config.get("gap")
        color = self.config.get("primary_color")
        bg_color = self.config.get("bg_color")
        sleep_ms = self.config.get("sleep_ms")
        for shift in range(car_size.value + gap.value):  # type: ignore
            for i in range(len(self.strip)):
                if (i - shift) % (car_size.value + gap.value) < car_size.value:  # type: ignore
                    self.strip[i] = color.value  # type: ignore
                else:
                    self.strip[i] = bg_color.value  # type: ignore
            self.strip.write()

            await self._sleep(sleep_ms.value)  # type: ignore
