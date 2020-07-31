import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class LED():

    def __init__(self, pin):
        self.state = 0
        self.pin = pin

        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, self.state)

    def set(self, onoff):
        self.state = onoff
        GPIO.output(self.pin, self. state)

    def __delete__(self):
        GPIO.cleanup()
