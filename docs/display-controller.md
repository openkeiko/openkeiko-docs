# Display Controller

FW1 uses an ST7789-compatible TFT connected to the display RP2040. The panel is configured as a 320 x 240 landscape display using the controller's 240 x 320 geometry with rotation 1.

## Interface

| Signal | Display RP2040 | Configuration |
| --- | ---: | --- |
| SPI clock | GPIO10 | SPI1 SCK |
| Pixel data | GPIO11 | SPI1 MOSI |
| Data/command | GPIO12 | Output |
| Chip select | GPIO13 | Active low |
| Backlight | GPIO25 | Active-high PWM |

The display interface uses SPI mode 0, 8-bit transfers, and MSB-first ordering. The validated MicroPython configuration runs SPI1 at 24 MHz. The stock display firmware uses a 62.5 MHz SPI clock.

The panel connection does not use MISO or a software-controlled reset pin.

## Pixel format and orientation

- Logical resolution: 320 x 240
- Color format: RGB565
- Panel geometry: 240 x 320
- Rotation: 1
- Backlight PWM frequency: 1 kHz

Backlight brightness maps linearly to PWM duty. A duty of zero turns the backlight off; higher duty increases brightness.

## GPIO8

The display firmware holds GPIO8 low before initializing the TFT. Its exact electrical role has not been confirmed, so it should be treated as a required low-level board control rather than named as a panel enable or reset signal.

## Known boundaries

- GPIO8's destination and active function remain unresolved.
- No separate panel reset connection has been identified.
- The validated MicroPython clock is lower than the stock clock but supports correct full-color output.
