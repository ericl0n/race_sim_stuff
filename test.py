import serial

port = 'COM6'
baudrate = 9600

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
            
def write_com_port(port, baudrate, text):
    ser = serial.Serial(port, baudrate)
    data = text.encode('utf-8')
    ser.write(data)
    return("done")
    
print(read_com_port(port,baudrate))
print(write_com_port(port,baudrate,"h"))