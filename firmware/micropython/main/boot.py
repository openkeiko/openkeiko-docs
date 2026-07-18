"""Early main-controller initialization for FW1."""

from machine import Pin


# GPIO28 is the display RP2040's active-low RUN input. Keep it high so main
# startup, reset, watchdog recovery, and UF2 deployment do not reset display.
display_run = Pin(28, Pin.OUT, value=1)
