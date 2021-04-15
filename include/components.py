import smbus, time, glob, include.grovepi as grovepi

# Water Sensor
bus = smbus.SMBus(1)

# DS18B20
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

class Relay(object):
    def __init__(self, pin):
        self.pin = pin
        self.status = 'OFF'
        
        grovepi.pinMode(self.pin, 'OUTPUT')

    def toggle(self):
        if self.status == 'OFF':
            self.status = 'ON'
            grovepi.digitalWrite(self.pin, 1)
        else:
            self.status = 'OFF'
            grovepi.digitalWrite(self.pin, 0)

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
    def __init__(self, pin):
        self.pin = 4
        self.module_type = 0
    
    def read_temp(self):
        return grovepi.dht(self.pin, self.module_type)[0]

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
        self.pin = 0
        self.offset = 41.02740741
        self.samplingInterval = 20
        self.printInterval = 20
        self.arrayLenth = 40
        
        self.pHArray = [0] * self.arrayLenth
        self.pHArrayIndex = 0

        self.samplingTime = time.time()
        self.printTime = time.time()
    
    def read(self):
        if (time.time() - self.samplingTime > self.samplingInterval):
            self.pHArrayIndex += 1
            self.pHArray[self.pHArrayIndex] = grovepi.analogRead(self.pin)
            print(self.pHArray[self.pHArrayIndex])
            if (self.pHArrayIndex == self.arrayLenth):
                self.pHArrayIndex = 0
                voltage = self.avergearray(self.pHArray, self.arrayLenth) * 5.0 / 1024
                pHValue = -19.18518519 * voltage + self.offset
                self.samplingTime = time.time()
        if (time.time() - self.printTime > self.printInterval):  #Every 800 milliseconds, print a numerical, convert the state of the LED indicator
            print("Voltage:")
            print(voltage)
            print("pH value: ")
            print(pHValue)
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