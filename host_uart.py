import serial
import time

# UART Configuration
# PORT = '/dev/pts/11'  # Virtual serial port
PORT = 'COM3'
BAUD_RATE = 2400
TIMEOUT = 10
TOTAL_BITS_PER_PACKET = 10 # (8 data + 1 start + 1 stop)

data = """
Finance Minister Arun Jaitley Tuesday hit out at former RBI governor Raghuram Rajan for predicting that the next banking crisis would be triggered by MSME lending, saying postmortem is easier than taking action when it was required. Rajan, who had as the chief economist at IMF warned of impending financial crisis of 2008, in a note to a parliamentary committee warned against ambitious credit targets and loan waivers, saying that they could be the sources of next banking crisis. Government should focus on sources of the next crisis, not just the last one.

In particular, government should refrain from setting ambitious credit targets or waiving loans. Credit targets are sometimes achieved by abandoning appropriate due diligence, creating the environment for future NPAs," Rajan said in the note." Both MUDRA loans as well as the Kisan Credit Card, while popular, have to be examined more closely for potential credit risk. Rajan, who was RBI governor for three years till September 2016, is currently.
"""

def main():
	# Open the serial port
	with serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT) as ser:
		transmit_times = []
		receive_times = []

		# Data transmission
		for byte in data.encode('utf-8'):
			start_time = time.time()
			ser.write([byte])  # Write one byte at a time
			end_time = time.time()
			transmit_times.append(end_time - start_time)

		# Calculate average transmit speed
		total_transmit_time = sum(transmit_times)
		total_bits = len(data) * TOTAL_BITS_PER_PACKET  # 10 bits per byte (8 data + 1 start + 1 stop)
		average_transmit_speed = total_bits / total_transmit_time
		print(f"Average transmit speed: {average_transmit_speed} bits per second")

		# Data receival
		received_data = []
		for _ in range(len(data)):
			start_time = time.time()
			print("lol")
			received_byte = ser.read(1)  # Read one byte at a time
			end_time = time.time()
			if received_byte:
				received_data.append(received_byte.decode('utf-8'))
				receive_times.append(end_time - start_time)

		# Calculate average receive speed
		total_receive_time = sum(receive_times)
		average_receive_speed = total_bits / total_receive_time  # Assuming received data length is same as transmitted
		print(f"Average receive speed: {average_receive_speed} bits per second")

		# Print the data received
		print("Received data:")
		print(''.join(received_data))

if __name__ == "__main__":
    main()
