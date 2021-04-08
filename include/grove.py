import smbus
import RPi.GPIO as GPIO
import time

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
bus = smbus.SMBus(1)
relay_state = 0

class Relay(object):
    def __init__(self, channel):
        self.addr = 0x11
        self.channel = channel
        self.status = 'OFF'

    def toggle(self):
        global relay_state)

        if self.status == 'OFF':
            self.status = 'ON'
            relay_state |= (1 << (self.channel - 1))
            bus.write_byte_data(self.addr, 0, 0x10)
            bus.write_byte_data(self.addr, 0, relay_state)

        else:
            self.status = 'OFF'
            relay_state &= ~(1 << (channel - 1))
            bus.write_byte_data(self.addr, 0, 0x10)
            bus.write_byte_data(self.addr, 0, relay_state)

        return self.status

class WaterSensor(object):
    def __init__(self):
        self.low_addr = 0x77
        self.high_addr = 0x78

        self.sensorvalue_min = 250 
        self.sensorvalue_max = 255

    def read(self):
        touch_val = 0
        trig_section = 0
        low_count = 0
        high_count = 0

        low_data = bus.read_i2c_block_data(self.low_addr, 0, 8)
        high_data = bus.read_i2c_block_data(self.high_addr, 0, 12)

        for i in range(0,8):
            if (low_data[i] >= self.sensorvalue_min and low_data[i] <= self.sensorvalue_max):
                low_count += 1
            if (low_count == 8):
                print('Pass')
        for i in range(0,12):
            if (high_data[i] >= self.sensorvalue_min and high_data[i] <= self.sensorvalue_max):
                low_count += 1
            if (high_count == 12):
                print('Pass')

        for i in range(0,8):
            if low_data[i] > 100:
                touch_val |= 1 << i

        for i in range(0,12):
            if high_data[i] > 100:
                touch_val |= 1 << (8+i)

        while touch_val & 0x01:
            trig_section += 1
            touch_val >>= 1

        return trig_section * 5


if __name__ == '__main__':
    GPIO.setup(23,GPIO.OUT)
    while(1):
        if flag:
            GPIO.output(23,GPIO.HIGH)
            flag = False
        else:
            GPIO.output(23,GPIO.LOW)
            flag = True

        time.sleep(1)
