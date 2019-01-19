
import numpy as np
import csv
import time #Required to timestamp & delay functions
#from pylive import live_plotter
import pyfirmata #facilitates communication with Arduino https://pyfirmata.readthedocs.io/en/latest/
from progress.bar import ChargingBar #required to display a charging bar
from random import shuffle


#tuning parameters (constants):

KC = 2*0.158
TI = 131.949

# change values in this method (temperature/time)
def get_set_point_temperature(time):
    if time <= 240:
        return 33 #degrees C
    if time > 2400:
        return 36 #degrees C

def get_change_in_DC(current_temperature, previous_temperature, delta_time, set_point_temperature):
    EN_previous = set_point_temperature - previous_temperature
    EN_current = set_point_temperature - current_temperature
    return KC*(EN_current - EN_previous + (delta_time/TI) * EN_current)

portName = 'COM4'
arduino = pyfirmata.Arduino(portName)

it = pyfirmata.util.Iterator(arduino)
it.start()

start_time = time.time()

input_pin = arduino.get_pin('a:0:i') #analog, input to the computer
#input5V_pin = arduino.get_pin('a:1:i') #analog, input to the computer
output_pin = arduino.get_pin('d:6:p') #digital, PWM mode, from the computer


def read_voltage(pin):
#this acts as a multimeter
    outputs = []
    for i in range(40):
        time.sleep(0.05)
        outputs.append(pin.read())
    return 5.0 * np.average(outputs)

output_pin.write(0)
time.sleep(10)
signal0 = read_voltage(input_pin)
initial_5V = (1000+220)/220*5
#initial_5V = (1000+220)/220*read_voltage(input5V_pin)
print(signal0, 'signal0')
print(initial_5V, 'initial_5V')



def update_duty_cycle(DC): 
    output_pin.write(DC)

def get_temperature(incoming_voltage, input5V_voltage):
    # read from arduino and do calculation
    ln_R4_over_R3 = np.log((incoming_voltage/signal0)*((initial_5V-signal0)/(input5V_voltage-incoming_voltage)))
    T_Kelvin = 1/( ( 0.003354016 + 0.0002569850*ln_R4_over_R3 + 2.620131e-06*ln_R4_over_R3**2 + 6.383091e-08*ln_R4_over_R3**3 ))
    T_Celcius = (T_Kelvin)-273.15
    return T_Celcius

def measure_temperatures(DC):
    incoming_voltage = read_voltage(input_pin)
    input5V_voltage = (1000+220)/220*read_voltage(input5V_pin)
    current_time = time.time()
    temperature = get_temperature(incoming_voltage, input5V_voltage)
    record_temperature(temperature, DC, incoming_voltage, input5V_voltage)
    return temperature, current_time

def record_temperature(temperature, DC, incoming_voltage, input5V_voltage):
    try:
        with open('_4203_project_4' + str(start_time) + '.csv', 'a', newline='') as csvfile:
            temperaturewriter = csv.writer(csvfile, delimiter=',')
            temperaturewriter.writerow([time.time() - start_time, DC, temperature, incoming_voltage, input5V_voltage, get_set_point_temperature(time.time()-start_time)])  
    except:
        print("weird file error", time.time())

def run():
    with open('_4203_project_4' + str(start_time) + '.csv', 'a', newline='') as csvfile:
        temperaturewriter = csv.writer(csvfile, delimiter=',')
        temperaturewriter.writerow(['time', 'DC', 'temperature', 'incoming_voltage', 'input5V_voltage', 'set_point_temperature'])
    DC = 0.1
    update_duty_cycle(DC)
    previous_temperature, previous_time = measure_temperatures(DC)
    time.sleep(3)
    current_temperature, current_time = measure_temperatures(DC)
    while current_time - start_time < 4800:
        delta_time = current_time - previous_time
        test = get_set_point_temperature(current_time-start_time)
        DC = DC + get_change_in_DC(current_temperature, previous_temperature, delta_time, test)
        if DC > 1:
                DC = 1
        if DC < 0:
                DC = 0
        update_duty_cycle(DC)
        previous_temperature = current_temperature
        previous_time = current_time
        current_temperature, current_time = measure_temperatures(DC)
        print(DC)
        print(current_temperature)
        print('seconds' + str(current_time - start_time))



run()
output_pin.write(0)
