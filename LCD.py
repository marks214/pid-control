import pyfirmata #facilitates communication with Arduino https://pyfirmata.readthedocs.io/en/latest/
import numpy as np
from time import sleep
from pyfirmata import Arduino, util, STRING_DATA


try:
    portName = 'COM3' #assigns a variable
    arduino = pyfirmata.Arduino(portName) #creates an instance of a class
    it = pyfirmata.util.Iterator(arduino)
    it.start() #calls a start method

    #Connect to arduino hardware on input port.
    input_pin = arduino.get_pin('a:0:i') #analog, input to the computer
    sleep(1)

    Vout = input_pin.read()
    print(Vout*5, 'Vout')
    arduino.send_sysex( STRING_DATA, util.str_to_two_byte_iter(str(Vout*5) + str(' Vout')) )

finally:
    arduino.exit()


