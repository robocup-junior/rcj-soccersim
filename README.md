# RCJ Soccer Simulator

This is the official repository of the RoboCupJunior Soccer Simulator. The
simulator is based on [Webots](https://github.com/cyberbotics/webots) and this
repository provides both the "automatic referee" (which implements the [Soccer
Simulated Rules](https://github.com/RoboCupJuniorTC/soccer-rules-simulation))
as well as a sample simulated team of robots with some basic strategy.

![Soccer Sim](./media/soccer_sim.png)

## How do I try this out?

1. Download [Webots](https://www.cyberbotics.com/#download)

2. Clone this repository to your computer by running

        git clone https://github.com/RoboCupJuniorTC/rcj-soccer-sim.git

3. Make sure the program will be executed by Python version 3. Set `python3` via
   `Tools > Preferences > Python command`

4. Use Webots to open the downloaded `soccer.wbt` world located in the `worlds`
   directory (via `File > Open World`)

5. Run the simulation. Note that the controllers that are responsible for the
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
