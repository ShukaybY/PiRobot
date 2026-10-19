from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.image_composition import ImageComposition
import expressions
import time

serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

def show(img):
    device.display(img.convert(device.mode))

print("Testing expressions...")

show(expressions.neutral())
time.sleep(1)

show(expressions.happy())
time.sleep(1)

show(expressions.sad())
time.sleep(1)

show(expressions.angry())
time.sleep(1)

show(expressions.surprised())
time.sleep(1)

show(expressions.sleepy())
time.sleep(1)

show(expressions.curious_look("left"))
time.sleep(1)

show(expressions.curious_look("right"))
time.sleep(1)

show(expressions.wink("left"))
time.sleep(1)

show(expressions.neutral())
print("Done.")
