#!/bin/bash
vlc-wrapper /home/bayesiansdn/Repositories/pruebas/sampleVideo.mkv --sout='#transcode{vcodec=mp4v,scale=Auto,acodec=mpga,ab=128,channels=2,samplerate=22050}:rtp{sdp=rtsp://:8554/}' \
--sout-keep --loop
# CCL : Se abrirá el video pues no se puede utilizar cvlc (ni vlc) con el usuario root
