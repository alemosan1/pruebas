# coding: utf-8
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.term import cleanUpScreens, makeTerm
from mininet.node import RemoteController, Controller
import os


class SingleSwitchTopo(Topo):exit

    def build(self, n=2):
        switch = self.addSwitch('s1')
	
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)

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
    cmdServer = "vlc-wrapper -vvv sampleVideo.mkv --sout '#duplicate{dst=rtp{dst=10.0.0.2,port=5004,mux=ts},dst=display}'"
    #Client side
    cmdClient = "su bayesiansdn ;"
    cmdClient = "vlc-wrapper rtp://10.0.0.2:5004"
    
    termDst = makeTerm(dst, title='VLC Client', term='xterm', display=None, cmd=cmdClient)
    termSrc = makeTerm(src, title='VLC Server', term='xterm', display=None, cmd=cmdServer)
    
    CLI(net)
    

if __name__ == '__main__':
    setLogLevel('info')
    simpleTest()
