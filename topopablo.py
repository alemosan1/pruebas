# coding: utf-8
import sys
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

    h3=net.get('h3')
    h2=net.get('h2')
    h1=net.get('h1')
    #cmd='su -c "vlc-wrapper bayesiansdn bayesiansdn-demos/network-simulator/mininet/net/samples/small.mp4"'
    #cmd= 'su -c "vlc-wrapper -vvv small.mp4 --sout \'#rtp{dst=10.0.0.2,port=5004}\''
    #cmd2='su -c "vlc-wrapper rtp://10.0.0.1:5004 &"'
    cmd3='wireshark'
    #h2.cmd('wireshark')
    #h1.cmd(cmd)
    #miTerm1=makeTerm(h1, term='xterm', cmd=cmd)
    #miTerm2=makeTerm(h2, term='xterm', cmd=cmd2)
    #CLI(net)
    #net.stop()

    print 'Executing command on h2'
    cmd2='vlc-wrapper rtp://@:5004 --sout "#transcode{vcodec=h264,acodec=mpga,ab=128,channels=2,samplerate=44100}:std{access=file,mux=mp4,dst=output.mp4}"' 

    """
    cmd2 = 'vlc rtsp://10.0.0.1:8554'
    # result2 = h2.cmd('sleep 5')
    """
    # time.sleep(5)

    print 'Executing command on h1'
    cmd1='vlc-wrapper -vvv drop.avi --sout "#transcode{vcodec=h264,acodec=mpga,ab=128,channels=2,samplerate=44100}:duplicate{dst=rtp{dst=10.0.0.2,port=5004,mux=ts}}"' 
    """
    cmd1='vlc -vvv small.mp4 \
    --sout=\'#transcode{vcodec=mp4v,scale=Auto,acodec=mpga,ab=128,channels=2,samplerate=22050}:rtp{sdp=rtsp://:8554}\' \
    --sout-keep '
    # result1 = h1.cmd('sleep 5')
    """
    # result1wo = h1.waitOutput()
    miTerm2=makeTerm(h2, term='xterm', cmd=cmd2)
    miTerm1=makeTerm(h1, term='xterm', cmd=cmd1)
    miTerm3=makeTerm(h2, term='xterm', cmd=cmd3)
    print 'commands on h1, h2 done FINISHED'

if __name__ == '__main__':
    # Tell mininet to print useful information /bayesiansdn-demos/network-simulator/mininet/net/samples
    setLogLevel('info')
    simpleTest()
