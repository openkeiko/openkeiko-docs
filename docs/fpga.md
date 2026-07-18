# FPGA

FW1 uses a Lattice `ICE40UP5K-SG48I` between the main RP2040, the external digital interfaces, USB, and serial SRAM.

## Connected devices

| Device | Connection |
| --- | --- |
| Main RP2040 | SPI configuration, fabric clock, external I/O paths |
| FT232H | Four-bit FT1248 interface |
| APS6404L-3SQR-ZR | 8 MiB serial SRAM |
| External header | UART, SPI, I2C, and general GPIO paths |

The FPGA is SRAM-configured. A volatile image remains active across a main-RP2040 reset as long as FPGA power and configuration state are retained.

## Main RP2040 interface

| Signal | Main GPIO |
| --- | ---: |
| SPI1 MISO | 12 |
| Configuration/runtime chip select | 13 |
| SPI1 SCK | 14 |
| SPI1 MOSI | 15 |
| Fabric clock | 23 |
| CDONE | 24 |
| CRESET_B | 29 |

The fabric clock is generated from the 125 MHz RP2040 system clock through GPOUT1 on GPIO23. The validated divider is 4, producing 31.25 MHz with a 50 percent duty cycle.

## Volatile configuration

The validated programming interface uses SPI1 at 5 MHz, mode 0, with 8-bit MSB-first transfers.

Accepted bitstreams are 64 to 128 KiB and contain the iCE40 synchronization word `7E AA 99 7E` within the first 256 bytes. The known images are 104,090 bytes.

Configuration uses active-low `CRESET_B` and checks `CDONE` before enabling user I/O. At least 1.2 ms is required for CRAM clear after reset release, and at least 49 additional clocks are required after `CDONE` for user-I/O activation. The validated implementation allows 1.3 ms and 56 wake clocks.

Configuration is volatile only. No NVCM write is required or performed. The factory image can be restored by resetting the FPGA without supplying a new CRAM image.

## FT1248 USB path

The FT232H is connected as an FT1248 slave. The FPGA is bus master.

| Property | Value |
| --- | --- |
| Width | 4-bit half-duplex |
| Bit order | LSB first |
| Clock polarity | Low |
| Clock phase | 1 |
| FPGA-derived clock | 3.90625 MHz in the validated implementation |
| FT232H RX/TX FIFO size | 1 KiB each |

FPGA package connections are:

| Signal | Package pin |
| --- | ---: |
| MIOSIO0 | 46 |
| MIOSIO1 | 47 |
| MIOSIO2 | 44 |
| MIOSIO3 | 48 |
| SCLK | 45 |
| SS, active low | 2 |
| MISO/status | 4 |

USB reads from this path are stream-oriented and can return different chunk sizes. Host software must not assume a fixed read size.

## Serial SRAM

| Signal | FPGA package pin |
| --- | ---: |
| Clock | 42 |
| Chip select | 3 |
| IO0 | 12 |
| IO1 | 21 |
| IO2 | 13 |
| IO3 | 20 |

## Logic-analyzer interface

The stock analyzer interface uses the FT1248 path and a small register protocol:

- Device address: `0x00`
- Control register: `0x80`
- Sample-rate register: `0x81`
- Start: `0x01`
- Stop: `0x02`
- Clear: `0x04`

Published sample rates are:

| Rate | Divider value |
| ---: | ---: |
| 122 kHz | `0x80` |
| 244 kHz | `0x40` |
| 488 kHz | `0x20` |
| 977 kHz | `0x10` |
| 1.95 MHz | `0x08` |
| 3.9 MHz | `0x04` |

Samples use four-channel run-length encoding: the high nibble contains the four logic levels and the low nibble contains run length minus one, for runs of 1 to 16 samples.

The four analyzer channels represent these multiplexed external paths:

1. SPI CS / UART RTS / GPIO27
2. SPI clock / UART CTS / GPIO26
3. SPI MOSI / UART RX / I2C SCL
4. SPI MISO / UART TX / I2C SDA

## Known boundaries

- FPGA configuration is explicit and should not occur as an incidental part of main-controller startup.
- Multi-byte FT1248 bursts are not currently treated as a stable interface.
- The complete factory FPGA design is not available as source.
- General output routing should remain disabled unless the selected image and external voltage domain are known.
