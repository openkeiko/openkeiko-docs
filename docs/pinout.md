# FW1 Pinout Reference

This is a working reference for the FW1 board. It separates assignments found in published documentation from assignments recovered through binary analysis or hardware testing.

## Evidence labels

| Label | Meaning |
| --- | --- |
| `documented` | Appears in published board or FPGA documentation. |
| `static analysis` | Recovered from stock firmware, host code, or a binary artifact. |
| `physically observed` | Confirmed through a hardware measurement, USB capture, or functional test. |
| `validated` | Used successfully by replacement firmware or a clean-room implementation on hardware. |
| `unresolved` | Plausible assignment that still needs continuity testing or a focused hardware experiment. |

A row can have more than one label. `static analysis` is not equivalent to a published schematic, and a functional result does not necessarily prove the complete passive net topology.

## Main RP2040 GPIO

| GPIO | Function | Connected device or path | Evidence |
| ---: | --- | --- | --- |
| 0 | UART0 TX | Display RP2040 link | `static analysis` |
| 1 | UART0 RX | Display RP2040 link | `static analysis` |
| 2 | UART0 CTS | Display RP2040 link | `static analysis` |
| 3 | UART0 RTS | Display RP2040 link | `static analysis` |
| 4 | SPI0 MISO | Shared CC1101 radio bus | `static analysis` |
| 5 | SPI0 chip select | Radio 2 | `static analysis` |
| 6 | SPI0 SCK | Shared CC1101 radio bus | `static analysis` |
| 7 | SPI0 MOSI | Shared CC1101 radio bus | `static analysis` |
| 8 | UART1 TX | External header pin 9 | `documented`, `static analysis` |
| 9 | UART1 RX | External header pin 5 | `documented`, `static analysis` |
| 10 | UART1 CTS | External header pin 7 | `documented`, `static analysis` |
| 11 | UART1 RTS | External header pin 11 | `documented`, `static analysis` |
| 12 | SPI1 MISO | External header pin 12; FPGA path | `documented`, `static analysis` |
| 13 | SPI1 chip select | External header pin 1; FPGA configuration CS | `documented`, `static analysis` |
| 14 | SPI1 SCK | External header pin 15; FPGA configuration clock | `documented`, `static analysis` |
| 15 | SPI1 MOSI | External header pin 13; FPGA path | `documented`, `static analysis` |
| 16 | I2C0 SDA | External header pin 10 | `documented`, `static analysis` |
| 17 | I2C0 SCL | External header pin 8 | `documented`, `static analysis` |
| 18 | Radio 1 chip select | CC1101 radio 1 | `static analysis` |
| 19 | Radio 1 GDO2 | CC1101 radio 1 | `static analysis` |
| 20 | Radio 2 GDO0 | CC1101 radio 2 | `static analysis` |
| 21 | Radio 1 GDO0 | CC1101 radio 1 | `static analysis` |
| 22 | Radio 2 GDO2 | CC1101 radio 2 | `static analysis` |
| 23 | FPGA clock | FPGA clock input; stock path is 31.25 MHz | `documented`, `static analysis`, `validated` |
| 24 | FPGA CDONE | FPGA configuration status | `static analysis`, `validated` |
| 25 | General output/status LED | External header pin 17 | `documented`, `static analysis` |
| 26 | General input | External header pin 14 | `documented`, `static analysis` |
| 27 | General output | External header pin 3 | `documented`, `static analysis` |
| 28 | Display RUN/reset, active low | Display RP2040 RUN input | `static analysis`, `physically observed` |
| 29 | FPGA CRESET_B | FPGA configuration reset | `static analysis`, `validated` |

### Main-side buses

| Bus | Pins | Role |
| --- | --- | --- |
| UART0 | TX 0, RX 1, CTS 2, RTS 3 | Main/display link, 8 Mbaud |
| SPI0 | MOSI 7, MISO 4, SCK 6 | Shared radio bus; CS18 for radio 1 and CS5 for radio 2 |
| UART1 | TX 8, RX 9, CTS 10, RTS 11 | External header |
| SPI1 | MOSI 15, MISO 12, SCK 14, CS13 | External header and FPGA configuration path |
| I2C0 | SDA 16, SCL 17 | External header |

The FPGA configuration path additionally uses `CRESET_B` on GPIO29 and `CDONE` on GPIO24. The recovered programmer uses SPI1 at 5 MHz.

## Display RP2040 GPIO

| GPIO | Function | Connected device or path | Evidence |
| ---: | --- | --- | --- |
| 0 | Inter-processor UART link signal | Crossed PCB link; see UART note below | `static analysis` |
| 1 | Inter-processor UART link signal | Crossed PCB link; see UART note below | `static analysis` |
| 2 | Inter-processor UART flow-control signal | Crossed PCB link; see UART note below | `static analysis` |
| 3 | Inter-processor UART flow-control signal | Crossed PCB link; see UART note below | `static analysis` |
| 4 | Serial audio data | Speaker path | `static analysis`, `validated` |
| 5 | Audio bit clock | Speaker path | `static analysis` |
| 6 | Audio word/LR clock | Speaker path | `static analysis` |
| 7 | Addressable RGB LED data | Seven-element LED chain | `static analysis`, `physically observed` |
| 8 | Probable charger enable, active low | Charger control | `unresolved` |
| 9 | Infrared transmit | IR output | `static analysis` |
| 10 | SPI1 SCK | TFT display | `static analysis`, `validated` |
| 11 | SPI1 MOSI | TFT display | `static analysis`, `validated` |
| 12 | Display data/command | TFT display | `static analysis`, `validated` |
| 13 | SPI1 chip select | TFT display | `static analysis`, `validated` |
| 14 | Gray button | Button event 0 | `static analysis` |
| 15 | Yellow button | Button event 1 | `static analysis` |
| 16 | Infrared receive | IR input | `static analysis` |
| 17 | PDM microphone clock | Microphone | `static analysis` |
| 18 | No software use recovered | Passive or board-revision-specific connection unknown | `unresolved` |
| 19 | No software use recovered | Passive or board-revision-specific connection unknown | `unresolved` |
| 20 | No software use recovered | Passive or board-revision-specific connection unknown | `unresolved` |
| 21 | No software use recovered | Passive or board-revision-specific connection unknown | `unresolved` |
| 22 | Green button | Button event 2 | `static analysis` |
| 23 | Blue button, active low | Button event 3; stock display boot path | `static analysis`, `physically observed` |
| 24 | Red button | Button event 4 | `static analysis` |
| 25 | TFT backlight PWM | Display backlight and startup status output | `static analysis`, `validated` |
| 26 | I2C1 SDA | Local sensor/control bus | `static analysis`, `validated` |
| 27 | I2C1 SCL | Local sensor/control bus | `static analysis`, `validated` |
| 28 | No software use recovered | Passive or board-revision-specific connection unknown | `unresolved` |
| 29 | PDM microphone data | Microphone | `static analysis` |

