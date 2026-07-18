# FW1 Recovery and Flashing

This page records the observed USB and boot behavior needed to identify the correct processor and avoid flashing the wrong target. It is a hardware reference, not a recommendation to overwrite a device before a backup and recovery plan exist.

## Before changing firmware

1. Confirm that the board is the FW1 dual-RP2040 hardware.
2. Save the current main and display images and record their hashes.
3. Capture the normal USB topology and note the hub port or physical location of each device.
4. Keep a known-good cable, host toolchain, and a way to interrupt or recover a failed application.
5. Treat the main and display images as separate targets. They are not interchangeable.

## Normal USB topology

The external connector feeds a USB2513 three-port hub. Normal enumeration is:

| Hub port | Device | VID:PID | Flashing role |
| ---: | --- | --- | --- |
| 1 | Main RP2040 application | `093c:2054` | Main firmware |
| 2 | Display RP2040 application | `093c:2055` | Display firmware |
| 3 | FT232H connected to the FPGA | `0403:6014` | FPGA interface; not an RP2040 flasher |

The hub itself identifies as `0424:2513`.

The main and display application devices each expose a CDC channel and a vendor reset interface. Opening the selected CDC device at 1200 baud and closing it requests that same processor to enter the RP2040 ROM bootloader.

## ROM bootloader behavior

Both RP2040s use the same ROM bootloader identity:

- VID:PID: `2e8a:0003`
- Volume: `RPI-RP2`

After both processors enter BOOTSEL, VID/PID and ROM serial information are insufficient to select a target. Use the stable hub port or physical USB location. Port 1 is main; port 2 is display.

The observed update order is display first, then main. A replacement updater should preserve target selection by hub location and wait for each processor to re-enumerate before proceeding.

The button-triggered boot path exposes the `RPI-RP2` UF2 mass-storage volume but does not expose the Picoboot interface. Flashing through this path means copying the intended `.uf2` file to the mounted volume; `picotool` cannot be used here.

## Button paths

### Red button

With the controller powered off and disconnected from USB, hold red while plugging in USB. Release it after the main RP2040 appears as `RPI-RP2` on hub port 1. This produces immediate main-RP2040 BOOTSEL. A direct hardware route to the main QSPI boot strap is the leading explanation, but continuity testing is still needed before documenting that as proven circuitry.

### Blue button

With the controller powered off and disconnected from USB, hold blue while plugging in USB. Release it after the display RP2040 appears as `RPI-RP2` on hub port 2.

The stock display application reads blue as an active-low input on display GPIO23. It shows a bootloader prompt, stores a RAM flag, and calls the RP2040 `reset_usb_boot` routine. This is an application-mediated display recovery path, not a confirmed direct hardware BOOTSEL strap.

A replacement MicroPython display boot hook must configure GPIO23 as `Pin.IN` with `Pin.PULL_UP` before sampling it, then call `machine.bootloader()` while the input is held low. GPIO23 is the main controller's FPGA clock, so the two controllers require separate boot hooks. The display-specific implementation lives at `firmware/micropython/display/boot.py`, and the main reset-protection hook lives at `firmware/micropython/main/boot.py`.

## Cross-processor reset

Main GPIO28 is the display RP2040's active-low RUN input. A pulse on this line disconnects and re-enumerates the display USB device. It must not be pulsed as a side effect of:

- Main application startup
- Main software reset
- Main watchdog recovery
- Main BOOTSEL entry or return
- Main UF2 flashing

The safer default is to hold GPIO28 high and leave it released. Any deliberate display reset should be an explicit, guarded operation.

## Watchdog recovery

Each processor can run its own hardware watchdog. A local watchdog reset should briefly remove only that processor's USB device and then return it on the same hub port. A missing peer device during a local reset is a regression to investigate rather than normal behavior.

For an unresponsive application, wait for the target processor's watchdog and USB re-enumeration before power cycling. Record the selected hub port, serial, reset cause, and last host operation if recovery fails.

## Safe flashing sequence

A target-aware flashing tool should:

1. Select one application device by VID/PID plus hub port or fixed serial.
2. Enter BOOTSEL on that processor only.
3. Confirm that exactly one `RPI-RP2` volume appeared at the same hub port.
4. Copy only the image intended for that processor to the root of the volume.
5. Wait for the volume to unmount and the same application identity to return.
6. Repeat for the other processor if a complete update is intended.
7. Confirm that both application devices and the FPGA interface are present afterward.

Do not match a ROM device by VID/PID alone, do not use `picotool` on this UF2-only path, and do not treat the FT232H as an RP2040 target.

## Flash layout

The current board configuration uses a 16 MiB flash device per RP2040. The MicroPython target reserves approximately 1 MiB for firmware and 15 MiB for the filesystem. Verify the exact image and layout for the build being flashed; do not assume that a filesystem image or firmware image is interchangeable between processors.

## Recovery gaps

The following points remain incomplete and should be resolved before calling the recovery map final:

- Continuity proof for the red-button route to main QSPI `CSn`
- Any secondary hardware route for blue in addition to display GPIO23
- Exact USB hub strap/EEPROM configuration
- Whether board revisions alter button, power, or boot wiring
- A tested recovery path for a processor that does not return after watchdog timeout
