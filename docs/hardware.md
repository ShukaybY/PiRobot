# Hardware / parts inventory

Evidence: original project README, supplied Python files, and owner confirmation that audio, camera, and servos work. The owner confirms wall outlet → power brick → USB cable → Pi, with no batteries installed. “Reported installed” refers to the original README; “owner-confirmed working” records the owner’s functional report, not independent bench testing of this sanitized copy. No electrical measurements were supplied. Quantities below are source-listed quantities; singular items are marked “1 listed,” not independently counted. Unspecified exact variants, voltages, and installation details are **Needs confirmation**.

| Part / exact known identity | Quantity | Role | Voltage supported by source | Status |
|---|---|---|---|---|
| Outlet power adapter; exact model Needs confirmation | 1 supply reported; adapter count Needs confirmation | Current wired power | USB connection confirmed; output voltage/current and exact connector Needs confirmation | Outlet-powered operation owner-confirmed |
| Raspberry Pi 3A+ | 1 listed | Controller | Wired outlet power confirmed; USB input confirmed; adapter rating Needs confirmation | Reported installed |
| SanDisk 32GB Class 10 microSD; exact SKU Needs confirmation | 1 listed | OS/storage | Needs confirmation | Reported installed |
| SH1106 1.3-inch 128×64 I2C OLED; board variant Needs confirmation | 1 listed | Eyes; address 0x3C in code | README connects VCC to 3.3V | Reported installed |
| Plantronics Poly Blackwire 3320 USB headset | 1 listed | Development microphone/speaker | USB; exact electrical rating Needs confirmation | Audio owner-confirmed working; model from original README |
| OV5647 5MP fixed-focus 75° CSI camera; module variant Needs confirmation | 1 listed | Vision | CSI; voltage Needs confirmation | Camera owner-confirmed working; model from original README |
| SG90 180° servo; manufacturer/variant Needs confirmation | 5 listed; 2 arm channels in code | Arms; remaining 3 roles Needs confirmation | README says 5V; supply connection conflicts | Arm servos owner-confirmed working; remainder unknown |
| GA12-N20 100RPM DC motor; exact SKU Needs confirmation | 4 | Tank tracks | 6V rating stated | Planned; installed status Needs confirmation |
| DRV8833 dual H-bridge module; board variant Needs confirmation | 1 listed | Track motor drive | README proposes 5V VCC; actual terminals/rating Needs confirmation | Planned; no driver code |
| VL53L0X ToF module; board variant Needs confirmation | 1 listed | Distance; source address 0x29 | README proposes 3.3V | Planned; no sensor code |
| MPU6050 GY-521 | 1 listed | Motion; source address 0x68 | README proposes 3.3V | Planned; no sensor code |
| TTP223 capacitive touch module; variant Needs confirmation | 3 | Touch inputs | Needs confirmation | Planned; no sensor code |
| MS3625 MEMS microphone, described as INMP441-compatible | 1 listed | Final I2S microphone | Needs confirmation | Planned |
| PAM8403 2×3W amplifier module; board variant Needs confirmation | 1 listed | Final speaker amplifier | README proposes 5V | Planned |
| 4Ω 3W mini speaker, JST-PH2.0; exact model Needs confirmation | 1 listed | Final audio output | Needs confirmation; 3W is power, not voltage | Planned |
| Samsung 30Q 18650, source says 3000mAh / 15A | 2 | Proposed parallel battery source | Needs confirmation; not specified in source | Planned; not installed |
| TP4056 Type-C charger, described as “with protection”; exact board Needs confirmation | 1 listed | Proposed charging/protection | Needs confirmation | Planned architecture; installation unknown |
| TPS61088 boost converter module; exact board Needs confirmation | 1 listed | Proposed regulated supply | Source claims 5V / 4A output; not measured | Planned architecture; installation unknown |
| MT3608 boost module; exact board Needs confirmation | Needs confirmation | Earlier converter | Needs confirmation | README reports replaced; not validated here |
| PPTC resettable fuse; exact model Needs confirmation | 1 listed | Proposed supply protection | Source says 2A / 16V; suitability Needs confirmation | Planned architecture; installation unknown |
| SPST toggle switch; model/rating Needs confirmation | 1 listed | Main power switching | Needs confirmation | Planned architecture; installation unknown |
| 1000µF 16V capacitor; type/model Needs confirmation | Needs confirmation | Proposed rail decoupling near servos | 16V rating stated, not operating voltage | Planned architecture; installation unknown |
| Breadboard / power rails; model Needs confirmation | Needs confirmation | Prototype interconnect | Needs confirmation | Mentioned in README; actual connections unknown |
| PVC/cardboard chassis with Lego tank tracks | Needs confirmation | Mechanical body/drive | Not applicable | Planned |

No supplier links, costs, inferred extra components, current-capacity validation, or battery build approval are asserted. The motor count (four) versus one dual-channel driver's grouping/load, and the two spare-arm-channel versus five-servo inventory, need confirmation before implementing movement.
