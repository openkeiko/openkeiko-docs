# USB

One external USB connection feeds a Microchip/SMSC USB2513 three-port USB 2.0 hub. The host sees both RP2040 controllers and the FPGA USB interface at the same time; there is no main/display USB multiplexer.

## Topology

| Hub port | Device | Normal VID:PID | Role |
| ---: | --- | --- | --- |
| 1 | Main RP2040 | `093C:2054` | Main CDC and reset interface |
| 2 | Display RP2040 | `093C:2055` | Display CDC and reset interface |
| 3 | FT232H | `0403:6014` | FPGA FT1248 interface |

The hub identifies as `0424:2513`. Older RP2040 application firmware may identify as `2E8A:000A`.

The `093C` identities belong to the existing product. Replacement firmware should use a separately authorized USB identity before distribution.

## RP2040 application interfaces

Each RP2040 independently exposes a composite USB device:

| Interface | Class | Endpoints |
| ---: | --- | --- |
| 0 | CDC communications `02/02/00` | Interrupt IN `0x81` |
| 1 | CDC data `0A/00/00` | Bulk OUT `0x02`, bulk IN `0x82` |
| 2 | Vendor reset `FF/00/01` | No endpoints |

The bulk endpoints use 64-byte maximum packets. The device class is IAD composite `EF/02/01`, and the declared maximum current is 250 mA.

CDC traffic belongs directly to the selected RP2040. It does not pass through the FT232H or the inter-processor UART.

## RP2040 ROM bootloader

Both controllers use the same ROM identity:

| Property | Value |
| --- | --- |
| VID:PID | `2E8A:0003` |
| Product | `RP2 Boot` |
| UF2 volume | `RPI-RP2` |
| Mass-storage endpoints | Bulk IN `0x81`, bulk OUT `0x02` |

When enabled, Picoboot is a separate vendor interface using bulk OUT `0x03` and bulk IN `0x84`.

The button-triggered stock display path disables Picoboot and exposes only the `RPI-RP2` mass-storage interface. UF2 copying works in this mode, but `picotool` cannot attach and `CURRENT.UF2` is absent.

The two ROM devices are descriptor-identical. Select them by hub port or physical USB location:

- Port 1: main RP2040
- Port 2: display RP2040

Do not select a flash target using `2E8A:0003` alone.

## Reset and BOOTSEL paths

- Opening and closing a selected application CDC device at 1200 baud requests BOOTSEL on that same RP2040.
- Holding red while connecting USB enters main BOOTSEL on hub port 1.
- Holding blue while connecting USB enters display BOOTSEL on hub port 2 while the display boot hook is present.
- The FT232H on port 3 is not an RP2040 serial or flashing path.

The normal two-controller update order is display first, then main. Only one indistinguishable `RPI-RP2` target should be handled at a time.

## Reset isolation

Main GPIO28 is the display RP2040's active-low RUN input. The main boot hook holds it high so a main startup, watchdog reset, software reset, BOOTSEL return, or UF2 update does not disconnect the display USB device.

Each RP2040 can run an independent watchdog. A local watchdog reset should remove and restore only that controller's USB child. Loss of the peer USB device is not expected behavior.

## Host behavior

USB device paths can change after reset. Host tools should rediscover an application device by its stable serial and hub location rather than retaining a platform-specific device path.

Reads from the FT232H/FPGA path are stream-oriented and may return partial chunks. Consumers must not assume fixed-size USB reads.

## Known boundaries

- Exact USB2513 strap or EEPROM configuration is not documented.
- Hub power switching and over-current wiring are unresolved.
- Button and reset routing may vary between board revisions.
