import serial
import time

# UART Configuration
PORT = '/dev/pts/9'  # Virtual serial port
BAUD_RATE = 2400  # Increased baud rate
TIMEOUT = 10
TOTAL_BITS_PER_PACKET = 10  # (8 data + 1 start + 1 stop)

data = """
Finance Minister Arun Jaitley Tuesday hit out at former RBI governor Raghuram Rajan for predicting that the next banking crisis would be triggered by MSME lending, saying postmortem is easier than taking action when it was required. Rajan, who had as the chief economist at IMF warned of impending financial crisis of 2008, in a note to a parliamentary committee warned against ambitious credit targets and loan waivers, saying that they could be the sources of next banking crisis. Government should focus on sources of the next crisis, not just the last one.

In particular, government should refrain from setting ambitious credit targets or waiving loans. Credit targets are sometimes achieved by abandoning appropriate due diligence, creating the environment for future NPAs," Rajan said in the note." Both MUDRA loans as well as the Kisan Credit Card, while popular, have to be examined more closely for potential credit risk. Rajan, who was RBI governor for three years till September 2016, is currently.
"""

def main():
	# Open the serial port
	with serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT) as ser:
		start_time = time.time()
		ser.write(data.encode('utf-8'))
		end_time = time.time()

		# Calculate transmission time for whole message
		total_bits = len(data) * TOTAL_BITS_PER_PACKET
		average_transmit_speed = total_bits / (end_time - start_time)
		print(f"Average transmit speed: {average_transmit_speed} bits per second")

		# Receive data
		start_time = time.time()
		received_data = ser.read(len(data))
		end_time = time.time()
		print("Received data:")
		print(received_data.decode('utf-8'))

		# Calculate average receive speed
		average_receive_speed = total_bits / (end_time - start_time)
		print(f"Average receive speed: {average_receive_speed} bits per second")

if __name__ == "__main__":
    main()
