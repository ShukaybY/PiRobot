# Wiring evidence

This is a source reconciliation, **not a verified assembly guide**. Code proves GPIO assignments, not physical continuity, voltage compatibility, or successful operation. Physical pin mappings below refer to the Pi 3A+ 40-pin header. Confirm the board and orientation before wiring. Audio, camera, and servo operation is owner-confirmed on the current outlet-powered build. No batteries are installed. Exact physical power/ground connections still require documentation.

Current power path, owner-confirmed: wall outlet → USB power brick → USB cable → Pi. Adapter rating and exact connector type need confirmation; this does not establish the servo supply branch.

## Components targeted by the application

| Component connection | BCM GPIO | Physical Pi pin | Power / ground evidence | Status |
|---|---|---|---|---|
| OLED SDA | 2 | 3 | I2C bus 1, address 0x3C in code | README connection; physical verification Needs confirmation |
| OLED SCK/SCL | 3 | 5 | I2C clock | README connection; physical verification Needs confirmation |
| OLED VCC | — | 1 | README: 3.3V | Module voltage compatibility Needs confirmation |
| OLED GND | — | 9 | Pi ground per README | Continuity Needs confirmation |
| Left arm signal | 12 | 32 | Code uses 50Hz software PWM | Assignment implemented; connection Needs confirmation |
| Right arm signal | 13 | 33 | Code uses 50Hz software PWM | Assignment implemented; connection Needs confirmation |
| Both servo red power leads | — | **Unresolved** | README table says Pi pin 4 (5V) via breadboard; later text says separate regulated rail | Conflicting; Needs confirmation, do not use as build instruction |
| Both servo brown grounds | — | 34 in README | Breadboard ground described | Common-ground continuity Needs confirmation |
| Plantronics headset | — | USB connector, not header | USB-powered; actual audio indexes configurable in source | Reported development setup; verify on Pi |
| OV5647 camera | — | CSI connector, not header | Camera ribbon; exact module/ribbon orientation Needs confirmation | Reported development setup |

GPIO12/13 can provide hardware PWM through other interfaces, but **this code uses `RPi.GPIO.PWM`, which is software PWM**. A PWM overlay does not convert these calls into hardware PWM. No overlay is required by this repository's implementation.

## Planned connections in the old README (not implemented or verified)

| Component connection | BCM GPIO | Physical Pi pin | Proposed supply / ground | Status |
|---|---|---|---|---|
| DRV8833 AIN1 / AIN2 | 17 / 27 | 11 / 13 | Control signals only | Planned; Needs confirmation |
| DRV8833 BIN1 / BIN2 | 22 / 23 | 15 / 16 | Control signals only | Planned; Needs confirmation |
| DRV8833 “VCC” / GND | — | 2 / 6 in old README | Proposed 5V / Pi ground; actual module power terminal identity unresolved | Needs confirmation; not a verified power connection |
| MPU6050 SDA / SCL | 2 / 3 | 3 / 5 | Shared I2C bus | Planned; Needs confirmation |
| MPU6050 VCC / GND | — | 17 / 14 | Proposed 3.3V / Pi ground | Planned; module compatibility Needs confirmation |
| VL53L0X SDA / SCL | 2 / 3 | 3 / 5 | Shared I2C bus | Planned; Needs confirmation |
| VL53L0X VCC / GND | — | 17 / 20 | Proposed 3.3V / Pi ground | Planned; module compatibility Needs confirmation |
| TTP223 head signal | 4 | 7 | Supply/ground not documented | Planned; Needs confirmation |
| TTP223 body signal | 5 | 29 | Supply/ground not documented | Planned; Needs confirmation |
| TTP223 wake signal | 6 | 31 | Supply/ground not documented | Planned; Needs confirmation |
| MS3625 I2S signals | Needs confirmation | Needs confirmation | Supply/ground Needs confirmation | Planned; no wiring supplied |
| PAM8403 input/output and speaker | Needs confirmation | Needs confirmation | Proposed 5V rail; actual audio input and grounds Needs confirmation | Planned |
| N20 motor outputs / grouping | Not GPIO-powered | Needs confirmation | Motor driver outputs, grouping/supply Needs confirmation | Planned |

The old architecture implies a shared return between Pi, actuator supply and driver. Which grounds are actually connected, their routing, and supply isolation/backfeed behavior **Need confirmation**. Do not assume common ground merely because it appears in this table. No actuators should be powered from signal GPIO. See [power](power.md) before interpreting the proposed 5V connections.
