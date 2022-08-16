import serial

with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
    s = ser.read(10)
print(s)
