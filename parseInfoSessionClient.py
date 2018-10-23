#usr
#coding: utf-8
#Parseo "manual" de logs para coger información de la sesión de streaming


import glob
import os
import subprocess
import re


list_of_files_client = glob.glob('/home/bayes/Repositories/pruebas/logs/client*')
latest_file_client = max(list_of_files_client, key=os.path.getctime)
id_logFile = re.findall(r'\d+', latest_file_client)[0]
path=""

def  fileExists():
	fn = "infoSession/infosessionClient"+id_logFile+".log"
	try:
	    file = open(fn, 'a')
	except IOError:
	    file = open(fn, 'w')
	return file   

file = fileExists()
session = subprocess.check_output('grep -m1 "Session*" '+latest_file_client+' | cut -d " " -f4 | cut -d ";" -f1', shell=True).rstrip('\n')



with open(latest_file_client, 'r') as filehandle:  
	channels = samplerate = bitrate = acodec = "NotApplicable" # Generamos estas variables aunque el audio no se reproduzca
	
	# IP CLIENT
	line = filehandle.readline()
	ip = line.split("=  ")
	ip_client = "IPClient=" + ip[1].rstrip('\n')

	for line in filehandle:
		if "Content-Base:" in line : # IP SERVER
			ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)
			ip_server = "IPServer=" + ip[0]
			#file.write(date)
		#if "Date" in line:
			#date = "Quitar el dia de la semana" + line.split(": ")[1]
		if "Transport:" in line : # PORTS
			if "client_port" and "server_port" in line :
				line = line.split(";")
				ports = line[2] + ", " + line [3]

		# AUDIO INFO
		if "samplerate:" in line :
			audioInfo = (line.split("] ")[2]).split("g: ")[1].split(" ")
			audioInfo[3] = audioInfo[3].rstrip('\n')
			aux = 1
			for i in audioInfo :
				if ":" in i :
					audioInfo [aux] = i.split(":")[1]
					aux += 1
			acodec = audioInfo[0]
			channels = audioInfo[1]
			samplerate = audioInfo[2]
			bitrate = audioInfo[3]
file.write("Session=" + session + ", " + ip_client + ", " + ip_server + ", " + ports + ", ")
file.write("AUDIO: " + "acodec="+acodec+ ", channels="+channels+ ", samplerate="+samplerate+ ", bitrate="+bitrate+ ", ")