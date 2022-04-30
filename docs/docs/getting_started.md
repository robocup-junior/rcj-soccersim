
# How do I try this out?

It's easy, you can set it up in about 10 minutes!
(plus download time)

## Installation

1. Install Python 3.7 (or higher) 64 bit from the [official website](https://www.python.org/downloads/) (please make sure it is version 3.7 or higher for Windows, and 3.8 or higher if installing on MacOS or Linux). On Windows, please make sure your Python is referenced in Windows PATH by selecting the option "Add Python 3.x to PATH" during the installation. Check out this great [installation guide](https://realpython.com/installing-python/) if you need some help!

2. Download [Webots](https://www.cyberbotics.com/#download) from their official website. Currently, version R2022a is stable with the Soccer Simulator. You can find detailed installation procedure on the official [Webots Installation guide](https://cyberbotics.com/doc/guide/installation-procedure).

3. Clone the rcj-soccersim repository to your computer by downloading the ZIP file from [here](https://github.com/RoboCupJuniorTC/rcj-soccersim/archive/master.zip) or running

        git clone https://github.com/RoboCupJuniorTC/rcj-soccersim.git

4. Finally, run Webots, go to `Tools > Preferences > Python command` and set it to `python` or `python3` to point Webots to Python 3. Depending on your system, the reference to Python 3 can be via the command `python` or `python3`. More information on how to configure Webots to work with Python can be found [here](https://cyberbotics.com/doc/guide/using-python).

## Running Soccer Sim

1. Use Webots to open the downloaded `soccer.wbt` world located in the `worlds`
   directory (via `File > Open World`)

2. Run/pause the simulation by clicking the corresponding buttons on the top-part of Webots window. Note that the controllers that are responsible for the
   various robots on the field can be found in the `controllers/` directory.

## Notes

A specific `webots` world can be executed directly from the command line as
follows:

        webots --mode=run worlds/soccer.wbt

Which allows for at least some automation. Further info can be found in the
[docs](https://cyberbotics.com/doc/guide/starting-webots).

The sample players as well as the "automatic referee" are implemented in
Python, which should allow for easily updating the code to match the rules and
avoid any compilation issues.
