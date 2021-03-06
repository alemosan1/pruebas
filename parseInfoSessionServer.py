import glob
import sys
import os
import subprocess
import re
import json
from pprint import pprint

file_to_parse = sys.argv[1]
id_logFile = re.findall(r'\d+', file_to_parse)[0]
unique_id_file = file_to_parse.split("_")[1]

#Eliminables
pathOrigin = ""
pathStream = ""

# FUNCION PARA VER SI EXISTE EL FICHERO
def  fileExists():
	fn = "infoSession/infosessionServer"+id_logFile+"_"+unique_id_file+".log"
	try:
	    file = open(fn, 'a')
	except IOError:
	    file = open(fn, 'w')
	return file   

file = fileExists()

# FUNCION PARA EXTRAER INFORMACION MULTIMEDIA CON FFPROBE
def getInformation(path, command, unique_id) :
	cmdVideoInf = "ffprobe -v quiet -print_format json -show_format -show_streams " + path

	data = audio = video = otros = ""
	data = subprocess.check_output(cmdVideoInf,shell=True)
	datajson = json.loads(data)
	dataInJson = datajson["streams"]
 	
 	# Identify different types of streams (audio, video, subtitles) in the video 
	for i in dataInJson :
		if i["codec_type"] == "video" :
			video = i
	   	elif i["codec_type"] == "audio" :
	   		audio = i
	   	else :
	   		otros = i
	
	# Obtain all data from video
	file.write("VIDEO_" + command + "," + unique_id + ",")
	for i in video:
	  	if not type(video[i]) is dict :
	  		file.write( i +"="+str(video[i])+",")
	  	# If the data is a dictionary, I will go through to obtain values
	  	else :
	  		for j in video[i] :
	 			file.write( j +"="+str(video[i][j])+",")
	file.write ("\n")
	
	# Obtain all data from audio
	file.write("AUDIO_" + command + "," + unique_id + ",")
	for i in audio:
	  	if not type(audio[i]) is dict :
	  		file.write( i +"="+str(audio[i])+",")
	  	# If the data is a dictionary, I will go through to obtain values
	  	else :
	  		for j in audio[i] :
	  			file.write( j +"="+str(audio[i][j])+",")
	file.write ("\n")	
	# We can obtain another information such as data,menu,and so on"

# If logs have the transcode line
with open(file_to_parse, 'r') as filehandle:  
	transcodeLine = ""
	gotUniqueID = False
	for line in filehandle:
		if "IP =  " in line :
			IP = line.split("IP =  ")[1].rstrip("\n")
		# Obtain the path to the file
		if "location='/home/bayes/Repositories/" in line:
			pathOrigin = line.split("file='")[-1].rstrip("'\n")
		# Obtain the URL path
		if "chain=" in line:
			pathStream = line.split("sdp=")[1].split("}")[0]
			cuenta     = len(pathStream.split("/:")[0])
			pathStream = pathStream[:cuenta+1] + IP + pathStream[cuenta+1:]
		if "sout chain=`transcode" in line :
			transcodeLine = line.split("{")[1].split("}")[0]
		if " s=" in line and not gotUniqueID:
			line = line.split("=")
			unique_id = line[1].rstrip('\r\n')
			gotUniqueID = True
			if not transcodeLine == "" :
				transcodeLine = "TRANSCODE_LINE," + unique_id + "," + transcodeLine
				file.write(transcodeLine+"\n")
#CODIGO DE EJECUCION
getInformation(pathOrigin, "ORIGINAL", unique_id)
getInformation(pathStream, "STREAMING", unique_id)