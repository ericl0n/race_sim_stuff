import serial
import vgamepad as vg
import time
from cvs_stuff import *


max_val = 1
min_val = 0

def setup_vals():
    global max_val
    global min_val
    val = read_record("max_min.csv")
    max_val = int(val[0][0])
    min_val = int(val[0][1])

def read_com_port(port, baudrate):
    ser = serial.Serial(port, baudrate)
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            try:
                value = int(line)
                return value
            except ValueError:
                continue

def convert_input_to_handbrake_value(input_value):
    # Assuming input_value ranges from 0 to 256
    
    handbrake_value = (input_value - min_val) / (max_val - min_val)
    if handbrake_value > 1.0:
        handbrake_value = 1.0
    elif handbrake_value < 0.0:
        handbrake_value = 0.0
    else:
        pass
    return round(handbrake_value,2)

def value_to_other_application(port,baudrate):
    input_value = read_com_port(port, baudrate)
    handbrake_value = convert_input_to_handbrake_value(input_value)
    return int(handbrake_value * 100)

def run_application(port,baudrate):
    gamepad = vg.VX360Gamepad() # make virtual xbox360 controller
    while True:
        input_value = read_com_port(port, baudrate)
        handbrake_value = convert_input_to_handbrake_value(input_value)
        gamepad.left_joystick_float(x_value_float = handbrake_value, y_value_float = 0.0)
        gamepad.update()
        #print(f"Handbrake Value: {handbrake_value}")
        #print(input_value)
        time.sleep(0.1)

def gamepad_setup():
    gamepad = vg.VX360Gamepad()
    return gamepad

def output_to_ver_controlr(gamepad,handbrake_value):
    gamepad.left_joystick_float(x_value_float = handbrake_value, y_value_float = 0.0)
    gamepad.update()

if __name__ == "__main__":
    port = 'COM6'  # Replace with your COM port
    baudrate = 4800  # Replace with your baud rate
    gamepad = vg.VX360Gamepad() # make virtual xbox360 controller
    while True:
        input_value = read_com_port(port, baudrate)
        handbrake_value = convert_input_to_handbrake_value(input_value)
        gamepad.left_joystick_float(x_value_float = handbrake_value, y_value_float = 0.0)
        gamepad.update()
        print(f"Handbrake Value: {handbrake_value}")
        #print(input_value)
        time.sleep(0.1)
