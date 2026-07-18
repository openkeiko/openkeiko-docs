# Component Datasheets

These manufacturer references describe confirmed or strongly identified FW1 components. A component datasheet defines the part itself; it does not prove how every pin is connected on the board.

| Component | Role | Reference |
| --- | --- | --- |
| RP2040 | Main and display controllers | [RP2040 datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf) |
| iCE40UP5K | FPGA | [iCE40 UltraPlus family datasheet](https://www.latticesemi.com/-/media/LatticeSemi/Documents/DataSheets/iCE/iCE40-UltraPlus-Family-Data-Sheet.ashx?document_id=51968) |
| CC1101 | Sub-GHz radios | [CC1101 datasheet](https://www.ti.com/lit/ds/symlink/cc1101.pdf) |
| BQ25892 | Charger and power path | [BQ25892 datasheet](https://www.ti.com/lit/ds/symlink/bq25892.pdf) |
| LIS3DH | Accelerometer | [LIS3DH datasheet](https://www.st.com/resource/en/datasheet/lis3dh.pdf) |
| MCP7940N | Real-time clock | [MCP7940N datasheet](https://ww1.microchip.com/downloads/aemDocuments/documents/MPD/ProductDocuments/DataSheets/MCP7940N-Battery-Backed-I2C-RTCC-with-SRAM-20005010J.pdf) |
| USB2513 | Three-port USB hub | [USB2513 datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/00001598B.pdf) |
| PCA9555-compatible device | Board-interface expander | [PCA9555 datasheet](https://www.nxp.com/docs/en/data-sheet/PCA9555.pdf) |
| FT232H | FPGA USB interface | [FT232H datasheet](https://ftdichip.com/wp-content/uploads/2024/03/DS_FT232H.pdf) |
| APS6404L-3SQR | 8 MiB serial SRAM | [APS6404L-3SQR datasheet](https://www.apmemory.com/wp-content/uploads/APS6404L-3SQR-v2.8-PKG.pdf) |
| SN74LXC1T45 | Header level translators | [SN74LXC1T45 datasheet](https://www.ti.com/lit/ds/symlink/sn74lxc1t45.pdf) |
| PCA9517 | I2C level translator | [PCA9517 datasheet](https://www.nxp.com/docs/en/data-sheet/PCA9517.pdf) |

The TFT is ST7789-compatible, but the exact controller variant has not been physically confirmed. The expander follows the PCA9555 register model, but its exact manufacturer and suffix also remain unresolved.
