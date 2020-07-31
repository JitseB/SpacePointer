import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Stepper():
    """
    Custom driver for the for the (double H-bridge) TB6612.
    """

    STEP_SEQUENCE = [
      [1,0,1,0],
      [0,1,1,0],
      [0,1,0,1],
      [1,0,0,1]
    ]

    def __init__(self, control_pins):
        self._step = 0
        self.current_angle = 0
        self.control_pins = control_pins

        for pin in self.control_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

    def step(self, reverse=False):
        # Move 1.7 deg
        if reverse:
            if self._step <= 0:
                self._step = 3
            else:
                self._step -= 1
        else:
            if self._step >= 3:
                self._step = 0
            else:
                self._step += 1
        for pin in range(4):
            GPIO.output(self.control_pins[pin], Stepper.STEP_SEQUENCE[self._step][pin])
        time.sleep(0.01)

    def relax(self):
        for pin in range(4):
            GPIO.output(self.control_pins[pin], 0)

    def __delete__(self):
        GPIO.cleanup()
