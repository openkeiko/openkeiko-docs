# FW1 Hardware Overview

This page defines the hardware scope used by the OpenKeiko documentation. It covers the original FW1 board with two physical RP2040 processors. It does not apply to later board revisions or other devices that use a different processor architecture.

## Processing roles

FW1 has two independent RP2040s:

| Processor | Primary role | Main responsibilities |
| --- | --- | --- |
| Main RP2040 | I/O and application controller | External header, two sub-GHz radios, FPGA configuration, main USB CDC device, inter-processor link |
| Display RP2040 | User-interface controller | TFT display, buttons, LEDs, audio, microphone, sensors, charger/RTC interface, display USB CDC device |

These are two microcontrollers, not a documented mapping of RP2040 core 0 and core 1. The documentation uses `main RP2040` and `display RP2040` consistently.

Each processor has its own flash device, USB boot path, watchdog, and application USB device. Resetting or flashing one should not be assumed to reset the other.

## Major hardware blocks

| Block | Role | Current evidence |
| --- | --- | --- |
| Main RP2040 | External I/O and application processing | Board definitions, stock-binary analysis, and physical USB/reset tests |
| Display RP2040 | UI and local peripherals | Stock-binary analysis and hardware validation |
| iCE40UP5K FPGA | Routes and processes external digital I/O; can be configured over SPI | Published constraints and recovered programming path |
| USB2513 hub | Presents both RP2040s and the FPGA interface through one external USB connection | Physical USB capture and device identification |
| FT232H-class interface | USB-to-FT1248 path for the FPGA | Published host-driver behavior and USB capture |
| Two CC1101 radios | Sub-GHz radio hardware connected to the main RP2040 | Stock-binary analysis and RF validation |
| 320 x 240 TFT | Display-side SPI peripheral | Stock-binary analysis and display validation |
| Board-interface I2C expander | Controls header directions and radio filter selection | Recovered register map; exact part suffix remains unresolved |
| Charger, RTC, and accelerometer | Display-side I2C peripherals | Device addresses and register behavior recovered; several parts physically identified |

## Data and control paths

- The main RP2040 and display RP2040 communicate over a hardware-flow-controlled UART link at 8 Mbaud.
- The main RP2040 uses SPI0 for the two radios.
- The main RP2040 uses SPI1 for the external I/O path and FPGA configuration.
- The display RP2040 uses SPI1 for the TFT, I2C1 for local sensors and control devices, and PIO engines for audio, LEDs, and the microphone.
- GPIO28 on the main RP2040 is the display RP2040's active-low RUN/reset input. It is a cross-processor control line and must not be pulsed as an incidental part of normal main-side reset or flashing.
- The external 20-pin header has a configurable I/O voltage reference. The reference input must be driven before relying on buffered header I/O.

## Storage and USB

The current board definition uses a 16 MiB flash device for each RP2040. The firmware layout reserves approximately 1 MiB for firmware and 15 MiB for the filesystem on the MicroPython target.

The external USB connection feeds a hub rather than selecting one processor. In normal operation the host can see the main RP2040, display RP2040, and FPGA interface simultaneously. The recovery implications are documented in [Recovery and flashing](recovery-and-flashing.md).

## Evidence status

This overview combines published hardware information, recovered stock-firmware behavior, static analysis, host-side observations, and physical validation. A detailed assignment should be treated according to the evidence label in the [pinout reference](pinout.md), not as an official schematic unless it is explicitly marked `documented`.
