import time  # Required to timestamp & delay functions
from random import shuffle
import numpy as np
from pyfirmata import Arduino, util, STRING_DATA

class  ArduinoHelper(object):
    portName = 'COM3'

    def __init__(self):
        self.arduino = Arduino(self.portName)
        it = util.Iterator(self.arduino)
        it.start()
        self.start_time = time.time()
        self.input_pin = self.arduino.get_pin('a:0:i') #analog, input to the computer
        self.output_pin = self.arduino.get_pin('d:6:p') #digital, PWM mode, from the computer
        self.switch_pin = self.arduino.get_pin('d:9:i') #digital, input to the computer (switch-state)

        # make sure the PWM pin (6) is off, wait a number of seconds
        # (gives enough time so everything is ready to be read - otherwise it may read "None")
        time.sleep(2)
        self.update_duty_cycle(0)

    def read_input_pin(self):
        return self.read_voltage(self.input_pin)

    def read_voltage(self, pin):
        """
            Returns the voltage of the pin passed in (between 0 and 5 Volts)
            It takes a number of measurements, then averages them to reduce noise
        """
        outputs = []
        for i in range(10):
            time.sleep(.1)
            outputs.append(pin.read())
        return 5.0 * np.average(outputs)

    def read_voltage_fast(self, pin):
        """
            Returns the voltage of the pin passed in (between 0 and 5 Volts)
            It takes a single of measurement
        """
        return 5.0 * pin.read()

    def write_to_lcd(self, *args):
        message = ''
        for arg in args:
            message += str(arg)
            
        print(message)   
        self.arduino.send_sysex(STRING_DATA, util.str_to_two_byte_iter(str(message)))
        
    def is_switch_on(self):
        switch_voltage = self.read_voltage_fast(self.switch_pin)
        return switch_voltage > 1


    def update_duty_cycle(self, DC): 
        self.output_pin.write(DC)