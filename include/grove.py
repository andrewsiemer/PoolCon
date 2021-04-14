import smbus, time, math, sys, struct, numpy, serial, glob
import RPi.GPIO as GPIO
from include.di_i2c import DI_I2C
 
# Relay
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Water Sensor
bus = smbus.SMBus(1)

# DS18B20
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# GrovePi+
address = 0x04
max_recv_size = 10
unused = 0
retries = 10
additional_waiting = 0
dht_temp_cmd = [40]
data_not_available_cmd = [23]
if sys.version_info<(3,0):
	p_version = 2
else:
	p_version = 3

# PHsensor
ser = None

def set_bus(bus):
	global i2c
	i2c = DI_I2C(bus = bus, address = address)

set_bus("RPI_1SW")

def setup_serial():
    global ser
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.01
    )

def write_i2c_block(block, i2c = i2c):
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

def read_identified_i2c_block(read_command_id, no_bytes, i2c = i2c):
	data = [-1]
	while data[0] != read_command_id[0]:
		data = read_i2c_block(no_bytes + 1)

	return data[1:]

def read_i2c_block(no_bytes = max_recv_size, i2c = i2c):
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

class Relay(object):
    def __init__(self, pin):
        self.pin = pin
        self.status = 'OFF'

        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def toggle(self):
        if self.status == 'OFF':
            self.status = 'ON'
            GPIO.output(self.pin, GPIO.HIGH)
        else:
            self.status = 'OFF'
            GPIO.output(self.pin, GPIO.LOW)

        return self.status

class DS18B20(object):
    def __init__(self):
        pass

    def read_temp_raw(self):
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
    
    def read(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_f

class DHT11(object):
    def __init__(self, sensor):
        self.sensor = 4
        self.module_type = 0
        self.last = 0
    
    def read_temp(self):
        write_i2c_block(dht_temp_cmd + [self.sensor, self.module_type, unused])
        number = read_identified_i2c_block(dht_temp_cmd, no_bytes=8)

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

class PHsensor(object):
    def __init__(self, pin):
        self.pin = pin
        self.offset = 41.02740741
        self.samplingInterval = 20
        self.printInterval = 20
        self.arrayLenth = 40
        
        self.pHArray = [0] * self.arrayLenth
        self.pHArrayIndex = 0

        self.samplingTime = time.time()
        self.printTime = time.time()
    
    def read(self):
        global ser
        if (time.time() - self.samplingTime > self.samplingInterval):
            print('asd')
            self.pHArrayIndex += 1
            self.pHArray[self.pHArrayIndex] = ser.readline()
            print(self.pHArray[self.pHArrayIndex])
            if (self.pHArrayIndex == self.arrayLenth):
                self.pHArrayIndex = 0
                voltage = self.avergearray(self.pHArray, self.arrayLenth) * 5.0 / 1024
                pHValue = -19.18518519 * voltage + self.offset
                self.samplingTime = time.time()
        if (time.time() - self.printTime > self.printInterval):  #Every 800 milliseconds, print a numerical, convert the state of the LED indicator
            print("Voltage:")
            print(voltage, 2)
            print("    pH value: ")
            print(pHValue, 2)
            self.printTime = time.time()

            return pHValue
        
        
    def avergearray(self, arr, number):
        amount = 0
        if (number <= 0):
            print("Error number for the array to avraging!/n")
            return 0
        if (number < 5): #less than 5, calculated directly statistics
            for i in range(0,number):
                amount += arr[i]
            avg = amount / number
            return avg
        else:
            if (arr[0] < arr[1]):
                min = arr[0]
                max = arr[1]
            else:
                min = arr[1]
                max = arr[0]
            for i in range(2,number):
                if (arr[i] < min):
                    amount += min # arr<min
                    min = arr[i]
                else:
                    if (arr[i] > max):
                        amount += max # arr>max
                        max = arr[i]
                    else:
                        amount += arr[i] # min<=arr<=max
            avg = amount / (number - 2)
        return avg

class ORPsensor(object):
    def __init__(self, pin):
        pass
    
    def read(self):
        pass