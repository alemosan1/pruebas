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
import subprocess
import glob
import time
import datetime
import ConfigParser

#Creo este fichero para guardar las otras funciones que tenemos.
#Ya uniremos todo y borraremos esto.

# Get information about the vlc logs like the ID, video parameters
def getInformation():
    list_of_files_server = glob.glob('/home/bayes/Repositories/pruebas/logs/server*') # * means all if need specific format then *.csv
    list_of_files_client = glob.glob('/home/bayes/Repositories/pruebas/logs/client*')
    latest_file_server = max(list_of_files_server, key=os.path.getctime)
    latest_file_client = max(list_of_files_client, key=os.path.getctime)


# Reads the full file line per line
def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def containNumber(inputString):
    return any(char.isdigit() for char in inputString)

# Renames the log file so we have a new one each time
def renameLog():
    os.chdir("../../logs")
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H:%M:%S')
    for filename in os.listdir("."):
        if (containNumber(filename) != True):
            os.rename(filename,filename[:-4]+st+".txt")
    os.chdir("..")

