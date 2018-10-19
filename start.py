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


class SingleSwitchTopo(Topo):

    def build(self, n=2):
    	    switch = self.addSwitch('s1')

    	    for h in range(n):
    		    host = self.addHost('h%s' % (h + 1))
      		    self.addLink(host, switch)

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
    os.chdir("logs")
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H:%M:%S')
    for filename in os.listdir("."):
        if (containNumber(filename) != True):
            os.rename(filename,filename[:-4]+st+".txt")
    os.chdir("..")

# Starts simulation    
def simpleTest():
    #Añadimos controlador odl, ip por defecto
    #controller = RemoteController('c1', ip='127.0.0.1', port=6633)
    topo = SingleSwitchTopo(n=4)
    #net = Mininet(topo=topo, controller=controller)
    net = Mininet(topo=topo) # Quito el controller para no tener que estar iniciando ODL
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Let's do a pingAll..."
    net.pingAll()
    src = net.get('h1') 
    dst = net.get('h2')



    #Container codec format
    muxerCodecVlan= {1:'mpeg1',2:'ts',3:'ps',4:'mp4',5:'avi',6:'asf',7:'dummy',8:'ogg',9:''}
    #INFO
    # mpeg1   MPEG-1 multiplexing - recommended for portability. Only works with mp1v video and mpga audio, but works on all known players
    # ts  MPEG Transport Stream, primarily used for streaming MPEG. Also used in DVDs
    # ps  MPEG Program Stream, primarily used for saving MPEG data to disk.
    # mp4 MPEG-4 mux format, used only for MPEG-4 video and MPEG audio.
    # avi AVI
    # asf ASF
    # dummy   dummy output, can be used in creation of MP3 files.
    # ogg

    #Video codec format
    videoCodecVlan= {1:'mp1v',2:'mp2v',3:'mp4v',4:'SVQ1',5:'SVQ3',6:'DVDv',
    7:'WMV1',8:'WMV2',9:'WMV3',10:'DVSD',11:'MJPG',12:'H263',13:'h264',14:'theo',
    15:'IV20',16:'IV40',17:'RV10',18:'cvid',19:'VP31',20:'FLV1',21:'CYUV',22:'HFYU',
    23:'MSVC',24:'MRLE',25:'AASC',26:'FLIC',27:'QPEG',28:'VP8'}

    #INFO
    # mp1v    MPEG-1 Video - recommended for portability ---> funciona con mux = ts
    # mp2v    MPEG-2 Video - used in DVDs ----> funciona con mux = ts
    # mp4v    MPEG-4 Video  ---> Funciona tanto con mux como sin mux
    # SVQ1    Sorenson Video v1 --> No funciona
    # SVQ3    Sorenson Video v3 --> No esta instalada la biblioteca necesario
    # DVDv    VOB Video - used in DVDs --> no funciona
    # WMV1    Windows Media Video v1 ---> funciona con ts
    # WMV2    Windows Media Video v2 -- funciona con ts
    # WMV3    Windows Media Video v3, also called Windows Media 9 (unsupported)
    # DVSD    Digital Video ---> no funciona
    # MJPG    MJPEG ----> funciona con ts (linea verde cunado hay error interesante)
    # H263    H263 ----> no esta instalado el codec
    # h264    H264 ---> funciona 
    # theo    Theora ---> no funciona con ts
    # IV20    Indeo Video --> Su instalación Libav/FFmpeg (libavcodec) no tiene el siguiente codificador:
    # IV40    Indeo Video version 4 or later (unsupported) ---> no funciona con ts
    # RV10    Real Media Video ---> no funciona ts
    # cvid    Cinepak ---> no funciona 
    # VP31    On2 VP ---> no esta instalado el codec
    # FLV1    Flash Video ---> no funciona con ts
    # CYUV    Creative YUV --> no esta instalada
    # HFYU    Huffman YUV ---> no funciona  con ts
    # MSVC    Microsoft Video v1 --> no funciona con ts
    # MRLE    Microsoft RLE Video --> no funciona con ts
    # AASC    Autodesc RLE Video --> no instalado 
    # FLIC    FLIC video ---> no instalado
    # QPEG    QPEG Video ----> no esta instalado
    # VP8 VP8 Video ---> no funciona con ts 

    #AUDIO CODEC FORMAT
    
    audioCodecVlan= {1:'mpga',2:'mp3',3:'mp4a',4:'a52',5:'vorb',6:'spx',7:'flac'}

    #INFO
    # mpga    MPEG audio (recommended for portability)
    # mp3     MPEG Layer 3 audio
    # mp4a    MP4 audio
    # a52     Dolby Digital (A52 or AC3)
    # vorb    Vorbis
    # spx     Speex
    # flac    FLAC

    #Configuration parameters

    codecVideoUsed=videoCodecVlan[13]
    codecAudioUsed=videoCodecVlan[6]
    codecMuxerUsed=muxerCodecVlan[2]

    enableMuxRTP="--sout-rtp-rtcp-mux"
    CPUlimit = ""
    #Server side
    cmdServer=""
    if type == '0' : # No errors
        cmdServer = "su bayes -c \"cvlc -vvv videos/sampleVideo.mkv --sout='#rtp{sdp=rtsp://:5004/}' --sout-keep --loop 2>&1 | ./timestamp.sh server "+type+"\""
    elif type == '1' : # Low fps rate and binary bit rate (video)
        cmdServer = "su bayes -c \"cvlc -vvv videos/sampleVideo.mkv --sout='#transcode{vcodec="+codecVideoUsed+",vb=60,vfilter=freeze,fps=5,scale=Automático,acodec=mpga,ab=256,channels=3,samplerate=22050,scodec=t140,soverlay}:rtp{sdp=rtsp://:5004/}' --sout-keep --loop 2>&1 | ./timestamp.sh server "+type+"\""
    elif type == '2' : #  Low sample rate (Audio)
        cmdServer = "su bayes -c \"cvlc -vvv videos/sampleVideo.mkv --sout='#transcode{vcodec="+codecVideoUsed+",scale=Auto,acodec=mpga,ab=128,channels=2,samplerate=8000}:rtp{sdp=rtsp://:5004/}' --sout-keep --loop 2>&1 | ./timestamp.sh server "+type+"\""
    elif type == '3' : #TO DO: incompatible mux format 
        cmdServer = "su bayes -c \"cvlc -vvv videos/sampleVideo.mkv --sout='#transcode{vcodec=avi,scale=Automático,acodec=mpga,ab=128,channels=2,samplerate=44100}:rtp{mux="+codecMuxerUsed+",sdp=rtsp://:5004/}' --sout-keep --loop  2>&1 | ./timestamp.sh server "+type+"\""
    elif type == '4' : #MP4 example
        cmdServer = "su bayes -c \"cvlc -vvv videos/sampleVideo.mkv --sout='#transcode{vcodec="+codecVideoUsed+",vb=2000,scale=Automático,acodec=vorb,ab=128,channels=2,samplerate=44100}:rtp{mux=mpeg1,sdp=rtsp://:5004/}' --sout-keep --loop 2>&1 | ./timestamp.sh server "+type+"\""
    elif type == '5' : #Limitation of CPU limit
        cmdServer = "su bayes -c \"cvlc -vvv videos/sampleVideo.mkv --sout='#rtp{sdp=rtsp://:5004/}' --sout-keep --loop 2>&1 | ./timestamp.sh server "+type+"\""
        CPUlimit = "& cpulimit -p `expr $! - 1` -l 15"
    #Client side
    #TODO: tenemos que poner que la IP se saque programaticamente
    cmdClient = "vlc-wrapper -vvv -R --network-caching 200 rtsp://10.0.0.1:5004/ 2>&1 | ./timestamp.sh cliente "+type+CPUlimit
    
    termSrc = makeTerm(src, title='VLC Server', term='xterm', display=None, cmd=cmdServer)
    time.sleep(3)
    termDst = makeTerm(dst, title='VLC Client', term='xterm', display=None, cmd=cmdClient)
    time.sleep(3)

    #Ahora vamos a poner un terminal para sacar informacióm
    cmdInfo = " ifstat 10.0.0.2 > codeccompresion/"+codecVideoUsed+codecMuxerUsed+".info"
    termGetInfo = makeTerm(dst,title= "Monitoring traffic", term='xterm', display=None, cmd=cmdInfo)

    
    # logfile = open("logs/clientVLC-log.txt","r") 
    # loglines = follow(logfile)
    # for line in loglines:
    #     st = datetime.datetime.now()
    #     print "["+str(st)+"]"+line,

    #Method to obtain information in log Files
    getInformation()
    CLI(net)
    cmdExit = "kill $(ps aux | grep 'vlc' | grep -v grep | awk '{print $2}');kill $(ps aux | grep 'ifstat' | grep -v grep | awk '{print $2}')"
    os.system(cmdExit)
    net.stop()

    

if __name__ == '__main__':
    setLogLevel('info')
    configerror= ConfigParser.ConfigParser()
    configerror.read(['./config_vlc.py'])
    type =configerror.get('errors','Type')

    #Vamos a renombrar los logs para cada vez que se ejecueten se guarden los previos.
    renameLog()
    simpleTest()
