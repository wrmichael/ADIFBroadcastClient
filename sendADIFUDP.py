import socket
import colored
import datetime
import sys

LOGFILE, HISTORYFILE = sys.argv[1], sys.argv[2]
print("Log file:" + LOGFILE)
print("HISTORY file:" + HISTORYFILE)


UDP_IP = "127.0.0.1"  # Replace with the target IP address
UDP_PORT = 2333       # Replace with the desired port
MESSAGE = ""         

# Create a UDP socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send the message (convert to bytes)
#sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

# Close the socket
#sock.close()


stored_lines = '' # Stores lines not yet written to a small file
history = '';
with open(HISTORYFILE) as history_file:
	history = history_file.read()

with open(LOGFILE) as big_file:
	stored_lines = big_file.read()
if "<eoh>" in stored_lines:
	records = stored_lines.split("<eoh>")[1]
else:
	records = stored_lines.split("<EOH>")[1]

idx = 0
split_eor = ''
if "<EOR>" in records:
	split_eor = "<EOR>"
else:
	split_eor = "<eor>"
for s in records.split(split_eor):
	if s not in history:
		idx = idx + 1
		if s != "":		
			MESSAGE = s.replace('\r'," ").replace('\n'," ") + "<EOR>"
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# Send the message (convert to bytes)
		sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
		print(MESSAGE)
		# Close the socket
		sock.close()
		with open(HISTORYFILE,'a') as history_file:
			history_file.write(s)
print("Number of records sent: {}".format(idx))