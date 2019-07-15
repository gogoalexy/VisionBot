# USB serial example.
#
# WARNING:
# This script should NOT be run from the IDE or command line, it should be saved as main.py
# Note the following commented script shows how to receive the image from the host side.

import sensor, image, time
from pyb import USB_VCP, LED

usb = USB_VCP()
led = LED(2)
sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
print("ASCII Table ~ Character Map")
thisByte = 33
init = True
usb.setinterrupt(3)
# input
while(init):
    cmd = usb.recv(1, timeout=5000)
    if (cmd == b'\x01'):
        led.toggle()
        # usb.send(0x33, timeout=5000)
        init = False

while(True):
    print(chr(thisByte))
    if (thisByte == 126):
        thisByte = 33
    thisByte += 1

