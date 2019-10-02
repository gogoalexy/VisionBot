# Frame Differencing

import sensor, image, pyb, time

BLUE_LED_PIN = 3 # operation indicator

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # grayscale image
sensor.set_framesize(sensor.B64X64) # 80*60 resolution
sensor.skip_frames(time = 2000) # Let new settings take affect.
sensor.set_auto_whitebal(False) # Turn off white balance.
clock = time.clock() # Tracks FPS.

# Take from the main frame buffer's RAM to allocate two extra frame buffer.
buffer1 = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.GRAYSCALE)
buffer2 = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.GRAYSCALE)

sensor.skip_frames(time = 500) # Give the user time to get ready.
buffer1.replace(sensor.snapshot()) # Capture the first frame.

oddframe = True # Tracks if the frame number is odd or not.

pyb.LED(BLUE_LED_PIN).on() # indicator on

for i in range(3000):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.
    if (oddframe):
        oddframe = False
        buffer2.replace(img)
        img.difference(buffer1)
    else:
        oddframe = True
        buffer1.replace(img)
        img.difference(buffer2)

    pyb.delay(4) # Slow down the entire process.

    print(clock.fps()) # Note: Your OpenMV Cam runs about half as fast while
    # connected to your computer. The FPS should increase once disconnected.

pyb.LED(BLUE_LED_PIN).off() # indicator off
