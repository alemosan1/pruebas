import glob
import os
import subprocess
import re
import json
from pprint import pprint

list_of_files_server = glob.glob('/home/bayes/Repositories/pruebas/logs/server*') # * means all if need specific format then *.csv
latest_file_server = max(list_of_files_server, key=os.path.getctime)
id_logFile = re.findall(r'\d+', latest_file_server)[0]
#Eliminables
path=""
pathURL=""


###FUNCION PARA VER SI EXISTE EL FICHERO
def  fileExists():
	fn = "infoSession/infosessionServer"+id_logFile+".log"
	try:
	    file = open(fn, 'a')
	except IOError:
	    file = open(fn, 'w')
	return file   

file = fileExists()


###FUNCION PARA EXTRAER INFORMACION MULTIMEDIA"
def getInformation(path,command) :
	if command =='video':
		cmdVideoInf = " ffprobe -v quiet -print_format json -show_format -show_streams "+path
	elif command=="streaming":
		cmdVideoInf = "ffprobe -v quiet -print_format json -show_format -show_streams "+path

	data=""
	audio=""
	video=""
	otros=""
	data=subprocess.check_output(cmdVideoInf,shell=True)
	datajson=json.loads(data)

	mostrar = datajson["streams"]
	    #Way of identifying different streams (audio,video,subtitles) in the video 
	for i in mostrar:
		if i["codec_type"]=="video":
			video=i
	   	elif i["codec_type"]=="audio":
	   		audio=i
    	else:
      		otros=i
	#Obtain all data from video
	file.write("\nVIDEO_ORIGINAL_"+command+",")
	for i in video:
	  	if not type(video[i]) is dict :
	  		file.write( i +"="+str(video[i])+",")
	  	# If the data is a dictionary, I will go through to obtain values
	  	else :
	  		for j in video[i] :
	 			file.write( j +"="+str(video[i][j])+",")

	  	  	#Obtain all data from audio
	file.write("\nAUDIO_ORIGINAL_"+command+",")
	for i in audio:
	  	if not type(audio[i]) is dict :
	  		file.write( i +"="+str(audio[i])+",")
	  	# If the data is a dictionary, I will go through to obtain values
	  	else :
	  		for j in audio[i] :
	  			file.write( j +"="+str(audio[i][j])+",")
	file.write ("\n")	
	#We can obtain antoher information such as data,menu,and so on"
# NOTA: El ultimo parametro que se anada al fichero del este log, debe tener un salto de linea. Si no, el filebeat no lo coge.


#### SERVER SIDE ####
with open(latest_file_server, 'r') as filehandle:  

	for line in filehandle:
		# Obtain the path to the file
		if "location='/home/bayes/Repositories/" in line:
			path = line.split("file='")[-1].rstrip("'\n")
		# Obtain the URL path
		if "chain=" in line:
			pathURL=line.split("sdp=")[1].split("}")[0]
		if "sout chain=`transcode" in line :
			line = line.split("{")[1].split("}")[0].split(",")
			for i in line:
				if "=" in i:
					i= i.split('=')
					file.write(i[0]+ "=" + i[1]+",")
		if "IP =" in line :
			IP = line.split("IP =  ")[1].rstrip("\n")

#CODIGO DE EJECUCION

#Manipulate string to put IP
cuenta =len( pathURL.split("/:")[0])
pathURL=pathURL[:cuenta+1]+IP+pathURL[cuenta+1:]



file.write("Fprobe en el VIDEO \n")
getInformation(path,"video")

file.write("Fprobe en el  STREAMING \n")
getInformation(pathURL,"streaming")

