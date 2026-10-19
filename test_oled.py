from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
import time

serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

def draw_eyes(open_eyes=True):
    with canvas(device) as draw:
        if open_eyes:
            # Left eye
            draw.ellipse([20, 15, 55, 50], outline="white")
            draw.ellipse([32, 27, 43, 38], fill="white")
            # Right eye
            draw.ellipse([73, 15, 108, 50], outline="white")
            draw.ellipse([85, 27, 96, 38], fill="white")
        else:
            # Closed eyes
            draw.line([20, 32, 55, 32], fill="white", width=3)
            draw.line([73, 32, 108, 32], fill="white", width=3)

print("Starting eye animation...")
while True:
    draw_eyes(open_eyes=True)
    time.sleep(3)
    draw_eyes(open_eyes=False)
    time.sleep(0.2)
