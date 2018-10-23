#usr
#coding: utf-8
#Parseo "manual" de logs para coger información de la sesión de streaming


import glob
import os
import subprocess
import re
import json
from pprint import pprint




list_of_files_server = glob.glob('/home/bayes/Repositories/pruebas/logs/server*') # * means all if need specific format then *.csv
latest_file_server = max(list_of_files_server, key=os.path.getctime)
id_logFile = re.findall(r'\d+', latest_file_server)[0]
path=""

def  fileExists():
	fn = "infoSession/infosessionServer"+id_logFile+".log"
	try:
	    file = open(fn, 'a')
	except IOError:
	    file = open(fn, 'w')
	return file   

file = fileExists()

#### SERVER SIDE ####
with open(latest_file_server, 'r') as filehandle:  
	fps_src = fps_dst = vcodec = scale = "NotApplicable" # Generamos estas variables aunque el video no se reproduzca
	demux_module=""
	#aux var to read transcode information if is read
	disabler=False
	for line in filehandle:
		# Obtain the path to the file
		if "location='/home/bayes/Repositories/" in line:
			path = line.split("file='")[-1].rstrip("'\n")
			#path=line.split("\'file\'")[-1].split("path")[-1].split("location=")[1].split(" f")[0]
			#print path
		if "source fps" in line:
			line = line.split(": ")[1].split(", ")
			fps_src = line[0].split(' ')[2]
			fps_dst = line[1].split(' ')[1].rstrip('\n')

		if "sout chain=`transcode" in line :
			disabler=True;
			line = line.split("{")[1].split("}")[0].split(",")

			for i in line:
				if "=" in i:
					i= i.split('=')
					file.write(i[0]+ "=" + i[1]+" ,")
		#Error
		if "looking for demux module matching \"" in line:
			#Always the demux is in the second line so this way is correct
			demux_module = line.split("\"")[1]

		#I access to this part if information about transcode has not been sent
		if not disabler:
			if  demux_module+" demux debug: |" in line :
				line=line.split("|")[-1].split("+")[-1].rstrip('\n')
				
				if "=" in line:
					line = line.split("=")
					file.write(line [0] +"="+ line [1]+" ,")

#Not applicable in this video VIDEO: fps_src=NotApplicable, fps_dst=NotApplicable, vcodec=NotApplicable, scale=NotApplicable

cmdVideoInf = " ffprobe -v quiet -print_format json -show_format -show_streams "+path+"  > "+path+".json"
data=""
audio=""
video=""
otros=""
os.system(cmdVideoInf)
with open(path+".json") as f:
    data = json.load(f)
    mostrar = data["streams"]
    #Way of identifying different streams (audio,video,subtitles) in the video 
    for i in mostrar:
    	if i["codec_type"]=="video":
    		video=i
    	elif i["codec_type"]=="audio":
    		audio=i
    	else:
    		otros=i
    		
if fps_src =="NotApplicable":
	fps_src=video["avg_frame_rate"]
if fps_dst =="NotApplicable":
	fps_dst=video["avg_frame_rate"]
if vcodec =="NotApplicable":
	vcodec=video["codec_name"]
if scale =="NotApplicable":
	scale=str(video["coded_width"])+":"+str(video["coded_height"])
file.write ("VIDEO: " + "fps_src="+fps_src+ ", fps_dst="+fps_dst+ ", vcodec="+vcodec+ ", scale="+scale+ "\n")

# NOTA: El ultimo parametro que se anada al fichero del este log, debe tener un salto de linea. Si no, el filebeat no lo coge.
