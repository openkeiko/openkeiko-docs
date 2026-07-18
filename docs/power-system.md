# Power System

Power management is owned by the display side of the board. The primary charger and power-path controller is a Texas Instruments BQ25892 on display I2C1.

## Power controller

| Property | Value |
| --- | --- |
| Device | BQ25892 |
| I2C address | `0x6B` |
| Bus | Display I2C1 |
| SDA | Display GPIO26 |
| SCL | Display GPIO27 |
| Bus speed | 400 kHz |

The device manages USB input, battery charging, the battery-to-system path, and ship-mode shutdown.

## Status registers

| Register | Fields used |
| --- | --- |
| `REG0B` | Input source, charge state, power-good status |
| `REG0E` | Battery-voltage ADC |
| `REG11` | VBUS-voltage ADC and VBUS-good status |
| `REG12` | Charge-current ADC |
| `REG14` | Part identity and revision |
| `REG09` | BATFET state and ship-mode control |

The decoded measurements are:

```text
battery_mV = 2304 + 20 * (REG0E & 0x7F)
vbus_mV    = 2600 + 100 * (REG11 & 0x7F)
charge_mA  = 50 * (REG12 & 0x7F)
```

`REG0B[7:5]` identifies the input source, `REG0B[4:3]` identifies the charge state, and `REG0B[2]` reports power-good. `REG11[7]` reports VBUS-good.

Continuous ADC conversion is enabled by setting `REG02[7:6]` while preserving the other charger-control bits.

## Power off and ship mode

A three-second hold of the red button requests power off. Red is active low on display GPIO24.

Power off is implemented by preserving `REG09` and setting bit 5, `BATFET_DIS`:

```text
REG09 = REG09 | 0x20
```

On battery power, this disconnects BAT from SYS and powers down both controllers and the board's system loads. With USB power present, VBUS can continue supplying SYS after the battery path is disabled, so setting `BATFET_DIS` does not guarantee that the board turns off.

The current replacement behavior refuses ship mode while an external input source, power-good, or VBUS-good condition is present.

## Wake behavior

The gray button is active low on display GPIO14 and is also connected to the charger's wake path. Holding gray for approximately two seconds wakes a board that was shut down through ship mode. This path does not require either RP2040 to be running.

## Inactivity behavior

Display inactivity turns down or disables the TFT backlight. It does not place either RP2040 into dormant sleep and does not shut down the rest of the board.

No application-level deep-sleep behavior is currently documented for FW1. Ship mode and backlight inactivity should therefore be treated as separate features.

## Known boundaries

- The complete passive BAT, SYS, and VBUS topology is not documented.
- Low-battery thresholds observed in existing firmware are approximate and are not presented as a calibrated battery specification.
- The exact board-level connection between gray and the charger wake input has not been continuity-mapped.
