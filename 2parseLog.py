import glob
import os
import subprocess
import re

list_of_files_server = glob.glob('/home/bayes/Repositories/pruebas/logs/server*') # * means all if need specific format then *.csv
list_of_files_client = glob.glob('/home/bayes/Repositories/pruebas/logs/client*')
latest_file_server = max(list_of_files_server, key=os.path.getctime)
latest_file_client = max(list_of_files_client, key=os.path.getctime)

session = subprocess.check_output('grep -m1 "Session*" '+latest_file_client+' | cut -d " " -f4 | cut -d ";" -f1', shell=True).rstrip('\n')

def  fileExists():
	fn = "infoSession/infosession"+session+".log"
	try:
	    file = open(fn, 'a')
	except IOError:
	    file = open(fn, 'w')
	return file   

file = fileExists()
file.write("Session=" + session + ", ")

with open(latest_file_client, 'r') as filehandle:  
	# Pillamos la primera linea que contiene la IP del cliente
	line = filehandle.readline()
	ip = line.split("=  ")
	file.write("IPClient=" + ip[1].rstrip('\n') + ", ")

	for line in filehandle:
		if "Content-Base:" in line :
			ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)
			file.write("IPServer=" + ip[0] + ", ")
			#file.write(date)
		#if "Date" in line:
			#date = "Quitar el dia de la semana" + line.split(": ")[1]
		if "Transport:" in line :
			if "client_port" and "server_port" in line :
				line = line.split(";")
				file.write(line[2] + " " + line [3] + ", ")

		# Audio info
		if "samplerate:" in line :
			file.write ("AUDIO: ")
			array=(line.split("] ")[2]).split("g: ")[1].split(" ")
			array[3] = array[3].rstrip('\n')
			for i in array :
				if ":" not in i  :
					file.write("acodec=")
				i=i.replace(':','=')
				file.write(i)
				file.write(", ")
		
#Server side
file.write ("VIDEO: ")
with open(latest_file_server, 'r') as filehandle:  
	fps = "fps=NotApplicable" # Ponemos esto para tener esta variable, aunque el video no se reproduzca
	video2 = "vcodec=NotApplicable"
	for line in filehandle:
		if "source fps" in line:
			line= line.split(": ")[1].split(", ")
			fps = line[0]+", " + line[1]
		if "core stream output debug: usi" in line:
			video=line.split("{")[1].split(',')
			video2 = video[0]+", "+video[1]

	file.write (fps + ", " + video2 + "\n")
# NOTA: El ultimo parametro que se anada al fichero del este log, debe tener un salto de linea. Si no, el filebeat no lo coge.
