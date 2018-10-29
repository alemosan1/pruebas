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

# Hemos observado que si le metemos transcodificacion de audio 
# mpeg_audio decoder va a tener la siguiente linea
# TODO: ¿QUE LINEA ???

with open(latest_file_client, 'r') as filehandle:  
	channels = samplerate = bitrate = acodec = "NotApplicable" # Generamos estas variables aunque el audio no se reproduzca | TODO: Al final no metemos nada de esto
	
	# IP CLIENT
	line = filehandle.readline()
	ip = line.split("=  ")
	ip_client = "ip_client=" + ip[1].rstrip('\n')

	for line in filehandle:
		if "Content-Base:" in line : # IP SERVER
			ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)
			ip_server = "ip_server=" + ip[0]

		if "Transport:" in line : # PORTS
			if "client_port" and "server_port" in line :
				line = line.split(";")
				ports = line[2] + " " + line [3]

		if " s=" in line :
			line = line.split("=")
			unique_id = line[1].rstrip('\r\n')

file.write(unique_id + " " + "session=" + session + " " + ip_client + " " + ip_server + " " + ports + "\n")