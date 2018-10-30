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
	
	#Var to save info
	ports= set()
	identification = set()
	contador = 0
	read = False



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
				port = line[2] + " " + line [3]
				ports.add(port)

		if " s=" in line :
			line = line.split("=")
			unique_id = line[1].rstrip('\r\n')

		if 'audio/' in line:
			contador = 5
			read="_audio"

		if 'video/' in line:
			contador = 5
			read="_video"

		if (read == "_audio" or read == "_video") and contador > -1:
			contador-=contador
			if 'port' in line:
				line = line.split(";")
				port = line[2]
				port = port[:port.find('=')]+read+port[port.find('='):].rstrip('\r\n')
				identification.add(port)
	

file.write(unique_id + " " + "session=" + session + " " + ip_client + " " + ip_server + " " )
for i in ports :
	for j in identification :		
		if  j.split('=')[1] in i.split('=')[1] :
			change ="_port_"+j.split('_')[2].split('=')[0]
			file.write(i.replace('_port',change)+" ")
file.write("\n")