import time, pigpio

class Servo():

    def __init__(self, pin):
        self.pin = pin
        self.degree = 0

        # RPi.GPIO isn't sufficient here
        # Timing of dutycycle is off...
        # (which ends up in servo-jitter).
        self.pwm = pigpio.pi()
        self.pwm.set_mode(self.pin, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency(self.pin, 50) # 50 Hz duty cycle
        self.pwm.set_PWM_dutycycle(self.pin, 0)

    def angle(self, degree):
        if self.degree == degree:
            return

        self.degree = degree
        width = degree / 180 * 2000 + 500
        self.pwm.set_servo_pulsewidth(self.pin, width)
        time.sleep(1)
        self.pwm.set_PWM_dutycycle(self.pin, 0)

    def __delete__(self):
        self.pwm.stop()
