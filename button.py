from machine import Pin

import utime
import asyncio


class Button:
    def __init__(
        self,
        button: Pin,
        short_press_callback=None,
        long_press_callback=None,
        n_press_callback=None,
    ):
        self.button = button
        self._pressed_times = 0
        self._is_pressed = False
        self._has_been_pressed = False
        self._pressed_at = 0
        self._pressed_time = 0
        self._released_at = 0
        self._pressed_times_threshold = 500

        self._debounce_time = 50 / 1000

        self.short_press_callback = short_press_callback or self._noop
        self.long_press_callback = long_press_callback or self._noop
        self.n_press_callback = n_press_callback or self._noop

    def _count_presses(self):
        time_diff = utime.ticks_diff(utime.ticks_ms(), self._released_at)
        if time_diff < self._pressed_times_threshold:
            self._pressed_times += 1
        else:
            self._pressed_times = 0

    @property
    def is_pressed_now(self):
        return self.button.value() == 0

    async def run(self):
        await self._loop()

    async def _loop(self):
        while True:
            # self._debug_log()
            await self._check()

            if self.is_pressed_now:
                await asyncio.sleep(self._debounce_time)
            else:
                await asyncio.sleep(0)

    async def _check(self):
        if self.is_pressed_now and not self._has_been_pressed:
            self._on_press()
        elif not self.is_pressed_now and self._has_been_pressed:
            self._on_release()

    def _on_press(self):
        self._count_presses()

        self._pressed_time = 0
        self._has_been_pressed = True
        self._is_pressed = True
        self._pressed_at = utime.ticks_ms()

    def _on_release(self):
        self._has_been_pressed = False
        self._is_pressed = False
        self._pressed_time = utime.ticks_diff(utime.ticks_ms(), self._pressed_at)
        self._released_at = utime.ticks_ms()
        self._pressed_at = 0

    async def _call_callbacks(self):
        if self._pressed_times == 0:
            if self._pressed_time < 1000:
                self.short_press_callback()
            else:
                self.long_press_callback()
        else:
            self.n_press_callback(self._pressed_times + 1)

    def _check_presses(self):
        if self._pressed_times == 0:
            if self._pressed_time < 1000:
                return "short"
            else:
                return "long"
        else:
            return self._pressed_times + 1

    @staticmethod
    def _noop(*args, **kwargs):
        pass

    def _debug_log(self):
        print(
            f"Pressed: {self._is_pressed}, "
            f"Has been pressed: {self._has_been_pressed}, "
            f"Pressed at: {self._pressed_at}, "
            f"Pressed time: {self._pressed_time}, "
            f"Released at: {self._released_at}, "
            f"Pressed times: {self._pressed_times}"
        )


async def test():
    button = Button(
        Pin(16, Pin.IN, Pin.PULL_UP),
        short_press_callback=lambda: print("Short press"),
        long_press_callback=lambda: print("Long press"),
        n_press_callback=lambda n: print(f"{n} press"),
    )
    asyncio.create_task(button.run())
    while True:
        # print(button._check_presses())
        await asyncio.sleep(1 / 100)


if __name__ == "__main__":
    button = Button(Pin(0, Pin.IN, Pin.PULL_UP))
    asyncio.run(test())
