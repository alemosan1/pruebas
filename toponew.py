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


class SingleSwitchTopo(Topo):

    def build(self, n=2):
	    switch = self.addSwitch('s1')

	    for h in range(n):
		    host = self.addHost('h%s' % (h + 1))
  		    self.addLink(host, switch)
def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def renameLog():
    os.chdir("logs")
    for filename in os.listdir("."):
        if (filename.endswith(".old") != True):
            os.rename(filename,filename+".old")
    os.chdir("..")
def simpleTest():
    #Añadimos controlador odl, ip por defecto
    controller = RemoteController('c1', ip='127.0.0.1', port=6633)
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo=topo, controller=controller)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Let's do a pingAll..."
    net.pingAll()
    src = net.get('h1') 
    dst = net.get('h2')
    
    #Server side
    cmdServer = "su bayesiansdn ;"
    cmdServer = "vlc-wrapper --extraintf=http:logger --verbose=2 --file-logging --logfile=logs/serverVLC-log.txt -vvv sampleVideo.mkv --sout '#duplicate{dst=rtp{dst=10.0.0.2,port=5004,mux=ts},dst=display} --sout-keep --loop'"
    #Client side
    cmdClient = "su bayesiansdn ;"
    cmdClient = "vlc-wrapper --extraintf=http:logger --verbose=2 --file-logging --logfile=logs/clientVLC-log.txt rtp://10.0.0.2:5004"
    
    termDst = makeTerm(dst, title='VLC Client', term='xterm', display=None, cmd=cmdClient)
    termSrc = makeTerm(src, title='VLC Server', term='xterm', display=None, cmd=cmdServer)
    
    time.sleep(5)
    #vlc-wrapper --extraintf=http:logger --verbose=2 --file-logging --logfile=vlc-log.txt
    logfile = open("logs/clientVLC-log.txt","r")
    loglines = follow(logfile)
    for line in loglines:
        print line,
    CLI(net)
    

if __name__ == '__main__':
    setLogLevel('info')
    #Vamos a renombrar los logs para cada vez que se ejecueten se guarden los previos.
    renameLog()
    simpleTest()
