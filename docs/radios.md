# Sub-GHz Radios

FW1 has two TI CC1101 radios connected to the main RP2040. They share one SPI bus and use separate chip-select and signal lines.

## Main-side wiring

Shared SPI0 configuration:

| Signal | Main GPIO |
| --- | ---: |
| MISO | 4 |
| SCK | 6 |
| MOSI | 7 |

The validated control bus runs at 1 MHz in SPI mode 0 with MSB-first transfers.

Radio-specific connections:

| Radio | Chip select | GDO0 | GDO2 | SMA connector |
| --- | ---: | ---: | ---: | --- |
| Radio 1 | GPIO18 | GPIO21 | GPIO19 | J2 |
| Radio 2 | GPIO5 | GPIO20 | GPIO22 | J1 |

Both devices report CC1101 `PARTNUM=0x00` and `VERSION=0x14`.

Each radio is connected to its own SMA path. No radio-to-connector switching behavior has been identified.

## Supported bands

The board uses three inclusive RF routing bands:

| Band code | Frequency range |
| ---: | --- |
| 1 | 300-348 MHz |
| 2 | 387-464 MHz |
| 3 | 779-928 MHz |

Frequencies outside these ranges are rejected by the current control layer.

## RF path selection

Band selection is controlled by the PCA9555-compatible expander at display-side I2C address `0x21`, not by the FPGA.

| Expander bit | Function |
| --- | --- |
| P1.1 | Radio 1 band code bit 0 |
| P1.2 | Radio 2 band code bit 0 |
| P1.3 | Radio 1 band code bit 1 |
| P1.4 | Radio 2 band code bit 1 |

The combined RF mask is `0x1E`. The relevant expander registers are output latch `0x03` and configuration `0x07`. A cleared configuration bit enables the corresponding expander output.

Unrelated expander bits must be preserved when selecting a band. The output latch is set before output direction is enabled to avoid an intermediate routing state.

## Validated behavior

- Radio 1 maps to SMA J2.
- Radio 2 maps to SMA J1.
- Selecting the correct 433 MHz path improved receive level by approximately 19-23 dB compared with leaving the RF controls high impedance.
- Radio 2/J1 received and decoded a known 915 MHz signal.
- Radio 1/J2 showed a 43 dB receive-level advantage over radio 2 when the known 915 MHz source was connected only to J2.

## Current software boundary

The validated replacement radio driver is receive-only:

- Transmit strobes are not issued.
- The TX FIFO is not exposed.
- PATABLE is held at eight zero bytes.

This is a software safety boundary, not a statement that the CC1101 hardware is physically incapable of transmission.

## Known boundaries

- The exact filter, switch, and matching topology behind the four expander controls is not documented.
- Expander P1.5, labelled `W8` in recovered interfaces, remains unresolved.
- Absolute sensitivity, output matching, and transmit behavior have not been characterized.
