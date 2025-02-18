from machine import Pin

import utime
import asyncio


class Button:
    def __init__(self, button: Pin):
        self.button = button
        self._pressed_times = 0
        self._is_pressed = False
        self._has_been_pressed = False
        self._pressed_at = 0
        self._pressed_time = 0
        self._released_at = 0
        self._pressed_times_threshold = 500

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
            await self._check()
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

    def _check_presses(self):
        if self._pressed_times == 0:
            if self._pressed_time < 1000:
                return "short"
            else:
                return "long"
        else:
            return self._pressed_times + 1
