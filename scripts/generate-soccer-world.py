#!/usr/bin/env python

import getopt
import sys
from pathlib import Path
from string import Template

try:
    options, _ = getopt.getopt(
        sys.argv[1:],
        "",
        [
            "template=",
            "blue_rgb=",
            "yellow_rgb=",
            "blue_png_url=",
            "yellow_png_url=",
            "controller_blue=",
            "controller_yellow=",
            "ir_range=",
        ],
    )
except getopt.GetoptError as err:
    print("ERROR:", err)
    sys.exit(1)


template_path = None
# Default params
params = {"ir_range": "0.6"}
for option, value in options:
    if option == "--template":
        template_path = Path(value)
    else:
        clean_key = option.replace("--", "")
        params[clean_key] = value

if template_path is None or not template_path.exists():
    print(f"ERROR: Provided path {template_path} does not exist")
    sys.exit(1)

s = Template(template_path.read_text())
print(s.substitute(params), end="")
