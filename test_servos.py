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

print("Testing servos...")

print("Arms down")
set_angle(left, 0)
set_angle(right, 0)
time.sleep(1)

print("Arms neutral")
set_angle(left, 90)
set_angle(right, 90)
time.sleep(1)

print("Arms up")
set_angle(left, 180)
set_angle(right, 180)
time.sleep(1)

print("Arms down")
set_angle(left, 0)
set_angle(right, 0)
time.sleep(1)

left.stop()
right.stop()
GPIO.cleanup()
print("Done.")
