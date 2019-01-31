import csv
import time  # Required to timestamp & delay functions
import numpy as np
from itertools import cycle
# We want to collect experimental data
# describing the response of the measured T to the changes
# in the control input
# change the duty cycle (DC) of the PWM

from progress.bar import ChargingBar  # required to display a charging bar
from arduino_helper import ArduinoHelper

board = ArduinoHelper()
start_time = time.time()
file_name = '_Lab_on_a_Chip_thermal_response_no_dt' + str(start_time) + '.csv'
signal0 = board.read_input_pin()
board.write_to_lcd(round(signal0, 2), ' initial V')

#TODO: loop for generation of DC_values array

DC_values = [1, 0]# 0.2, 0, 0.3, 0, 0.4, 0, 0.5, 0, 0.6, 0, 0.7, 0, 0.8, 0, 0.9, 0, 1, 0]

seconds_between_readings = 1
seconds_to_equalize_min = 10
seconds_to_equalize_max = 400

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
    return temperature, incoming_voltage

def record_temperature(temperature, DC, incoming_voltage):
    try:
        with open(file_name, 'a', newline='') as csvfile:
            temperaturewriter = csv.writer(csvfile, delimiter=',')
            temperaturewriter.writerow([time.time() - start_time, DC, temperature, incoming_voltage, '5', ''])  
    except:
        board.write_to_lcd("weird file error", time.time())

def stabilize_initial():
    board.update_duty_cycle(0)
    next_stable_time = time.time() + 2#0
    while time.time() < next_stable_time:
        temperature, _ = measure_temperatures(0)
        if temperature < 23 or temperature > 28:
            raise Exception("Temperature during stabilization period out of expected range")
        time.sleep(seconds_between_readings)



def run():  
    with open(file_name, 'a', newline='') as csvfile:
        temperaturewriter = csv.writer(csvfile, delimiter=',')
        temperaturewriter.writerow(['time', 'DC', 'temperature', 'incoming_voltage', 'input5V_voltage', 'set_point_temperature'])
    stabilize_initial()

    previous_switch_on = board.is_switch_on()

    for DC in DC_values:
        board.update_duty_cycle(DC)
        next_stable_time = time.time() + seconds_to_equalize_max
        message_index = cycle([0,1,2])
        while time.time() < next_stable_time:            
            (temperature, voltage) = measure_temperatures(DC)
            if temperature < 20:
                raise Exception("Temperature shouldn't go down")
            
            messages = [str(DC) + ' DC', 
                str(round(voltage, 2)) + ' V', 
                str(round(temperature, 2)) + ' C' ]

            switch_on = board.is_switch_on()
            if switch_on != previous_switch_on and not switch_on:
                board.write_to_lcd("off")
            elif switch_on != previous_switch_on:
                i = next(message_index)
                board.write_to_lcd(messages[i])
            previous_switch_on = switch_on
            time.sleep(.1)
            time.sleep(seconds_between_readings)

try:
    run()
except KeyboardInterrupt:
    board.write_to_lcd('stopped')
finally:
    board.write_to_lcd('FIN')
    board.output_pin.write(0)
    board.arduino.exit()
