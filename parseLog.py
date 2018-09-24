import glob
import os
import subprocess
import re

def  fileExists():
	fn = "infosession.txt"
	try:
	    file = open(fn, 'a')
	    #Create a line to separate the dissimilar sessions
	    file.write(100*"-"+'\r\n')
	except IOError:
	    file = open(fn, 'w')
	return file   


list_of_files_server = glob.glob('/home/bayes/Repositories/pruebas/logs/server*') # * means all if need specific format then *.csv
list_of_files_client = glob.glob('/home/bayes/Repositories/pruebas/logs/client*')
latest_file_server = max(list_of_files_server, key=os.path.getctime)
latest_file_client = max(list_of_files_client, key=os.path.getctime)

print latest_file_client
print latest_file_server

# Open the file that contains all information about sessions.
file = fileExists()
session=subprocess.check_output('grep -m1 "Session*" '+latest_file_client+' | cut -d " " -f4 | cut -d ";" -f1', shell=True)
file.write("Session = "+str(session))

#variables to get only specific information.
read = False
# counter and numberlines I want to read.
counter = 0
numberLines=30

with open(latest_file_client, 'r') as filehandle:  
    for line in filehandle:
		if "DESCRIBE response" in line :
			read = True
    	
		# if to get only the number of lines specified in the variable after the DESCRIBE response
		if read :
			counter += 1
    		#if to get the date of the streaming session
    		if "Date" in line:
    			file.write("Date = "+ line.split(": ")[1])

    		if "=" in line:
    			line = line.split("] ")[1]
    			file.write(line)

    		if counter > numberLines :
    			read = False

    	#To get audio codification information
		if "samplerate:" in line :
			array=(line.split("] ")[2]).split("g:")[1].split(" ")
			file.write (20*'-'+"codificacion del audio"+20*'-'+"\r\n")
			for i in array :
				i=i.replace(':','=')
				file.write(i)
				file.write('\n')
    			print i
    		#Close the client log file to start parsing the server side
    		
file.write (20*'-'+"codificacion del video"+20*'-'+"\r\n")
existsIP=False
with open(latest_file_server, 'r') as filehandle:  
    for line in filehandle:
		# Linea para pillar la ip del source y del dest ---> core stream out debug: net: connecting to [10.0.0.2]:54809 from [10.0.0.1]:60072
		if "debug: net: connecting to" in line and "from" in line and not existsIP: 
			print line
			ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)
			file.write("IP Client = " + ip[0]+'\r\n'+ "IP Server = " + ip[1]+'\r\n')
			existsIP = True
		if "source fps " in line:
			line= line.split(": ")[1].split(", ")
			file.write(line[0]+'\r\n')
			file.write(line[1])
		if "core stream output debug: usi" in line:
			line=line.split("{")[1].split(',')
			file.write(line[0]+'\n'+line[1]+'\n')

