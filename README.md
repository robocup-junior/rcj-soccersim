# RCJ Soccer Sim Webots Playground

This repository serves as a playground for various experiments related to
setting up a simulated RCJ Soccer environment in the Webots simulator.

It currently features a sample robot as well as a supervisor. These are in an
aplha stage and will very probably change in the future.

## How do I try this out?

1. Download [Webots](https://www.cyberbotics.com/])

2. Clone this repository to your computer by running `git clone https://github.com/RoboCupJuniorTC/webots-soccer-sim-playground.git`

3. Open the downloaded `soccer.wbt` world which you can find in the `worlds`
   directory (via `File > Open World`)

4. Run the simulation. Note that just one robot (`B1`) will move usint the
   Python controler which is located at
   `controllers/rcj_soccer_player/rcj_soccer_player.py`. Every other robot will
   stand still

## Notes

A specific `webots` world can be executed directly from the command line as
follows:

        webots --mode=run worlds/soccer.wbt

Which allows for at least some automation. Further info can be found in the
[docs](https://cyberbotics.com/doc/guide/starting-webots).

Both the sample player as well as the supervisor are implemented in Python,
which should allow for easily updating the code to match the rules and avoid
any compilation issues.
