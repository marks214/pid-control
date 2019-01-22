# Multimeter
# 

import matplotlib.pyplot as plt
import matplotlib.animation as animation #Required to live plot
import numpy as np
import csv
import time #Required to timestamp & delay functions
from pylive import live_plotter
import pyfirmata #facilitates communication with Arduino https://pyfirmata.readthedocs.io/en/latest/
from progress.bar import ChargingBar #required to display a charging bar


portName = 'COM3'
arduino = pyfirmata.Arduino(portName)
it = pyfirmata.util.Iterator(arduino)
it.start()

#Connect to arduino hardware on input port.
input_pin = arduino.get_pin('a:0:i') #analog, input to the computer
input_pinV = arduino.get_pin('a:1:i') #analog, input to the computer
output_pin = arduino.get_pin('d:3:p') #digital, PWM from the computer

# Set digital pin 3 to high to heat up resistor R2
output_pin.write(1)
time.sleep(1)
signal0 = input_pin.read()
voltage = input_pinV.read()
print(signal0, 'signal0', voltage, 'voltage')

"""bar = ChargingBar('Heating up...', max=20)
signal1 = 0
for i in range(20):
    time.sleep(5)
    bar.next()
bar.finish()"""