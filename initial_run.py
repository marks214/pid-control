from arduino_helper import ArduinoHelper
import time

try:
    board = ArduinoHelper()
    board.write_to_lcd('WELCOME!!!')

    while True:
        Vout = board.read_input_pin()
        output = str(round(Vout, 3)) +  ' VA0'
        switch_on = board.is_switch_on()
        if  switch_on:
            output += ' ON'
        else:
            output += ' OFF'
        board.write_to_lcd(output)
except KeyboardInterrupt:
    print('Program Stopped.')
finally:
    board.arduino.exit()



