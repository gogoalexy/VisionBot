# CEN

import sensor, image, time, pyb

BLUE_LED_PIN = 3

def drawGrids(img, begin, end, intergrid):
    for row in range(begin, end, intergrid):
        if row == begin:
            continue
        img.draw_line(row, begin, row, end, color=120, thickness=1)
    for col in range(begin, end, intergrid):
        if col == begin:
            continue
        img.draw_line(begin, col, end, col, color=120, thickness=1)
    return img

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.B64X64)
sensor.set_auto_whitebal(False) # Turn off white balance.
sensor.set_auto_gain(False, gain_db=8)
sensor.skip_frames(time = 2000)

clock = time.clock()

buffer1 = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.GRAYSCALE)
buffer2 = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.GRAYSCALE)
sensor.skip_frames(time = 500)
buffer1.replace(sensor.snapshot())

oddframe = True # Tracks if the frame number is odd or not.

pyb.LED(BLUE_LED_PIN).on() # indicator on

for i in range(1000):
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
    drawGrids(img, 0, 63, 8)

    print(clock.fps()) # Note: Your OpenMV Cam runs about half as fast while
    # connected to your computer. The FPS should increase once disconnected.

pyb.LED(BLUE_LED_PIN).off() # indicator off
