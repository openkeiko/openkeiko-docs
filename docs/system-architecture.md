# FW1 System Architecture

FW1 is a small distributed system. The main and display RP2040s have separate responsibilities and communicate over a dedicated UART link. USB connects to both processors independently; it is not a proxy for the inter-processor link.

## Topology

```text
                           External USB
                                |
                         USB2513 three-port hub
                         /          |           \
                        /           |            \
              Main RP2040   Display RP2040     FT232H
                  |               |              |
       SPI0 -----+               |              FT1248
       CC1101 x2 |               |              |
       SPI1 -----+----- iCE40 FPGA ------------+
       I2C0/header              |
       20-pin header            external I/O

              Main RP2040 <==== UART0, 8 Mbaud ====> Display RP2040
```

The diagram shows functional ownership, not every passive buffer, level shifter, or power connection.

## Processor ownership

| Area | Main RP2040 | Display RP2040 |
| --- | --- | --- |
| Inter-processor link | UART0, 8 Mbaud, hardware flow control | UART0, 8 Mbaud, hardware flow control |
| USB application device | Independent CDC/reset composite | Independent CDC/reset composite |
| External header | UART1, SPI1, I2C0, GPIO26/27 | Not assigned |
| Radios | Two CC1101 devices on SPI0 | No persistent radio bus recovered |
| FPGA | Configure and clock the FPGA; own the external I/O path | Not assigned |
| Display | Not assigned | ST7789-family TFT on SPI1 |
| Audio | Not assigned | PIO speaker output and PDM microphone |
| Controls | Not assigned | Buttons, RGB LEDs, IR, local sensors |
| Power and time | Receives status through the link | Charger, RTC, and power UI on I2C1 |

## Main/display link

The physical link uses UART0 at 8,000,000 baud, 8 data bits, no parity, one stop bit, and hardware RTS/CTS flow control.

For replacement firmware, both RP2040 UART peripherals use hardware-valid roles:

| Role | GPIO |
| --- | ---: |
| TX | 0 |
| RX | 1 |
| CTS | 2 |
| RTS | 3 |

The board crosses the signal paths between processors. The stock-binary view of the display side can therefore appear reversed when described from the peer's wire perspective. The [pinout reference](pinout.md) records this distinction explicitly.

The replacement framing currently documented in the source workspace uses `0x7E` frame delimiters, `0x7D` byte escaping, a versioned header, a maximum 512-byte payload, and CRC-16/CCITT-FALSE. That is a replacement protocol, not a recovered specification of the stock internal protocol. It should remain labelled as such in future documentation.

## Main-side I/O

The main RP2040 uses SPI0 for two CC1101 radios. The radios share MOSI, MISO, and clock and have separate chip-select and GDO lines. The current replacement control path treats them as receive-only; this is a software safety decision and should not be read as proof that the original hardware cannot transmit.

SPI1 is shared by the external I/O path and FPGA configuration. The main processor configures the FPGA using:

- SPI1 at 5 MHz
- GPIO13 as configuration chip select
- GPIO29 as active-low `CRESET_B`
- GPIO24 as `CDONE`
- GPIO23 as the FPGA clock output, normally 31.25 MHz in the recovered path

The FPGA is SRAM-configured. Initial bring-up can preserve the factory pass-through image before attempting a replacement bitstream.

## Display-side I/O

The display RP2040 owns the user-facing peripherals:

- TFT: SPI1, GPIO10/11/12/13, with backlight PWM on GPIO25
- Speaker: PIO serial audio on GPIO4/5/6 at 8 kHz
- RGB LEDs: GPIO7, seven-element chain
- Infrared: transmit GPIO9, receive GPIO16
- Microphone: PDM data GPIO29 and clock GPIO17
- Buttons: GPIO14, GPIO15, GPIO22, GPIO23, and GPIO24
- Local I2C: SDA GPIO26, SCL GPIO27

The local I2C devices are the accelerometer, board-interface expander, charger/power-path controller, and RTC. Exact passive wiring around the expander and charger still needs additional hardware work.

## USB architecture

The host sees one hub and three downstream functions in normal operation:

| Hub port | Device | Normal VID:PID | Role |
| ---: | --- | --- | --- |
| 1 | Main RP2040 | `093c:2054` | Main CDC/reset interface |
| 2 | Display RP2040 | `093c:2055` | Display CDC/reset interface |
| 3 | FT232H | `0403:6014` | FPGA FT1248 interface |

Both RP2040s independently expose a composite CDC/reset device. CDC traffic does not pass through the FT232H or the main/display UART.

When either RP2040 enters its ROM bootloader, its application device changes to `2e8a:0003`. The two ROM devices must be selected by hub port or physical USB location because VID/PID alone is not enough to identify the processor.

## Reset boundaries

The reset boundaries are intentionally asymmetric:

- A local RP2040 watchdog resets only the processor that owns it.
- GPIO28 on the main RP2040 controls the display RP2040's active-low RUN input.
- Stock main initialization pulsed GPIO28; replacement firmware now holds it released to avoid disconnecting display USB during main reset or flashing.
- A display reset or flash should not be treated as permission to reset the main RP2040.

This separation is important for both recovery tooling and future software architecture.
