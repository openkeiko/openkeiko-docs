# Base MicroPython

This page describes the first firmware milestone: build an unmodified MicroPython runtime with the FW1 16 MiB flash geometry, flash the same UF2 to both RP2040 controllers, and install the required role-specific boot hooks.

The board definition only establishes the RP2040 target, flash size, filesystem boundary, and safe default buses. It does not initialize the display, radios, FPGA, charger, buttons, or inter-processor protocol.

## Flash layout

Each controller has a 16 MiB QSPI flash device:

| Region | Address range | Size | Purpose |
| --- | --- | ---: | --- |
| Firmware | `0x10000000` - `0x100FFFFF` | 1 MiB | MicroPython firmware reservation |
| Filesystem | `0x10100000` - `0x10FFFFFF` | 15 MiB | MicroPython storage |

The filesystem begins at flash offset `0x00100000`. The first filesystem initialization can erase the existing contents in that region, including stock assets and settings. Treat the existing filesystem contents as unavailable once the new runtime initializes storage.

## Board definition

The minimal board definition lives in:

```text
firmware/micropython/boards/FW1_16MB/
├── fw1_16mb.h
├── mpconfigboard.cmake
└── mpconfigboard.h
```

The important settings are:

```c
#define PICO_FLASH_SIZE_BYTES (16 * 1024 * 1024)
#define MICROPY_HW_FLASH_STORAGE_BYTES (15 * 1024 * 1024)
```

The board header also provides main-side defaults for UART0, I2C0, and SPI1. The display-side application must pass its own recovered pin assignments explicitly; the base firmware does not assume that both processors have the same peripheral wiring.

## Build prerequisites

Install or provide:

- Git
- A working ARM `arm-none-eabi` toolchain with newlib
- `make`, CMake, and a native compiler for `mpy-cross`
- `mpremote` for installing the role-specific boot hooks

Build against the pinned MicroPython release used for the initial port:

```text
Release: v1.28.0
Commit:  e0e9fbb17ed6fd06bb76e266ae554784c9c80804
```

Keep the MicroPython checkout outside this repository. The board definition is passed into the build; no MicroPython source is copied into OpenKeiko.

## Build the UF2

From the root of `openkeiko-docs`, set paths for the MicroPython checkout and build output:

```sh
export MICROPYTHON_DIR="$PWD/../micropython"
export BUILD_DIR="$PWD/.artifacts/micropython/build/FW1_16MB"
export BOARD_DIR="$PWD/firmware/micropython/boards/FW1_16MB"
```

Obtain the pinned checkout and its submodules:

```sh
git clone --branch v1.28.0 --depth 1 --recurse-submodules \
  https://github.com/micropython/micropython.git "$MICROPYTHON_DIR"
git -C "$MICROPYTHON_DIR" checkout e0e9fbb17ed6fd06bb76e266ae554784c9c80804
git -C "$MICROPYTHON_DIR" submodule update --init --recursive
```

If the checkout already exists, verify it before building:

```sh
test "$(git -C "$MICROPYTHON_DIR" rev-parse HEAD)" = \
  e0e9fbb17ed6fd06bb76e266ae554784c9c80804
```

Build the cross-compiler and RP2040 port:

```sh
make -C "$MICROPYTHON_DIR/mpy-cross" -j"$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 4)"
make -C "$MICROPYTHON_DIR/ports/rp2" \
  BOARD_DIR="$BOARD_DIR" \
  BUILD="$BUILD_DIR" \
  -j"$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 4)"
```

The expected artifacts are:

```text
.artifacts/micropython/build/FW1_16MB/firmware.uf2
.artifacts/micropython/build/FW1_16MB/firmware.bin
.artifacts/micropython/build/FW1_16MB/firmware.elf
```

Confirm the image hash and keep it with the build record:

```sh
shasum -a 256 "$BUILD_DIR/firmware.uf2"
```

## Enter flash mode

Start with the controller powered off and disconnected from USB. Keep the button held while plugging in the USB cable:

