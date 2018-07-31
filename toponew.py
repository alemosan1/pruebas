# coding: utf-8
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.term import cleanUpScreens, makeTerm
from mininet.node import RemoteController, Controller
import os


class SingleSwitchTopo(Topo):
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
    h1 = net.get('h1') 
    h2 = net.get('h2')


	
    #cmd = 'su bayesiansdn -c "vlc /home/bayesiansdn/vlcprueba/small.mp4"'
    #el host no tiene conexión, la prueba de youtube no funciona
    #cmd = 'su bayesiansdn -c "vlc https://youtu.be/AsGUJpCCkVw"'
    # TO DO : Hacemos que h1 mande el video small y que h2 lo reciba con xterm.
    cmd1 = "su bayesiansdn ;"
    cmd1 = "vlc-wrapper -vvv /home/bayesiansdn/bayesiansdn-demos/network-simulator/mininet/net/samples/SampleVideo_1280x720_30mb.mkv --sout '#duplicate{dst=rtp{dst=10.0.0.2,port=5004,mux=ts},dst=display}'"
    
    #client side
    cmd2 = "su bayesiansdn ;"
    cmd2 = "vlc-wrapper rtp://10.0.0.2:5004"
    
    miterm = makeTerm(h2, title='VLC Client', term='xterm', display=None, cmd=cmd2)
    miterm = makeTerm(h1, title='VLC Server', term='xterm', display=None, cmd=cmd1)
    
    CLI(net)
    

if __name__ == '__main__':
    setLogLevel('info')
    simpleTest()
