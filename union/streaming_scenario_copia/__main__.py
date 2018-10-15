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

def Main(): # Esto es igual que el que simula los errores de red. Lee el config
	config = ConfigParser.ConfigParser()
	config.read(['../config'])
	ip = config.get('main', 'Ip') # Pilla la ip del controlador
	error_interval = int(config.get('main', 'ErrorInterval' )) # Pilla el intervalo en segundos entre dos errores
	os.system("service filebeat start") # Inicia filebeat como servicio 

	network = scenario_topology.ScenarioTopo() # Crea la red desde scenario_topo.py
	network.run(ip)
	network.stream() # Hace el streaming con el comando que ellos tenian
	# Ver los 3 metodos anteriores en scenario_topo
	orig_timestamp = datetime.now() 
	sim_id = str(orig_timestamp.year) + str(orig_timestamp.month) + str(orig_timestamp.day) + \
					  str(orig_timestamp.hour)+ str(orig_timestamp.minute) # Crea un timestamp para usar como ID de la simulacion
	logger = set_logger(sim_id) # Comienza a crear logs

	now_timestamp = datetime.now()
	minutes = int(config.get('main', 'MinutesRunning')) # Pilla cuntos minutos debe durar la simulacion

	#for switch in network.net.switches:
	#	failure_injection.config_push(switch)

	while (now_timestamp - orig_timestamp).total_seconds() < minutes * 60: # Mientras no se cumpla el tiempo de simulacion
		sleep(error_interval * 2) # Sleep entre errores
		switch = choice(network.net.switches) # Pilla un switch aleatorio
		failure_injection.inject(sim_id, switch, error_interval, logger) # Crea el fallo - ver metodo en failure_injection
		now_timestamp = datetime.now()

	logger.info(sim_id + " stop") # Una vez acaba la simulacion, lo resalta en el log
	network.remove() # Para la red - mininet

def set_logger(sim_id): 
	logger = logging.getLogger()
	hdlr = logging.FileHandler('/root/log/' + sim_id + '.log')
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s') # Creacion de los logs: timestamp+log level+mensaje
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr)
	logger.setLevel(logging.INFO)
	logger.info(sim_id + " start " + str(json.dumps(failure_injection.encode_errors())))
	return logger

if __name__ == '__main__':
	Main()
