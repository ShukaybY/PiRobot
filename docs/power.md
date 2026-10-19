# Power architecture and unresolved connections

## Current build (owner-confirmed)

The owner confirms that the robot currently receives **power from a wall outlet through a power brick and USB cable connected to the Pi**, with **no batteries installed**, and that audio, camera, and servos are working. Battery operation is a future plan.

The outlet adapter model, DC output voltage/current, exact USB connector type, servo supply branch, and ground routing are **Needs confirmation**. Functional operation does not document the exact supply topology or electrical measurements. Python controls signal GPIO only; it cannot establish these physical connections.

## Documented proposal, not verified build instructions

The old README proposes this sequence:

```text
2 × Samsung 30Q cells described as parallel
→ TP4056 Type-C board described as charger + protection
→ SPST switch
→ PPTC described as 2A / 16V
→ TPS61088 module described as 5V / 4A
→ breadboard 5V rail
   → Pi 5V header input
   → servo power with 1000µF capacitor nearby
   → DRV8833 supply
   → PAM8403 supply
```

This records the earlier plan only. It does not validate cell configuration, board protection, charging while operating, current handling, regulation, reverse-current paths, wiring gauge, fuse coordination, thermal behavior, or motor/servo transients. Ratings quoted in the original README are not measurements or proof of suitability.

## Servo conflict

The wiring table connects servo power through Pi physical pin 4 and a breadboard. A later section instead says servos must receive power from a regulated rail rather than the Pi pin. Neither code nor supplied test results resolve this conflict. Servo supply origin, whether that rail also feeds the Pi, and ground routing are **Needs confirmation**. No one option is presented here as a verified connection.

## Remaining wiring details and future battery decisions

For the current outlet-powered build, document the adapter rating, exact USB input connector, servo supply branch, and common grounds. For a future battery build, confirm the exact battery/charger/boost/protection boards and their documentation, servo and motor supply requirements, measured peak loads, fuse placement/rating, switch and conductor ratings. Confirm whether USB and header power can coexist safely in the actual assembly. Establish servo endpoints mechanically before motion tests. The README's assertion that one converter is sufficient and another browns out is a historical report, not validation of this design.

Until those details are established, use this repository as software and project evidence, not as instructions to assemble or charge a battery pack. The preparation performed no electrical or hardware tests.