### Inter-processor UART note

The RP2040 UART mux only permits hardware-valid roles on the selected pins. Replacement firmware configures UART0 on both processors as TX GPIO0, RX GPIO1, CTS GPIO2, and RTS GPIO3. The PCB crosses the signals between processors. Some stock-binary analysis records describe the display side from the peer's wire perspective as RX0/TX1/RTS2/CTS3; that notation should not be used as an alternate RP2040 pin-function assignment.

## External 20-pin header

Pin 4 is the I/O voltage reference input and must be driven before relying on buffered I/O. The documented options are to connect pin 2 to pin 4 for a 5 V reference or pin 6 to pin 4 for a 3.3 V reference.

| Pin | Function | Main signal | Front end |
| ---: | --- | --- | --- |
| 1 | SPI chip select output | GPIO13 | SN74LXC1T45 |
| 2 | 5 V output | - | Power |
| 3 | General output | GPIO27 | SN74LXC1T45 |
| 4 | I/O voltage reference, 1.1-5.5 V | - | Required input |
| 5 | UART1 RX input | GPIO9 | SN74LXC1T45 |
| 6 | 3.3 V output | - | Power |
| 7 | UART1 CTS input | GPIO10 | SN74LXC1T45 |
| 8 | I2C0 SCL | GPIO17 | PCA9517 |
| 9 | UART1 TX output | GPIO8 | SN74LXC1T45 |
| 10 | I2C0 SDA | GPIO16 | PCA9517 |
| 11 | UART1 RTS output | GPIO11 | SN74LXC1T45 |
| 12 | SPI1 MISO input | GPIO12 | SN74LXC1T45 |
| 13 | SPI1 MOSI output | GPIO15 | SN74LXC1T45 |
| 14 | General input | GPIO26 | SN74LXC1T45 |
| 15 | SPI1 clock output | GPIO14 | SN74LXC1T45 |
| 16 | SWCLK | SWCLK | Direct |
| 17 | General output/status LED | GPIO25 | SN74LXC1T45 |
| 18 | SWDIO | SWDIO | Direct |
| 19 | Ground | - | Ground |
| 20 | Ground | - | Ground |

## FPGA package pins

These assignments come from the published constraint set and are included separately from the RP2040 board pinout.

| Function | iCE40 pin |
| --- | ---: |
| SPI MISO, RP2040 side / external side | 14 / 25 |
| SPI MOSI, RP2040 side / external side | 17 / 23 |
| SPI clock, RP2040 side / external side | 15 / 27 |
| SPI CS, RP2040 side / external side | 16 / 26 |
| UART TX, RP2040 side / external side | 6 / 28 |
| UART RX, RP2040 side / external side | 9 / 31 |
| UART CTS, RP2040 side / external side | 10 / 32 |
| UART RTS, RP2040 side / external side | 11 / 34 |
| GPIO26, RP2040 / external / direction | 19 / 36 / 35 |
| GPIO27, RP2040 / external / direction | 18 / 41 / 40 |
| FPGA clock | 37 |
| I2C SDA / SCL | 43 / 38 |
| I/O configuration enable | 39 |
| SRAM clock / chip select | 42 / 3 |
| SRAM IO0 / IO1 / IO2 / IO3 | 12 / 21 / 13 / 20 |
| FTDI IO0 / IO1 / IO2 / IO3 | 46 / 47 / 44 / 48 |
| FTDI SCLK / SS / MISO | 45 / 2 / 4 |

## Display-side I2C devices

The display-side bus is I2C1 on GPIO26/GPIO27 at a recovered operating frequency of 400 kHz.

| Address | Device or role | Evidence |
| ---: | --- | --- |
| `0x19` | LIS3DH accelerometer | `static analysis`, `validated` |
| `0x21` | PCA9555/TCA9555-compatible board-interface expander | `static analysis`, `physically observed`; exact suffix unresolved |
| `0x6B` | BQ25892 charger/power-path controller | `static analysis`, `physically observed` |
| `0x6F` | MCP7940 RTC | `static analysis` |

The expander's recovered role includes header direction control on port 0 and radio filter selection on port 1. Port 1 bit 5 and the exact external net labelled `W8` remain unresolved.

## Known follow-up work

- Continuity-test the red button route to the main RP2040 BOOTSEL strap.
- Confirm whether display GPIO8 reaches the charger's active-low enable input.
- Identify the exact I2C expander suffix and resolve port 1 bit 5.
- Check display GPIO18-21 and GPIO28 for passive or board-revision-specific connections.
- Record board revision differences before treating this map as universal.
