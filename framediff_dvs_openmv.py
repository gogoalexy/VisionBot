# Frame Differencing

import sensor, image, pyb, time, pyb

BLUE_LED_PIN = 3 # operation indicator

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # grayscale image
sensor.set_framesize(sensor.QQQVGA) # 80*60 resolution
sensor.skip_frames(time = 2000) # Let new settings take affect.
sensor.set_auto_whitebal(False) # Turn off white balance.
clock = time.clock() # Tracks FPS.

# Take from the main frame buffer's RAM to allocate two extra frame buffer.
buffer0 = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.GRAYSCALE)
buffer1 = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.GRAYSCALE)
buffer2 = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.GRAYSCALE)
prevFD = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.GRAYSCALE)

sensor.skip_frames(time = 500) # Give the user time to get ready.
buffer0.replace(sensor.snapshot())
buffer1.replace(sensor.snapshot()) # Capture the first frame.

count = 0 # Tracks if the frame number is odd or not.

pyb.LED(BLUE_LED_PIN).on() # indicator on

for i in range(1000):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.
    if (count == 0):
        count += 1
        buffer2.replace(img)
        prevFD.replace(buffer1).difference(buffer0).gamma_corr(contrast=0.5)
        print(img.difference(buffer1).gamma_corr(contrast=0.5, brightness=0.5).sub(prevFD).compressed_for_ide(), end="")
    elif (count == 1):
        count += 1
        buffer0.replace(img)
        prevFD.replace(buffer2).difference(buffer1).gamma_corr(contrast=0.5)
        print(img.difference(buffer2).gamma_corr(contrast=0.5, brightness=0.5).sub(prevFD).compressed_for_ide(), end="")
    elif (count == 2):
        count = 0
        buffer1.replace(img)
        prevFD.replace(buffer0).difference(buffer2).gamma_corr(contrast=0.5)
        print(img.difference(buffer0).gamma_corr(contrast=0.5, brightness=0.5).sub(prevFD).compressed_for_ide(), end="")

    print(clock.fps()) # Note: Your OpenMV Cam runs about half as fast while
    # connected to your computer. The FPS should increase once disconnected.

pyb.LED(BLUE_LED_PIN).off() # indicator off
