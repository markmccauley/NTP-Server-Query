"""
python2 code to query an NTP time server
Posted at https://stackoverflow.com/questions/12664295/ntp-client-in-python
"""

from contextlib import closing
from socket import socket, AF_INET, SOCK_DGRAM
import numpy as np
import sys
import struct
import time
import operator
import statistics
import turtle

NTP_PACKET_FORMAT = "!12I"
NTP_DELTA = 2208988800 # 1970-01-01 00:00:00
NTP_QUERY = '\x1b' + 47 * '\0' 

# designate list of NTP time server names
server_names = { "0.us.pool.ntp.org":0, "1.us.pool.ntp.org":0, "2.us.pool.ntp.org":0, "0.ubuntu.pool.ntp.org":0,
				"1.ubuntu.pool.ntp.org":0, "2.ubuntu.pool.ntp.org":0, "3.ubuntu.pool.ntp.org":0, "ntp.ubuntu.com":0,
				"time.apple.com":0, "time.windows.com":0, "time1.google.com":0, "time2.google.com":0,
				"time3.google.com":0, "time4.google.com":0, "ntp1.tamu.edu":0, "ntp2.tamu.edu":0,
				"ntp3.tamu.edu":0, "ops1.engr.tamu.edu":0, "ops2.engr.tamu.edu":0, "ops3.engr.tamu.edu":0,
				"ops4.engr.tamu.edu":0, "filer.cse.tamu.edu":0, "compute.cse.tamu.edu":0, "linux2.cse.tamu.edu":0,
				"dns1.cse.tamu.edu":0, "dns2.cse.tamu.edu":0, "dhcp1.cse.tamu.edu":0, "dhcp2.cse.tamu.edu":0 }

def ntp_time(host="", port=123):
	with closing(socket( AF_INET, SOCK_DGRAM)) as s:
		s.sendto(NTP_QUERY.encode(), (host, port))
		s.settimeout(2)
		try:
			msg, address = s.recvfrom(1024)
		except:
			return 0
		unpacked = struct.unpack(NTP_PACKET_FORMAT,
			msg[0:struct.calcsize(NTP_PACKET_FORMAT)])
		return unpacked[10] + float(unpacked[11]) / 2**32 - NTP_DELTA

def calculate_difference(): # get the differences of local time and server time store in dict.
	differences_list = [] # put differences in list to avoid 0 values accounting to mean
	discrepancy_list = [] # put discrepancies in a list for charting
	for key in server_names: #get each key from dictionary
		server_time = ntp_time(key)
		local_time = time.time()
		if server_time != 0: # check if server is reachable
			server_names[key] = local_time - server_time
			differences_list.append(server_names[key]) # build list of differences

	average_difference = statistics.mean(differences_list) # get mean of differences

	for key in server_names: # find discrepancy
		if server_names[key] !=0: # check if server is reachable
			server_names[key] = abs(server_names[key] - average_difference)
			discrepancy_list.append(server_names[key])

	return discrepancy_list

def drawBar(t, height):
	t.begin_fill()               # start filling shape
	t.left(90)
	t.forward(height*100)
	t.right(90)
	t.forward(5)
	t.write("%.3f" % height)
	t.forward(55)
	t.right(90)
	t.forward(height*100)
	t.left(90)
	t.end_fill()                 # stop filling shape

def create_chart():
	maxheight = max(chart_data)*100
	numbars = len(chart_data)
	border = 10

	wn = turtle.Screen()             # Set up the window and its attributes
	wn.setworldcoordinates(0-border, 0-border, 60*numbars+border, maxheight+border)
	wn.bgcolor("white")
	wn.title("Discrepancies")

	drawer = turtle.Turtle()           # create drawer and set attributes
	drawer.pensize(3)

	for data in chart_data: # if discrepancy is less than 1 use green
		if data < 1:
			drawer.fillcolor("green")
		else: 							# otherwise color red
			drawer.fillcolor("red")
		drawBar(drawer, data)
		
	wn.exitonclick()


if __name__ == "__main__":
	print("Querying servers...")
	chart_data = calculate_difference()
	max_server = max(server_names, key = server_names.get)
	max_server_value = server_names[max_server]
	print("Greatest discrepancy: " + max_server + " - " + str(max_server_value) + " sec")
	create_chart()
