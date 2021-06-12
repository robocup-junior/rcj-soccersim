#!/bin/bash
# Note that this assumes a Debian distribution
apt -qq update
apt -qq install python3-pip -y > /dev/null
pip3 -q install numpy==1.20.2 scipy==1.6.3 --user
xvfb-run /usr/local/webots/webots --stdout --stderr --batch --mode=fast $1
