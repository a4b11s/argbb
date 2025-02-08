from modes.filling_mode import FillingMode
from strip import strip
from modes.pulse_mode import PulseMode
import asyncio
import utime

BUTTON_PIN_NUMBER = 16
STRIP_PIN_NUMBER = 15
NUM_LEDS = 60

strip.fill((0, 0, 0))
strip.write()

pm = PulseMode()
fm = FillingMode()

async def work_emulator():
    while True:
        time = utime.ticks_ms()
        await asyncio.sleep(1)
        print(f"Work time: {utime.ticks_diff(utime.ticks_ms(), time)}")


async def main():
    asyncio.create_task(work_emulator())
    asyncio.create_task(fm.run())
    x = 0
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
