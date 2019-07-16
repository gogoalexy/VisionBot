# USB serial example.
#
# WARNING:
# This script should NOT be run from the IDE or command line, it should be saved as main.py
# Note the following commented script shows how to receive the image from the host side.

import sensor, image, time, ustruct
from pyb import USB_VCP, LED

usb = USB_VCP()
led = LED(1)
sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.

usb.setinterrupt(3)
# input
while(True):
    cmd = usb.recv(1, timeout=5000)
    if (cmd == b'\x01'):
        led.toggle()
        for item in range(65, 91):
            usb.write(ustruct.pack('<b', item))
    else:
        continue
