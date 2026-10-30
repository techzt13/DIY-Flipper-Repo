# DIY Flipper Zero (STM32WB55 "FCFZ-style" clone)

My **Hack Club Fallen** project: a hand-built Flipper Zero clone based on the
**WeAct STM32WB55CGU6** board, running the official Flipper / Momentum firmware
(via the open-source FCFZ / Nucleus Dark / Flipper-Diy community port).
Remote participant — Hong Kong 🇭🇰

## What it does
- **Sub-GHz (433 MHz, CC1101)** — read/save/replay remotes (HK band, not 315)
- **NFC (ST25R3916)** — the real Flipper NFC chip, full read/emulate
- **Infrared** — receive + transmit remotes (TV-b-gone style)
- **iButton / 1-Wire**, **BadUSB (USB-C)**, **GPIO/UART** breakout
- **SD card** for saved captures, ST7565 monochrome LCD, 6-button nav
- 18650 battery → TP4056 charge → MT3608 boost → 5 V rail

Known clone limitations (firmware/secure-enclave, not fixable in hardware):
U2F and KeeLoq need factory keys; 125 kHz RFID is not supported by the
FCFZ firmware build; no speaker/vibration.

## Repo contents
| Path | What |
|---|---|
| `bom.csv` | Fallen funding BOM (links, min quantities, justifications) |
| `kicad/diy-flipper.kicad_pro/.kicad_sch/.kicad_pcb/.kicad_prl` | Full KiCad 8 project — carrier PCB the WeAct board + modules plug into |
| `kicad/gerbers/` | Gerber + drill files for fab (HASL, cheapest option) |
| `case/bottom_shell.stl`, `case/lid.stl` | 3D-printable 2-part case (ready to slice) |
| `case/case_step.py` | CadQuery source → exports STEP (run in Google Colab) |
| `case/*.step` | STEP exports of the case |

## Build
1. **PCB**: send `kicad/gerbers/` to the cheapest fab (HASL, 1.6 mm, any colour).
2. **Modules**: plug in per the schematic — WeAct board (J1/J2 headers),
   ST7565 LCD (J3), CC1101 433 MHz (J4), micro-SD module (J5),
   ST25R3916 NFC (J6), IR RX (J7), iButton (J8), UART debug (J9), 5 V in (J10).
3. **Buttons**: 6× tactile through SN74HC165 shift register (U1) with 10 kΩ
   pull-downs; inputs H=LEFT G=UP F=OK E=RIGHT D=DOWN C=BACK, SH/LD=PH3.
4. **IR TX**: PB9 → 1 kΩ → 2N3904 base; collector → IR LED → 47 Ω → 3V3.
5. **Power**: 18650 → TP4056 → MT3608 (set to 5.0 V!) → slide switch → 5 V pin.
   The MT3608 is required — the onboard regulator sags on a low battery.
6. **Firmware**: STM32CubeProgrammer (hold BOOT0) → write OTP at 0x1FFF7000 →
   qFlipper "Install from file" → flash the FCFZ-modified Momentum `.dfu`
   (Zadig for the USB driver on Windows). Verify the pinout in the exact `.dfu`
   you flash matches the schematic before powering anything on!

## Pin map (matches prebuilt FCFZ/Momentum .dfu)
SPI bus: SCK=PB3, MISO=PB4, MOSI=PB5 · LCD: CS=PB2, DC=PB1, RST=PB0 ·
SD: CS=PA4 · CC1101: CSN=PA7, GDO0=PA1 · NFC: CS=PE4, IRQ=PA2 ·
IR RX=PA0, TX=PB9 · iButton=PB8 · UART: TX=PB6, RX=PB7

## Build log
- [x] Research + verified parts list (Amazon HK, ST official NFC board)
- [x] Wiring schematic + pinout cross-checked vs community sources & videos
- [x] KiCad schematic + PCB (carrier board, 130×105 mm)
- [x] Case CAD (STL + STEP)
- [ ] Order parts on the HCB grant card
- [ ] Assemble + flash firmware
- [ ] Demo video → Build Submission 🍂

## Credits
Firmware port & reference pinout: FCFZ / Nucleus Dark / Flipper-Diy community,
Momentum firmware, flipperdevices.
