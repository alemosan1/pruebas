"""
The simulation is run here. 

"""
import scenario_topology
import failure_injection
from random import choice
from datetime import datetime
import ConfigParser
import logging
import json
import os
from time import sleep

def Main(): # Esto es igual que elque simula los errores de red. Lee el config
	config = ConfigParser.ConfigParser()
	config.read(['../config'])
	ip = config.get('main', 'Ip')
	error_interval = int(config.get('main', 'ErrorInterval' ))
	os.system("service filebeat start")

	network = scenario_topology.ScenarioTopo() # Crea la red segun el file scenario_topo.py
	network.run(ip)
	network.stream() # Hace el streaming con el comando que ellos tenian
	orig_timestamp = datetime.now()
	sim_id = str(orig_timestamp.year) + str(orig_timestamp.month) + str(orig_timestamp.day) + \
					  str(orig_timestamp.hour)+ str(orig_timestamp.minute)
	logger = set_logger(sim_id) # Pilla el timestamp para crear el nombre del fichero log - id (Esto deberiamos hacerlo igual)

	now_timestamp = datetime.now()
	minutes = int(config.get('main', 'MinutesRunning'))

	#for switch in network.net.switches:
	#	failure_injection.config_push(switch)

	while (now_timestamp - orig_timestamp).total_seconds() < minutes * 60:
		sleep(error_interval * 2)
		switch = choice(network.net.switches)
		failure_injection.inject(sim_id, switch, error_interval, logger)
		now_timestamp = datetime.now() # Introduce sus errores de red y los mete en el log

	logger.info(sim_id + " stop")
	network.remove()


def set_logger(sim_id):
	logger = logging.getLogger()
	hdlr = logging.FileHandler('/root/log/' + sim_id + '.log')
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr)
	logger.setLevel(logging.INFO)
	logger.info(sim_id + " start " + str(json.dumps(failure_injection.encode_errors())))
	return logger

if __name__ == '__main__':
	Main()
