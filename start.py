# usr
# coding: utf-8
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.term import cleanUpScreens, makeTerm
from mininet.node import RemoteController, Controller
import os
import subprocess
import glob
import time
import datetime
import ConfigParser
import uuid

class SingleSwitchTopo(Topo):
    def build(self, n=2):
    	    switch = self.addSwitch('s1')

    	    for h in range(n):
    		    host = self.addHost('h%s' % (h + 1))
      		    self.addLink(host, switch)

# Reads the full file line per line
def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def containNumber(inputString):
    return any(char.isdigit() for char in inputString)

# Renames the log file so we have a new one each time
def renameLog():
    os.chdir("logs")
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H:%M:%S')
    for filename in os.listdir("."):
        if (containNumber(filename) != True):
            os.rename(filename,filename[:-4]+st+".txt")
    os.chdir("..")

# Starts simulation    
def simpleTest():
    #Añadimos controlador odl, ip por defecto
    #controller = RemoteController('c1', ip='127.0.0.1', port=6633)
    topo = SingleSwitchTopo(n=4)
    #net = Mininet(topo=topo, controller=controller)
    net = Mininet(topo=topo) # Quito el controller para no tener que estar iniciando ODL
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Let's do a pingAll..."
    net.pingAll()
    src = net.get('h1') 
    dst = net.get('h2')
	
	# Check the file codecsInfo.txt for more info about codecs
	# CONTAINER CODEC FORMAT
    muxerCodecVlan = {1:'mpeg1',2:'ts',3:'ps',4:'mp4',5:'avi',6:'asf',7:'dummy',8:'ogg',9:''}

    # VIDEO CODEC FORMAT
    videoCodecVlan = {1:'mp1v',2:'mp2v',3:'mp4v',4:'SVQ1',5:'SVQ3',6:'DVDv',
    7:'WMV1',8:'WMV2',9:'WMV3',10:'DVSD',11:'MJPG',12:'H263',13:'h264',14:'theo',
    15:'IV20',16:'IV40',17:'RV10',18:'cvid',19:'VP31',20:'FLV1',21:'CYUV',22:'HFYU',
    23:'MSVC',24:'MRLE',25:'AASC',26:'FLIC',27:'QPEG',28:'VP8'}

    # AUDIO CODEC FORMAT
    audioCodecVlan = {1:'mpga',2:'mp3',3:'mp4a',4:'a52',5:'vorb',6:'spx',7:'flac'}

	# VIDEOS AVAILABLE
    selectVideoURL = {1:'videos/sampleVideo.mkv',2:'videos/small.mp4',3:'videos/exampleAVI.avi'}
   
	# Configuration parameters
    codecVideoUsed = videoCodecVlan[3]
    codecAudioUsed = audioCodecVlan[1]
    codecMuxerUsed = muxerCodecVlan[2]
    videoURL	   = selectVideoURL[1]
    enableMuxRTP   = "--sout-rtp-rtcp-mux"
    CPUlimit 	   = ""
    unique_id      = str(uuid.uuid4()) # Generation of a unique id(UUID) to identify sessions

    # SERVER SIDE
    cmdServer = ""
    if err_type == '0' : # No errors
        cmdServer = "su bayes -c \"cvlc -vvv "+videoURL+" --sout='#rtp{sdp=rtsp://:5004/}' \
        --sout-keep --sout-rtp-name="+unique_id+" --loop 2>&1 | \
        ./timestamp.sh server "+err_type+" "+unique_id+"\""
    elif err_type == '1' : # Low fps rate and binary bit rate (video)
        cmdServer = "su bayes -c \"cvlc -vvv "+videoURL+" \
		--sout='#transcode{vcodec="+codecVideoUsed+",vb=60,vfilter=freeze,fps=5,scale=Automático,samplerate=48000, acodec=audio}\
        :rtp{sdp=rtsp://:5004/}' --sout-keep --sout-rtp-name="+unique_id+" --loop 2>&1 | \
        ./timestamp.sh server "+err_type+" "+unique_id+"\""
    elif err_type == '2' : #  Low sample rate (Audio)
        cmdServer = "su bayes -c \"cvlc -vvv "+videoURL+" \
        --sout='#transcode{vcodec="+codecVideoUsed+",scale=Auto,acodec=spx,ab=128,channels=2,samplerate=8000}\
        :rtp{sdp=rtsp://:5004/}' --sout-keep --sout-rtp-name="+unique_id+ " --loop 2>&1 | \
         ./timestamp.sh server "+err_type+" "+unique_id+"\""
    elif err_type == '3' : # TODO: incompatible mux format 
        cmdServer = "su bayes -c \"cvlc -vvv "+videoURL+" \
         --sout='#transcode{vcodec=avi,scale=Automático,acodec=mpga,ab=128,channels=2,samplerate=44100}\
         :rtp{mux="+codecMuxerUsed+",sdp=rtsp://:5004/}' --sout-keep --sout-rtp-name="+unique_id+" --loop  2>&1 \
         | ./timestamp.sh server "+err_type+" "+unique_id+"\""
    elif err_type == '4' : #MP4 example
        cmdServer = "su bayes -c \"cvlc -vvv "+videoURL+" \
        --sout='#transcode{vcodec="+codecVideoUsed+",vb=2000,scale=Automático,acodec=vorb,ab=128,channels=2,samplerate=44100}\
        :rtp{mux=mpeg1,sdp=rtsp://:5004/}' --sout-keep --sout-rtp-name="+unique_id+" --loop 2>&1 \
        | ./timestamp.sh server "+err_type+" "+unique_id+"\""
    elif err_type == '5' : #Limitation of CPU limit
        cmdServer = "su bayes -c \"cvlc -vvv "+videoURL+" \
        --sout='#rtp{sdp=rtsp://:5004/}' --sout-keep --sout-rtp-name="+unique_id+" --loop 2>&1\
         | ./timestamp.sh server "+err_type+" "+unique_id+"\""
        CPUlimit = "& cpulimit -p `expr $! - 1` -l 15"
    
	# CLIENT SIDE - TODO: tenemos que poner que la IP se saque programaticamente
    cmdClient = "su bayes -c \" vlc-wrapper -vvv -R --network-caching 200 rtsp://10.0.0.1:5004/ 2>&1 | \
     ./timestamp.sh cliente "+err_type+CPUlimit+" "+unique_id+"\""
    
	# XTERMS
    termSrc = makeTerm(src, title='VLC Server', term='xterm', display=None, cmd=cmdServer)
    time.sleep(3)
    for i in range(int(cli_nr)): #TODO: Esto funciona? Los creamos todos con la misma IP de cliente?
        termDst = makeTerm(dst, title='VLC Client '+str((i+1)), term='xterm', display=None, cmd=cmdClient)
        time.sleep(3)
	
	# TODO: Check
    #Ahora vamos a poner un terminal para sacar informacióm
    cmdInfo = "ifstat 10.0.0.2 > codeccompresion/"+codecVideoUsed+codecMuxerUsed+".info"
    termGetInfo = makeTerm(dst, title= "Monitoring traffic", term='xterm', display=None, cmd=cmdInfo)

    # Cogemos la info del video desde el servidor
    # Lo hacemos aquí por problemas con el acceso a esa IP
    cmdParseInfoServer = "su bayes -c \"python parseInfoSessionServer.py\""
    termParseInfo = makeTerm(src, title= "Parsing Server Info...", term='xterm', display=None, cmd=cmdParseInfoServer)

	# TODO: Para que es esto que esta comentado?
    # logfile = open("logs/clientVLC-log.txt","r") 
    # loglines = follow(logfile)
    # for line in loglines:
    #     st = datetime.datetime.now()
    #     print "["+str(st)+"]"+line,

    CLI(net)
    cmdExit = "sudo kill $(ps aux | grep 'vlc' | grep -v grep | awk '{print $2}'); \
                kill $(ps aux | grep 'ifstat' | grep -v grep | awk '{print $2}')" # En esta segunda linea es donde se produce el error
    os.system(cmdExit)
    net.stop()

if __name__ == '__main__':
    # setLogLevel('info')
    configerror = ConfigParser.ConfigParser()
    configerror.read(['./config_vlc.py'])
    err_type = configerror.get('errors','Type')
    cli_nr = configerror.get('clients','ClientsNumber')
    os.system('systemd-machine-id-setup')

    #Vamos a renombrar los logs para cada vez que se ejecueten se guarden los previos.
    renameLog()
    simpleTest()
