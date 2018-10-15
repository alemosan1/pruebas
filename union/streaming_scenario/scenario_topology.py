#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.clean import cleanup
from time import sleep
from os import system

class ScenarioTopo( Topo ):

	def __init__( self ): # Crea la red
		Topo.__init__( self )

		s1, s2, s3 = [ self.addSwitch(s) for s in ('s1','s2','s3') ]
		self.addLink(s1, s2)
		self.addLink(s2, s3)
		self.addLink(s3, s1)

		h1, h2 = [ self.addHost(h) for h in ('h1','h2') ]
		self.addLink(h1, s1)
		self.addLink(h2, s3)
		self.net = None

	def run(self, remote_ip): # Conecta con el opendaylight
		controller = RemoteController('c1', ip=remote_ip, port=6633)
		self.net = Mininet(topo=self, link=TCLink, controller=controller )
		setLogLevel("debug")
		self.net.start()
		sleep(3)
		self.net.pingAll()

	def remove(self): # Para la simulacion (creo)
		self.net.stop()
		cleanup()

	def stream(self): # Comieza el streaming
		h1 = self.net.get('h1')
		system('systemd-machine-id-setup')
		h1.cmd('../net/vlc_send.sh &') # Sin xterm y eso me hace dudar
		CLI(self.net)

