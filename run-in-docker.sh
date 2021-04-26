#!/bin/bash
xvfb-run /usr/local/webots/webots --stdout --stderr --batch --mode=fast $1
