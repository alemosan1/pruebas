import subprocess
import re

output = subprocess.check_output("mediainfo sampleVideo.mkv", shell=True)

result = {}
dic = {}
print 'hola'
for row in output.split('\n'):
	#if 'fps' in row:
	# divide string and remove all spaces
	key = row.partition(':')[0]
	key = key.replace(" ","")
	value=row.partition(':')[2]
	value = value.replace(" ","")
	dic[key]=value

	#to get any number (float,double) in a string
	#arr = [float(s) for s in re.findall(r'-?\d+\.?\d*', str)]

	#only works with int numbers
	#[int(s) for s in str.split() if s.isdigit()]
for release in dic :
	print release+":"+dic[release]
	
    
     



