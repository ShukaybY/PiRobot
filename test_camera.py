import subprocess
import os

def capture_image(path="capture.jpg"):
    subprocess.run([
        'rpicam-still',
        '-o', path,
        '--timeout', '500',
        '--nopreview',
        '-q', '85'
    ], capture_output=True)
    return os.path.exists(path)

if capture_image():
    print("Image captured successfully")
else:
    print("Capture failed")
