#usr
# coding: utf-8
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.term import cleanUpScreens, makeTerm
from mininet.node import RemoteController, Controller
import os
import time
import datetime
import ConfigParser


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
    
    
    #Server side
    cmdServer=""
    if type == '0' : # No errors
        cmdServer = "vlc-wrapper -vvv sampleVideo.mkv --sout='#transcode{vcodec=mp4v,scale=Auto,acodec=mpga,ab=128,channels=2,samplerate=22050}:rtp{sdp=rtsp://:5004/}' --sout-keep --loop 2>&1 | ./timestamp.sh server0"
    elif type == '1' : # Low fps rate and binary bit rate
        cmdServer = "vlc-wrapper -vvv sampleVideo.mkv --sout='#transcode{vcodec=h264,vb=60,vfilter=freeze,fps=5,scale=Automático,acodec=mpga,ab=256,channels=3,samplerate=22050,scodec=t140,soverlay}:rtp{sdp=rtsp://:5004/}' --sout-keep --loop 2>&1 | ./timestamp.sh server1"
    elif type == '2' : #TO DO: incompatible video format
        cmdServer = "vlc-wrapper -vvv sampleVideo.mkv --sout='#transcode{vcodec=theo,vb=2000,scale=Automático,acodec=vorb,ab=128,channels=2,samplerate=44100}:rtp{sdp=rtsp://:5004/}' --sout-keep --loop 2>&1 | ./timestamp.sh server2"
        print ""

    #Client side
    #TODO: tenemos que poner que la IP se saque programaticamente
    cmdClient = "vlc-wrapper -vvv -R --network-caching 200 rtsp://10.0.0.1:5004/ 2>&1 | ./timestamp.sh cliente"+type
    
    termSrc = makeTerm(src, title='VLC Server', term='xterm', display=None, cmd=cmdServer)
    time.sleep(5)
    termDst = makeTerm(dst, title='VLC Client', term='xterm', display=None, cmd=cmdClient)

    time.sleep(5)
    
    # logfile = open("logs/clientVLC-log.txt","r") 
    # loglines = follow(logfile)
    # for line in loglines:
    #     st = datetime.datetime.now()
    #     print "["+str(st)+"]"+line,

    CLI(net)
    cmdExit = "kill $(ps aux | grep 'vlc' | grep -v grep | awk '{print $2}')"
    os.system(cmdExit)
    net.stop()

    

if __name__ == '__main__':
    setLogLevel('info')
    configerror= ConfigParser.ConfigParser()
    configerror.read(['./config_vlc.py'])
    type =configerror.get('errors','Type')

    #Vamos a renombrar los logs para cada vez que se ejecueten se guarden los previos.
    renameLog()
    simpleTest()
