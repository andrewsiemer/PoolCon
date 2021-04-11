import smbus
import RPi.GPIO as GPIO
import time
from include.di_i2c import DI_I2C
import math
import sys
import struct
import numpy

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
bus = smbus.SMBus(1)
relay_state = 0

address = 0x04
max_recv_size = 10
unused = 0
retries = 10
additional_waiting = 0
relay_cmd = [10]
dht_temp_cmd = [40]
data_not_available_cmd = [23]

if sys.version_info<(3,0):
	p_version = 2
else:
	p_version = 3

def set_bus(bus):
	global i2c
	i2c = DI_I2C(bus = bus, address = address)

set_bus("RPI_1SW")

def write_i2c_block(block, i2c):
	'''
	Now catches and raises Keyboard Interrupt that the user is responsible to catch.
	'''
	counter = 0
	reg = block[0]
	data = block[1:]
	while counter < 3:
		try:
			i2c.write_reg_list(reg, data)
			time.sleep(0.002 + additional_waiting)
			return
		except KeyboardInterrupt:
			raise KeyboardInterrupt
		except:
			counter += 1
			time.sleep(0.003)
			continue

def read_identified_i2c_block(read_command_id, no_bytes, i2c):

	data = [-1]
	while data[0] != read_command_id[0]:
		data = read_i2c_block(no_bytes + 1, i2c)

	return data[1:]

def read_i2c_block(no_bytes = max_recv_size, i2c):
	'''
	Now catches and raises Keyboard Interrupt that the user is responsible to catch.
	'''
	data = data_not_available_cmd
	counter = 0
	while data[0] in [data_not_available_cmd[0], 255] and counter < 3:
		try:
			data = i2c.read_list(reg = None, len = no_bytes)
			time.sleep(0.002 + additional_waiting)
			if counter > 0:
				counter = 0
		except KeyboardInterrupt:
			raise KeyboardInterrupt
		except:
			counter += 1
			time.sleep(0.003)
			
	return data

class DHT11(object):
    def __init__(self, sensor):
        self.sensor = 4
        self.module_type = 0
        self.last = 0
    
    def read_temp(self):
        write_i2c_block(dht_temp_cmd + [self.sensor, self.module_type, unused], i2c)
        number = read_identified_i2c_block(dht_temp_cmd, no_bytes=8, i2c=i2c)

        if p_version==2:
            h=''
            for element in (number[0:4]):
                h+=chr(element)

            t_val=struct.unpack('f', h)
            t = round(t_val[0], 2)

            h = ''
            for element in (number[4:8]):
                h+=chr(element)

            hum_val=struct.unpack('f',h)
            hum = round(hum_val[0], 2)
        else:
            t_val=bytearray(number[0:4])
            h_val=bytearray(number[4:8])
            t=round(struct.unpack('f',t_val)[0],2)
            hum=round(struct.unpack('f',h_val)[0],2)
        if t > -100.0 and t < 150.0 and hum >= 0.0 and hum <= 100.0:
            temp_f = t * 9.0 / 5.0 + 32.0
            self.last = temp_f
            return temp_f
        else:
            return self.last

class Relay(object):
    def __init__(self, channel):
        self.addr = 0x11
        self.channel = channel
        self.status = 'OFF'
        self.i2c = DI_I2C(bus = "RPI_1SW", address = 0x11)

    def toggle(self):
        global relay_state

        if self.status == 'OFF':
            self.status = 'ON'
            relay_state |= (1 << (self.channel - 1))
            write_i2c_block(relay_cmd + [self.addr, relay_state, unused])
            read_i2c_block(no_bytes=1)

        else:
            self.status = 'OFF'
            relay_state &= ~(1 << (self.channel - 1))
            write_i2c_block(relay_cmd + [self.addr, relay_state, unused])
            read_i2c_block(no_bytes=1)

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
