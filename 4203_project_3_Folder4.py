
portName = 'COM4'
arduino = pyfirmata.Arduino(portName)

it = pyfirmata.util.Iterator(arduino)
it.start()

import csv
import time  # Required to timestamp & delay functions
from random import shuffle

import numpy as np
# We want to collect experimental data
# describing the response of the measured T to the changes
# in the control input
# change the duty cycle (DC) of the PWM
# 
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation #Required to live plot
#from pylive import live_plotter
import pyfirmata  # facilitates communication with Arduino https://pyfirmata.readthedocs.io/en/latest/
from progress.bar import ChargingBar  # required to display a charging bar

start_time = time.time()

input_pin = arduino.get_pin('a:0:i') #analog, input to the computer
input5V_pin = arduino.get_pin('a:1:i') #analog, input to the computer
output_pin = arduino.get_pin('d:6:p') #digital, PWM mode, from the computer

def read_voltage(pin):
    outputs = []
    for i in range(10):
        time.sleep(.1)
        outputs.append(pin.read())
    return 5.0 * np.average(outputs)

output_pin.write(0)
time.sleep(10)
signal0 = read_voltage(input_pin)
initial_5V = (1000+220)/220 #*read_voltage(input5V_pin)
print(signal0, 'signal0')
print(initial_5V, 'initial_5V')

#DC_values = [0.25, 0, 0.5, 0, 0.75, 0, 1, 0, 0.25, 0.5, 0.75, 1, 0.75, 0.5, 0.25, 0]
#DC_values = [0.5, 1, 0.5, 0]
#DC_values = [0.25, 1, 0.25, 0.75, 0.25]
DC_values = [0.1, 0, 0.2, 0, 0.3, 0, 0.4, 0, 0.5, 0, 0.6, 0, 0.7, 0, 0.8, 0, 0.9, 0, 1, 0, 0.15, 0, 0.25, 0, 0.35, 0]

seconds_between_readings = 1
seconds_to_equalize_min = 10
seconds_to_equalize_max = 120

def update_duty_cycle(DC): #DC = duty cycle
    output_pin.write(DC)

def get_temperature(incoming_voltage, input5V_voltage):
    # read from arduino and do calculation
    ln_R4_over_R3 = np.log((incoming_voltage/signal0)*((initial_5V-signal0)/(input5V_voltage-incoming_voltage)))
    T_Kelvin = 1/( ( 0.003354016 + 0.0002569850*ln_R4_over_R3 + 2.620131e-06*ln_R4_over_R3**2 + 6.383091e-08*ln_R4_over_R3**3 ))
    T_Celcius = (T_Kelvin)-273.15
    return T_Celcius

def measure_temperatures(DC):
    incoming_voltage = read_voltage(input_pin)
    input5V_voltage = (1000+220)/220*5 #read_voltage(input5V_pin)
    temperature = get_temperature(incoming_voltage, input5V_voltage)
    record_temperature(temperature, DC, incoming_voltage, input5V_voltage)

def record_temperature(temperature, DC, incoming_voltage, input5V_voltage):
    try:
        with open('_Lab_on_a_Chip' + str(start_time) + '.csv', 'a', newline='') as csvfile:
            temperaturewriter = csv.writer(csvfile, delimiter=',')
            temperaturewriter.writerow([time.time() - start_time, DC, temperature, incoming_voltage, input5V_voltage])  
    except:
        print("weird file error", time.time())

def run():
    update_duty_cycle(0)
    next_stable_time = time.time() + 60
    while time.time() < next_stable_time:
        measure_temperatures(0)
        time.sleep(seconds_between_readings)

    for DC in DC_values:
        update_duty_cycle(DC)
        next_stable_time = time.time() + seconds_to_equalize_max
        while time.time() < next_stable_time:
            measure_temperatures(DC)
            time.sleep(seconds_between_readings)
    
        #line1 = live_plotter(DC_values,temperature_values,line1)
#     line1 = live_plotter(DC_values,temperature_values,line1)
# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)
"""def animate(i):
    pullData = open('4203_project_3.csv',"r").read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    ax1.clear()
    ax1.plot(xar,yar)
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
"""       

run()
output_pin.write(0)
wait = input("Press Enter to Continue")
