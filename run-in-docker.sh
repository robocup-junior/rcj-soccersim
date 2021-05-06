#!/bin/bash
apt update
apt install -y python3-pip
pip3 install numpy==1.20.2 scipy==1.6.3 --user
xvfb-run /usr/local/webots/webots --stdout --stderr --batch --mode=fast $1
