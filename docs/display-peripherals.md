# Display-Side Peripherals

The display RP2040 owns the buttons, RGB LEDs, audio interfaces, infrared interfaces, and local I2C devices.

## Buttons

All five buttons are active low and use pull-ups.

| Button | Display GPIO | Additional role |
| --- | ---: | --- |
| Gray | 14 | Charger wake path |
| Yellow | 15 | - |
| Green | 22 | - |
| Blue | 23 | Display BOOTSEL request during early startup |
| Red | 24 | Three-second ship-mode request |

A 35 ms debounce interval is used by the validated MicroPython controller.

## RGB LEDs

Seven WS2812-compatible RGB LEDs are connected as a serial chain on display GPIO7.

| Property | Value |
| --- | --- |
| LED count | 7 |
| Data GPIO | 7 |
| Wire order | GRB |
| Pixel width | 24 bits |
| PIO clock | 8 MHz |
| Latch delay | 100 microseconds |

The board includes an inverting stage between GPIO7 and the LED chain. The RP2040-side idle level is therefore high. An all-zero frame turns the chain off; the validated implementation sends the zero frame twice when disabling it.

## Local I2C bus

Display I2C1 uses GPIO26 for SDA and GPIO27 for SCL at 400 kHz.

| Address | Device |
| ---: | --- |
| `0x19` | LIS3DH accelerometer |
| `0x21` | PCA9555-compatible board-interface expander |
| `0x6B` | BQ25892 charger and power-path controller |
| `0x6F` | MCP7940 RTC |

### Accelerometer

The LIS3DH is configured for:

- 100 Hz sampling
- X, Y, and Z enabled
- High-resolution mode
- +/-2 g range
- Block-data update

Samples are read as three little-endian signed 16-bit values and shifted right by four. In this mode, each shifted LSB represents 1 mg.

### Real-time clock

The MCP7940 stores time in packed BCD. Seconds bit 7 controls and reports oscillator operation. Both 12-hour and 24-hour values can be decoded.

## Speaker interface

| Signal | Display GPIO |
| --- | ---: |
| Serial audio data | 4 |
| Bit clock | 5 |
| Word/LR clock | 6 |

The validated digital interface uses 8 kHz, 16-bit stereo frames with the same sample in both channels. Existing audio assets use 8 kHz, signed 16-bit PCM WAV, with mono preferred.

The digital clock and data path has been validated with silent output. The amplifier enable, analog routing, and speaker transducer have not yet been validated with a nonzero waveform.

## PDM microphone

| Signal | Display GPIO |
| --- | ---: |
| PDM clock | 17 |
| PDM data | 29 |

The validated PDM clock is 2.048 MHz. The capture path decimates 256 PDM bits into each 8 kHz PCM sample and produces signed 16-bit output. Validated saved captures use 8 kHz mono PCM WAV.

The microphone operates independently of the PCA9555 direction outputs.

## Infrared receiver

The demodulated IR receiver is connected to display GPIO16. It idles high and produces low pulses for received carrier marks.

The validated decoder supports:

- NEC
- NEC extended address/command fields
- NEC repeat frames
- Raw edge-duration capture

A frame completes after 30 ms of high idle. Raw captures are limited to 512 durations.

## Infrared transmitter

The IR transmitter is connected to display GPIO9 and idles low.

| Property | Value |
| --- | --- |
| Supported carrier range | 20-60 kHz |
| NEC carrier | 38 kHz |
| Nominal carrier duty | 34.4 percent |
| Maximum raw timings | 512 |
| Maximum requested raw duration | 2 seconds |

NEC, extended NEC, and raw replay have been validated through onboard optical loopback and external targets. Requested raw duty-cycle values are range-checked, but the hardware waveform remains at the fixed 34.4 percent duty.
