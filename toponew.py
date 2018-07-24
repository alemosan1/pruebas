# coding: utf-8
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.term import cleanUpScreens, makeTerm


class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=2):
        switch = self.addSwitch('s1')
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)
            #Añadir el controlador opendaylight (así probamos a ver el tráfico)

def simpleTest():
    "Create and test a simple network"
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo)
    net.start()
    #print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    ale = net.get('h1')
    cmd = 'su bayesiansdn -c "vlc /home/bayesiansdn/vlcprueba/small.mp4"' #Cambiar por url de youtube, por ejemplo
    miterm = makeTerm(ale, title='VLC PRUEBA', term='xterm', display=None, cmd=cmd)
    #CLI(net)
    

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
