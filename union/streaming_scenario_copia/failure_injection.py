import ConfigParser
import httplib
import base64
import xml.etree.ElementTree as ET
import json
import time
from datetime import datetime

error_dictionary = {}
error_dictionary[6] = {'err_type': 'e6', 'Desc': 'All flows (except the CONTROLLER one) from a switch have been modified by changing the node-connector-output field', 'Params': {'Switch': '', 'Timestamp': ''}}
error_dictionary['6f'] = {'err_type': 'e6', 'Desc': 'All flows (except the CONTROLLER one) from a switch have been modified by changing the node-connector-output field', 'Params': {'Switch': '', 'Timestamp': ''}}
logger = None

# Sends error_dictionary
def encode_errors():
	config = ConfigParser.ConfigParser()
	config.read('../config')
	coll_int = config.get('main','CollectorInterval')
	error_dictionary['delay'] = int(coll_int)
	return error_dictionary

# Initial push of all flow data in operational database into config database
# in order to optimize some of the methods below this one
def config_push(node):
	node_dec = int(node, 16)
	resp_xml = odl_comm(params = ("GET", "/restconf/operational/opendaylight-inventory:nodes/node/openflow:"+str(node_dec)+"/flow-node-inventory:table/0"))
	flow_id = None
	old_xml = {}

	root = ET.fromstring(resp_xml)

	for child in root.findall('{urn:opendaylight:flow:inventory}flow'):
		for subchild in child:
			if subchild.tag == "{urn:opendaylight:flow:inventory}id" and '#UF' not in subchild.text:
				flow_id = subchild.text
				resp2_xml = odl_comm(params = ("GET", "/restconf/operational/opendaylight-inventory:nodes/node/openflow:"+str(node_dec)+"/flow-node-inventory:table/0/flow/"+str(flow_id)))
				old_xml[flow_id] = resp2_xml

				root2 = ET.fromstring(resp2_xml)
				for node in root2.findall('{urn:opendaylight:flow:statistics}flow-statistics'):
					root2.remove(node)

				data = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + ET.tostring(root2).replace('ns0:', '').replace('ns1:', '').replace(':ns0', '').replace(':ns1', '').replace(' xmlns="urn:opendaylight:flow:statistics"', '')
				
				headers2 = { 'Content-type' : 'application/yang.data+xml','Authorization' : 'Basic %s' %  str(base64.b64encode(b"admin:admin").decode("ascii")) }
				resp2_xml = odl_comm(params = ("PUT", "/restconf/config/opendaylight-inventory:nodes/node/openflow:"+str(node_dec)+"/flow-node-inventory:table/0/flow/"+str(flow_id)), body = data, headers = headers2)
	return


def inject(sim_id, node, error_interval, logger):

	logger.info(sim_id + ' pause')
	time.sleep(4)
	send_report(6, {'Switch': str(int(node.dpid, 16)), 'Timestamp': str(datetime.now())}, sim_id, logger)
	dictionary = change_flow(node.dpid)
	logger.info(sim_id + ' play')
	time.sleep(error_interval)
	print 'Fixing modified flows error...'
	logger.info(sim_id + ' pause')
	time.sleep(4)
	fix_node_flow(node.dpid, dictionary)
	print 'Fixed'
	send_report(str(6) + 'f', {'Switch': str(int(node.dpid, 16)), 'Timestamp': str(datetime.now())}, sim_id,
					   logger)
	logger.info(sim_id + ' play')


# Sends error and fix reports
def send_report(err, parameters, sim_id, logger):
	error_report = error_dictionary.get(err)
	error_report['Params'] = parameters
	if isinstance(err, (int, long)):
		logger.info(sim_id + " err " + str(json.dumps({'err': error_report})))
	else:
		logger.info(sim_id + " fix " + str(json.dumps({'err': error_report})))
	return

