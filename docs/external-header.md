# External 20-Pin Header

The main RP2040 reaches the external header through the FPGA and board-level translators. Buffered I/O requires an external logic-voltage reference on pin 4.

## Pinout

| Pin | Function | Main signal | Front end |
| ---: | --- | --- | --- |
| 1 | SPI chip-select output | GPIO13 | SN74LXC1T45 |
| 2 | 5 V output | Power | Direct |
| 3 | General output | GPIO27 | SN74LXC1T45 |
| 4 | I/O voltage reference | Required input | 1.1-5.5 V |
| 5 | UART1 RX input | GPIO9 | SN74LXC1T45 |
| 6 | 3.3 V output | Power | Direct |
| 7 | UART1 CTS input | GPIO10 | SN74LXC1T45 |
| 8 | I2C0 SCL | GPIO17 | PCA9517 |
| 9 | UART1 TX output | GPIO8 | SN74LXC1T45 |
| 10 | I2C0 SDA | GPIO16 | PCA9517 |
| 11 | UART1 RTS output | GPIO11 | SN74LXC1T45 |
| 12 | SPI1 MISO input | GPIO12 | SN74LXC1T45 |
| 13 | SPI1 MOSI output | GPIO15 | SN74LXC1T45 |
| 14 | General input | GPIO26 | SN74LXC1T45 |
| 15 | SPI1 clock output | GPIO14 | SN74LXC1T45 |
| 16 | Main SWCLK | SWCLK | Direct |
| 17 | General output/status LED | GPIO25 | SN74LXC1T45 |
| 18 | Main SWDIO | SWDIO | Direct |
| 19 | Ground | - | Ground |
| 20 | Ground | - | Ground |

## I/O voltage reference

Pin 4, `V PINS IN`, must be powered before using buffered UART, SPI, or general GPIO signals.

- Jumper pin 6 to pin 4 for 3.3 V logic.
- Jumper pin 2 to pin 4 for 5 V logic.
- Documented acceptable reference range: 1.1-5.5 V.

Do not assume that the presence of USB or battery power automatically supplies pin 4.

## Translators

UART, SPI, and general GPIO signals use SN74LXC1T45 translators. External I2C uses a PCA9517 translator.

Published per-channel figures for the SN74LXC1T45 paths are:

- 24 mA recommended drive at 3.3 V
- 32 mA recommended drive at 5 V
- 50 mA absolute maximum

These are component figures, not validated aggregate connector, thermal, or board-current limits.

## Direction control

A PCA9555-compatible expander at display I2C address `0x21` controls the buffered UART and SPI directions.

| Expander bit | Header signal | Header pin |
| --- | --- | ---: |
| P0.1 | UART RTS | 11 |
| P0.2 | UART RX | 5 |
| P0.3 | UART TX | 9 |
| P0.4 | SPI MOSI | 13 |
| P0.5 | SPI MISO | 12 |
| P0.6 | SPI CS | 1 |
| P0.7 | SPI SCK | 15 |
| P1.0 | UART CTS | 7 |

At the expander-register level, configuration bit 0 selects output and bit 1 selects input/high impedance. Output latches should be set before changing a path to output.

The validated outward-default mask enables UART RTS, UART TX, SPI MOSI, SPI CS, and SPI SCK. UART RX, UART CTS, and SPI MISO remain inputs.

## Shared FPGA paths

Main SPI1 is also used for volatile FPGA configuration. Header pins 1, 12, 13, and 15 should not be treated as ordinary external SPI while the FPGA is being configured.

GPIO26/header pin 14 and GPIO27/header pin 3 pass through dedicated FPGA paths. Their FPGA package pins and direction controls are listed in the [pinout reference](pinout.md).

## Debug pins

Pins 16 and 18 expose the main RP2040 SWCLK and SWDIO signals directly. They are not level-translated through the header voltage domain.

## Known boundaries

- The exact software-controlled PCA9517 pull-up routing remains unresolved.
- Board-wide current and thermal limits are not established by the translator component ratings.
- Direction and passive wiring may differ across board revisions.
