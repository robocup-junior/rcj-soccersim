FROM ubuntu:focal
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install wget gdebi-core xvfb supervisor ffmpeg x264 aria2 xserver-xorg-video-all mesa-utils tigervnc-standalone-server python3 python3-pip xdotool xrdp x11-apps x11-common x11-session-utils x11-xkb-utils x11-xserver-utils x11proto-core-dev x11proto-dev xserver-common xserver-xorg-core xserver-xorg-video-nvidia-455 libxv1 x11-xserver-utils && pip3 install websockets
RUN aria2c -x 16 "https://github.com/cyberbotics/webots/releases/download/R2021a/webots_2021a_amd64.deb" && gdebi -n webots_2021a_amd64.deb && rm webots_2021a_amd64.deb
EXPOSE 1234
EXPOSE 5901
VOLUME /out
#RUN DEBIAN_FRONTEND=noninteractive apt-get -y install xorg
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install libglvnd0 libgl1 libglx0 libegl1 libxext6 libx11-6
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
ENTRYPOINT /app/run-webots.sh
COPY . /app
RUN chmod -R 777 /app
