import RPi.GPIO as GPIO
import time

LEFT_SERVO = 12
RIGHT_SERVO = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_SERVO, GPIO.OUT)
GPIO.setup(RIGHT_SERVO, GPIO.OUT)

left = GPIO.PWM(LEFT_SERVO, 50)
right = GPIO.PWM(RIGHT_SERVO, 50)

left.start(0)
right.start(0)

def set_angle(servo, angle):
    duty = 2 + (angle / 18)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

def set_arms(angle):
    set_angle(left, angle)
    set_angle(right, 180 - angle)
    print(f"Left: {angle}° Right: {180 - angle}°")

try:
    while True:
        angle = int(input("Enter left arm angle (0-180): "))
        set_arms(angle)
except KeyboardInterrupt:
    left.stop()
    right.stop()
    GPIO.cleanup()
    print("Done.")
