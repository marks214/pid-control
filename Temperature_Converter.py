import time
import numpy as np
from arduino_helper import ArduinoHelper
import helpers
from itertools import cycle

board = ArduinoHelper()

try:   
    # Set digital pin 6 to high to heat up 220 ohm resistor
    board.update_duty_cycle(1)
    time.sleep(1)
    signal0 = board.read_input_pin()
    board.write_to_lcd('Warming Up...')
    helpers.display_loading_bar(10)

    signal1 = board.read_input_pin()
    
    # Set the output of digital pin 6 to low (0V)
    board.update_duty_cycle(0)
    T_Celcius = helpers.calculate_temperature(signal0, signal1)

    messages = cycle([str(round(signal0, 2)) + ' initial V', 
                str(round(signal1, 2)) + ' final V', 
                str(round(signal1 - signal0 , 2)) + ' \u0394' + 'V',
                str(round(T_Celcius, 2)) + ' C' ])
    board.write_to_lcd('All Done!')
    previous_switch_on = board.is_switch_on()   
    while True:
        switch_on = board.is_switch_on()
        if switch_on != previous_switch_on and not switch_on:
            board.write_to_lcd("off")
        elif switch_on != previous_switch_on:
            board.write_to_lcd(next(messages))
        previous_switch_on = switch_on
        time.sleep(.1)

except KeyboardInterrupt:
    board.write_to_lcd('FINISHED')
finally:
    board.arduino.exit()