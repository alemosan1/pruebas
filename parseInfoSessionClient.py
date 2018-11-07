#usr
#coding: utf-8
#Parseo "manual" de logs para coger información de la sesión de streaming
import glob
import os
import subprocess
import re
import sys


latest_file_client = sys.argv[1]
id_logFile = re.findall(r'\d+', latest_file_client)[0]
unique_id_file = latest_file_client.split("_")[1]

def  fileExists():
	fn = "infoSession/infosessionClient"+id_logFile+"_"+unique_id_file+".log"
	try:
	    file = open(fn, 'a')
	except IOError:
	    file = open(fn, 'w')
	return file   

file = fileExists()
session = subprocess.check_output('grep -m1 "Session*" '+latest_file_client+' | cut -d " " -f4 | cut -d ";" -f1', shell=True).rstrip('\n')
path = ""

with open(latest_file_client, 'r') as filehandle:  
	#Var to save info
	get_ports = set()
	identification = set()
	contador = 0
	read = ports = ""
	
	# IP_CLIENT
	line = filehandle.readline()
	ip = line.split("=  ")
	ip_client = "ip_client=" + ip[1].rstrip('\n')

	for line in filehandle:
		if "Content-Base:" in line : # IP_SERVER
			ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)
			ip_server = "ip_server=" + ip[0]

		if "Transport:" and "client_port" and "server_port" in line : # PORTS
			line = line.split(";")
			port = line[2] + " " + line [3]
			get_ports.add(port)


		if " s=" in line :
			line = line.split("=")
			unique_id = line[1].rstrip('\r\n')

		if 'audio/' in line:
			contador = 5
			read = "_audio"

		if 'video/' in line:
			contador = 5
			read = "_video"

		if (read == "_audio" or read == "_video") and contador > 0:
			contador -= contador
			print contador
			if 'port' in line:
			
				line = line.split(";")
				print line
				port = line[2]
				port = port[:port.find('=')]+ read + port[port.find('='):].rstrip('\r\n')
				identification.add(port)

for i in get_ports :
	for j in identification :		
		if  j.split('=')[1] in i.split('=')[1] :
			change ="_port_" + j.split('_')[2].split('=')[0]
			ports += i.replace('_port', change) + " "

file.write(unique_id + " " + "session=" + session + " " + ip_client + " " + ip_server + " " + ports + "\n")