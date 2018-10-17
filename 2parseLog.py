import glob
import os
import subprocess
import re

list_of_files_server = glob.glob('/home/bayes/Repositories/pruebas/logs/server*') # * means all if need specific format then *.csv
list_of_files_client = glob.glob('/home/bayes/Repositories/pruebas/logs/client*')
latest_file_server = max(list_of_files_server, key=os.path.getctime)
latest_file_client = max(list_of_files_client, key=os.path.getctime)
id_logFile = re.findall(r'\d+', latest_file_client)[0]

def  fileExists():
	fn = "infoSession/infosession"+id_logFile+".log"
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

#### SERVER SIDE ####
with open(latest_file_server, 'r') as filehandle:  
	fps_src = fps_dst = vcodec = scale = "NotApplicable" # Generamos estas variables aunque el video no se reproduzca
	for line in filehandle:
		if "source fps" in line:
			print line 
			line = line.split(": ")[1].split(", ")
			fps_src = line[0].split(' ')[2]
			fps_dst = line[1].split(' ')[1].rstrip('\n')

			# line= line.split(": ")[1].split(", ")
			# file.write(line[0]+'\r\n')
			# file.write(line[1])
		if "core stream output debug: usi" in line:
			videoParams=line.split("{")[1].split(',')
			vcodec = videoParams[0].split("=")[1]
			scale = videoParams[1].split("=")[1]

file.write ("VIDEO: " + "fps_src="+fps_src+ ", fps_dst="+fps_dst+ ", vcodec="+vcodec+ ", scale="+scale+ "\n")

# NOTA: El ultimo parametro que se anada al fichero del este log, debe tener un salto de linea. Si no, el filebeat no lo coge.
