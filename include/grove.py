import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23,GPIO.OUT)

class Relay(object):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin,GPIO.OUT)
        self.status = 'OFF'
    
    def toggle(self):
        if self.status == 'OFF':
            self.status = 'ON'
            GPIO.output(self.pin,GPIO.HIGH)
        else:
            self.status = 'OFF'
            GPIO.output(self.pin,GPIO.LOW)

        return self.status

if __name__ == '__main__':
    while(1):
        if flag:
            GPIO.output(23,GPIO.HIGH)
            flag = False
        else:
            GPIO.output(23,GPIO.LOW)
            flag = True

        time.sleep(1)