# Communicates with Opendaylight
def odl_comm(params, headers=None, timeout=1000, body=None):
	config = ConfigParser.ConfigParser()
	config.read('../config')
	ip = str(config.get('main','Ip'))
	conn = httplib.HTTPConnection(ip, 8181)
	userAndPass = base64.b64encode(b"admin:admin").decode("ascii")
	if headers == None:
		headers = { 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Authorization' : 'Basic %s' %  userAndPass }
	if body == None:
		conn.request(str(params[0]), str(params[1]), headers=headers)
	else:
		conn.request(str(params[0]), str(params[1]), headers=headers, body=body)
	resp = conn.getresponse().read()
	conn.close()
	return resp

def change_flow(node):
	node_dec = int(node, 16)
	node_dec = 3
	resp_xml = odl_comm(params = ('GET', "/restconf/operational/opendaylight-inventory:nodes/node/openflow:" +str
		(node_dec ) +"/flow-node-inventory:table/0"))
	old_xml = {}
	flow_id = None

	root = ET.fromstring(resp_xml)

	for child in root.findall('{urn:opendaylight:flow:inventory}flow'):
		for subchild in child:
			if subchild.tag == "{urn:opendaylight:flow:inventory}id" and '#UF' not in subchild.text:
				flow_id = subchild.text
				resp2_xml = odl_comm(params = ('GET', "/restconf/operational/opendaylight-inventory:nodes/node/openflow:" +str
												 (node_dec ) +"/flow-node-inventory:table/0/flow/" +str(flow_id)))
				old_xml[flow_id] = resp2_xml
				root2 = ET.fromstring(resp2_xml)

				for node in root2.iter('{urn:opendaylight:flow:inventory}output-node-connector'):
						node.text = '0'
				for node in root2.findall('{urn:opendaylight:flow:statistics}flow-statistics'):
					root2.remove(node)

				data = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + ET.tostring(root2).replace('ns0:', '').replace \
					('ns1:', '').replace(':ns0', '').replace(':ns1', '').replace \
					(' xmlns="urn:opendaylight:flow:statistics"', '')
				headers2 = { 'Content-type' : 'application/yang.data+xml'
							,'Authorization' : 'Basic %s' %  str(base64.b64encode(b"admin:admin").decode("ascii")) }
				odl_comm(params =("PUT", "/restconf/config/opendaylight-inventory:nodes/node/openflow:" +str
					(node_dec ) +"/flow-node-inventory:table/0/flow/" +str(flow_id)), body = data, headers = headers2)
	return old_xml


# Given a dictionary of 'flow' xmls, it pushes each flow
# separately into the node
def fix_node_flow(node, dictionary):
	node_dec = int(node, 16)
	node_dec = 3

	for flow_id, odl_xml in dictionary.iteritems():
		time.sleep(2)
		root2 = ET.fromstring(odl_xml)

		for node in root2.findall('{urn:opendaylight:flow:statistics}flow-statistics'):
			root2.remove(node)

		data = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + ET.tostring(root2).replace('ns0:',
																									 '').replace('ns1:',
																												 '').replace(
			':ns0', '').replace(':ns1', '').replace(' xmlns="urn:opendaylight:flow:statistics"', '')

		headers2 = {'Content-type': 'application/yang.data+xml',
					'Authorization': 'Basic %s' % str(base64.b64encode(b"admin:admin").decode("ascii"))}
		odl_comm(params=("PUT", "/restconf/config/opendaylight-inventory:nodes/node/openflow:" + str(
			node_dec) + "/flow-node-inventory:table/0/flow/" + str(flow_id)), body=data, headers=headers2)
	return


# Given a 'table' xml, this function pushes it
# to a node
def fix_node_table(node, old_xml):
	node_dec = int(node, 16)

	flow_id = None
	root = ET.fromstring(old_xml)

	for child in root.findall('{urn:opendaylight:flow:inventory}flow'):
		for node in child.iter('{urn:opendaylight:flow:statistics}flow-statistics'):
			child.remove(node)

	for child in root.findall('{urn:opendaylight:flow:table:statistics}flow-table-statistics'):
		root.remove(child)	

	data = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + ET.tostring(root).replace('ns0:', '').replace('ns1:', '').replace(':ns0', '').replace(':ns1', '')

	headers2 = { 'Content-type' : 'application/yang.data+xml','Authorization' : 'Basic %s' %  str(base64.b64encode(b"admin:admin").decode("ascii")) }
	odl_comm(params = ("PUT", "/restconf/config/opendaylight-inventory:nodes/node/openflow:"+str(node_dec)+"/table/0"), body = data, headers = headers2)
	return
