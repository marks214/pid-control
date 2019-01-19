import csv
import time  # Required to timestamp & delay functions
import numpy as np
# We want to collect experimental data
# describing the response of the measured T to the changes
# in the control input
# change the duty cycle (DC) of the PWM
# 
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation #Required to live plot
#from pylive import live_plotter
from progress.bar import ChargingBar  # required to display a charging bar
from arduino_helper import ArduinoHelper

board = ArduinoHelper()
signal0 = board.read_input_pin()
print(signal0, 'signal0')

DC_values = [1]

seconds_between_readings = 1
seconds_to_equalize_min = 10
seconds_to_equalize_max = 360

def get_temperature(incoming_voltage):
    """
        incoming_voltage should be in volts (between 0 and 5)
    """
    # read from arduino and do calculation
    R_ratio = np.log((signal0/incoming_voltage)*(5-incoming_voltage)/(5-signal0))
    T_Kelvin = 1/( ( 0.003354016 + 0.0002569850*R_ratio + 2.620131e-06*R_ratio**2 + 6.383091e-08*R_ratio**3 ))
    T_Celcius = (T_Kelvin)-273.15
    return T_Celcius

def measure_temperatures(DC):
    incoming_voltage = board.read_input_pin()
    temperature = get_temperature(incoming_voltage)
    record_temperature(temperature, DC, incoming_voltage)
    return temperature

def record_temperature(temperature, DC, incoming_voltage):
    try:
        with open('_Lab_on_a_Chip' + str(board.start_time) + '.csv', 'a', newline='') as csvfile:
            temperaturewriter = csv.writer(csvfile, delimiter=',')
            temperaturewriter.writerow([time.time() - board.start_time, DC, temperature, incoming_voltage, '5'])  
    except:
        print("weird file error", time.time())

def stabilize_initial():
    board.update_duty_cycle(0)
    next_stable_time = time.time() + 20
    while time.time() < next_stable_time:
        temperature = measure_temperatures(0)
        if temperature < 23 or temperature > 28:
            raise Exception("Temperature during stabilization period out of expected range")
        time.sleep(seconds_between_readings)

def run():  
    stabilize_initial()

    for DC in DC_values:
        board.update_duty_cycle(DC)
        next_stable_time = time.time() + seconds_to_equalize_max
        while time.time() < next_stable_time:            
            temperature = measure_temperatures(DC)
            if temperature < 23:
                raise Exception("Temperature shouldn't go down")
            time.sleep(seconds_between_readings)

try:
    run()
except KeyboardInterrupt:
    print('Keyboard Interrupt')
finally:
    board.output_pin.write(0)
    board.arduino.exit()
