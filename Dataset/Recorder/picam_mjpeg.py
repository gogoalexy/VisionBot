import picamera

camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.start_recording('my_video.mjpg', format=mjpeg)
camera.wait_recording(15)
camera.stop_recording()
