from strip import strip
import asyncio
import utime
from mode_controller import ModeController

BUTTON_PIN_NUMBER = 16
STRIP_PIN_NUMBER = 15
NUM_LEDS = 60

mode_controller = ModeController()


async def change_mode():
    while True:
        await asyncio.sleep(4)
        print("Changing mode")
        mode_controller.next_mode()


async def work_emulator():
    while True:
        time = utime.ticks_ms()
        await asyncio.sleep(1)
        print(f"Work time: {utime.ticks_diff(utime.ticks_ms(), time)}")


async def main():
    asyncio.create_task(work_emulator())
    asyncio.create_task(mode_controller.run())
    asyncio.create_task(change_mode())
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    strip.fill((0, 0, 0))
    strip.write()

    utime.sleep_ms(500)
    asyncio.run(main())
