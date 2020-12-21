#FROM debian:buster
FROM ubuntu:focal
EXPOSE 1234
EXPOSE 42000
EXPOSE 42001
EXPOSE 42002
EXPOSE 42003
VOLUME /out
RUN apt-get update && apt-get -y upgrade && DEBIAN_FRONTEND=noninteractive apt-get -y install wget gdebi-core xvfb supervisor ffmpeg x264 aria2 xserver-xorg-video-all mesa-utils tigervnc-standalone-server python3 python3-pip xdotool && pip3 install websockets
RUN aria2c -x 16 https://github.com/cyberbotics/webots/releases/download/R2020b-rev1/webots_2020b-rev1_amd64.deb
RUN gdebi -n webots_2020b-rev1_amd64.deb && rm webots_2020b-rev1_amd64.deb
COPY . /app
ENTRYPOINT /app/supervisor.sh