- **Main controller:** hold the red button, plug in USB, and wait for the main RP2040 to appear as `RPI-RP2` on hub port 1.
- **Display controller:** hold the blue button, plug in USB, and wait for the display RP2040 to appear as `RPI-RP2` on hub port 2.

The red path enters main-controller BOOTSEL directly. The blue path is provided by the stock display application through display GPIO23 and an application call into the RP2040 bootloader. Install the display-specific boot hook described below before relying on blue after replacing the stock display application. If the expected `RPI-RP2` device does not appear, stop and use a separate hardware recovery method instead.

These button paths expose an `RPI-RP2` UF2 mass-storage volume, not the Picoboot interface. Do not use `picotool` here. Release the button after the expected controller appears and confirm the hub port before copying the UF2.

## Flash one controller

Flash only one RP2040 at a time. Do not place both controllers in BOOTSEL together; their `RPI-RP2` volumes are otherwise indistinguishable.

After placing the selected controller in BOOTSEL, confirm that the expected `RPI-RP2` volume is mounted. Copy the UF2 file to the root of that volume. On macOS:

```sh
BOOT_VOLUME=$(find /Volumes -maxdepth 1 -type d -name RPI-RP2 -print -quit)
test -n "$BOOT_VOLUME"
cp "$BUILD_DIR/firmware.uf2" "$BOOT_VOLUME/"
```

The controller will unmount the volume and reboot after accepting the file. Wait for its MicroPython USB serial device to return before flashing the second controller. The base UF2 is intentionally identical for main and display; the controller role is assigned by the files installed on its filesystem, not by a different board flash geometry.

Repeat the BOOTSEL selection, flash, and re-enumeration steps for the other controller.

For automated tooling, select the target by stable USB hub port or fixed serial and flash display first, main second. Never select an RP2040 ROM device by `2e8a:0003` alone because both controllers use that identity in BOOTSEL.

## Install role-specific boot hooks

`boot.py` is a filesystem file, not part of the compiled UF2. Install the main or display boot hook on the matching controller after flashing.

After both freshly flashed controllers appear as MicroPython serial devices, identify their serials:

```sh
uvx mpremote devs
```

## Enable main reset protection

GPIO28 is the display controller's active-low RUN input. The main-specific boot hook holds it high from the start of main boot so main startup, reset, watchdog recovery, and UF2 deployment do not reset or disconnect the display:

```text
firmware/micropython/main/boot.py
```

Install it only on the main controller:

```sh
uvx mpremote connect id:<MAIN_SERIAL> \
  fs cp firmware/micropython/main/boot.py :boot.py
uvx mpremote connect id:<MAIN_SERIAL> reset
```

Do not pulse GPIO28 during ordinary boot, reset, or flashing. Any deliberate display reset should be a separate, guarded operation.

## Enable display blue-button recovery

GPIO23 is the display controller's active-low blue-button input. The display-specific boot hook configures it with an internal pull-up before sampling it:

```text
firmware/micropython/display/boot.py
```

Install it only on the display controller:

```sh
uvx mpremote connect id:<DISPLAY_SERIAL> \
  fs cp firmware/micropython/display/boot.py :boot.py
uvx mpremote connect id:<DISPLAY_SERIAL> reset
```

The hook debounces the held-low input briefly and calls `machine.bootloader()` before application startup. After it is installed, power off the board, hold blue, and plug in USB to enter display flash mode. The main controller should have the main reset-protection hook installed separately.

## Smoke test

With the role-specific boot hooks installed, verify that each controller can:

1. Enumerate as a distinct MicroPython serial device.
2. Accept a REPL connection.
3. Reset and re-enumerate without disconnecting its peer.
4. Create and read a small filesystem file.
5. Enter BOOTSEL again through the selected recovery path.

Example filesystem check:

```sh
uvx mpremote connect id:<TARGET_SERIAL> exec \
  "import os; print(os.listdir('/')); print(open('/boot.py').read())"
```

The expected result at this stage is a working generic MicroPython runtime, not a functioning display, radio, FPGA, or inter-processor link. Those should be brought up as separate, role-specific milestones.
