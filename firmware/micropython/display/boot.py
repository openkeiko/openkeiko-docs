"""Display-only boot hook with blue-button BOOTSEL entry."""

import machine
import time
from machine import Pin


# GPIO23 is the active-low blue button on the display controller. Configure
# the pull-up before sampling it so a held button is detected during startup.
blue_button = Pin(23, Pin.IN, Pin.PULL_UP)
if blue_button.value() == 0:
    time.sleep_ms(25)
    if blue_button.value() == 0:
        machine.bootloader()
