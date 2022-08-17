# import serial

# with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
#     # s = ser.read(10)
#     line = ser.readline()
# print(line)

import time
import serial

print('Running LW20 sample.')

# Make a connection to the com port.
serialPortName = '/dev/ttyUSB0'
serialPortBaudRate = 115200
port = serial.Serial(serialPortName, serialPortBaudRate, timeout=0.1)

# Enable serial mode by sending some characters over the serial port.
port.write('www\r\n')
# Read and ignore any unintended responses
port.readline()

# Get the product information
port.write('?\r\n')
productInfo = port.readline()
print('Product information: ' + productInfo)

while True:	
	# Get distance reading (First return, default filtering)
	port.write('LD\r\n')
	distanceStr = port.readline()
	# Convert the distance string response into a number
	distanceCM = float(distanceStr)

	# Do what you want with the distance information here
	print('standoff: {0:.2f} m'.format(distanceCM))

	# Wait for 50ms before the next reading is taken
	time.sleep(0.05)
