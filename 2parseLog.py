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
	fn = "infoSession/infosession"+session+".txt"
	try:
	    file = open(fn, 'a')
	except IOError:
	    file = open(fn, 'w')
	return file   

file = fileExists()
file.write(session + ", ")

#variables to get only specific information.
read = False
# counter and numberlines I want to read.
counter = 0
numberLines=30

with open(latest_file_client, 'r') as filehandle:  
	# Pillamos la primera linea que contiene la IP del cliente
	line = filehandle.readline()
	ip = line.split("=  ")
	file.write(ip[1].rstrip('\n') + ", ")

	for line in filehandle:

		if "DESCRIBE response" in line :
			read = True
    	
		# if to get only the number of lines specified in the variable after the DESCRIBE response
		if read :
			counter += 1
			if "Content-Base:" in line :
				ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)
				file.write(ip[0] + ", ")
				#file.write(date)
    		#if to get the date of the streaming session
			if "Date" in line:
				date = "Quitar el dia de la semana" + line.split(": ")[1]
			if "=" in line:
				line = line.split("] ")[1]
				#file.write(line)

			if counter > numberLines :
				read = False

    	#To get audio codification information
		if "samplerate:" in line :
			array=(line.split("] ")[2]).split("g:")[1].split(" ")
			#file.write (20*'-'+"codificacion del audio"+20*'-'+"\r\n")
			for i in array :
				i=i.replace(':','=')
				# file.write(i)
				#file.write('\n')
    			#print i
    		#Close the client log file to start parsing the server side
    		
#file.write (20*'-'+"codificacion del video"+20*'-'+"\r\n")
with open(latest_file_server, 'r') as filehandle:  
    for line in filehandle:
		if "source fps " in line:
			line= line.split(": ")[1].split(", ")
			#file.write(line[0]+'\r\n')
			#file.write(line[1])
		if "core stream output debug: usi" in line:
			line=line.split("{")[1].split(',')
			#file.write(line[0]+'\n'+line[1]+'\n')
 

