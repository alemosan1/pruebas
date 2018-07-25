# coding: utf-8
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.term import cleanUpScreens, makeTerm
from mininet.node import RemoteController, Controller


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
    ale = net.get('h1')
    #cmd = 'su bayesiansdn -c "vlc /home/bayesiansdn/vlcprueba/small.mp4"'
    #el host no tiene conexión, la prueba de youtube no funciona
    #cmd = 'su bayesiansdn -c "vlc https://youtu.be/AsGUJpCCkVw"'
    # TO DO : Hacemos que h1 mande el video small y que h2 lo reciba con xterm.
    cmd = 'su bayesiansdn'
    miterm = makeTerm(ale, title='VLC PRUEBA', term='xterm', display=None, cmd=cmd)
    CLI(net)
    

if __name__ == '__main__':
    setLogLevel('info')
    simpleTest()
