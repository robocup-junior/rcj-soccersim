# Running the simulator

_Note: This document is intended for the organizers of events in which the RCJ
Soccer Sim is to be used_

This document outlines how the RoboCupJunior Soccer Sim can be used to simulate
a match in a "headless" way. In other words, it shows how you can go from
having the code for two teams and the RoboCupJunior Soccer Sim code to getting
an output in form of either an MPEG-4 video or a HTML site.

**Input**
- Source code for the yellow team
- Source code for the blue team
- RoboCupJunior Soccer Sim

**Output**
- MPEG-4 video and/or HTML site
- JSON file containing all the important events happened during the game

## Preliminaries

This guide makes a couple of assumptions:
1. You use a UNIX-like environment (i.e. something like Linux or macOS)
2. You have Webots installed and cloned the `rcj-soccer-sim` repository locally
   (check the [Getting Started](./getting_started.md) guide on how to do so)

## Running Soccer Sim (and Webots) in Automatic Mode

As Webots [docs](https://cyberbotics.com/doc/guide/starting-webots#command-line-arguments)
state, it can also be started from a Terminal, or a command line prompt. The
most basic command would look as follows:

    $ webots --mode=fast worlds/soccer.wbt

This opens up Webots and automatically starts the game in the GUI. You can then
either pause the game, restart it or even manually setup the video/HTML export.

Soccer Sim's referee has the ability to automatically start the recording and
stop the execution when it finishes. To do so, the `RCJ_SIM_AUTO_MODE`
environment variable needs to be set (the value doesn't matter but we suggest
`True` or something of that sort). Furthermore, to make sure the game is
recorded, a recording format needs to be specified. This is done via the
`RCJ_SIM_REC_FORMATS` environment variable and all the options are documented
in the section below.

In summary, to automatically run the `world/soccer.wbt` world file (the Soccer
environment) and record the output in HTML format, the following command can be
used:

    $ RCJ_SIM_AUTO_MODE=True RCJ_SIM_REC_FORMATS=x3d webots --mode=run worlds/soccer.wbt


## Environment variables

The full list of environment variables supported by the Soccer Sim can be found
below:

- `RCJ_SIM_AUTO_MODE`: If set (to any value), the simulation speed is set to
    fast, the recorders are started at the beginning and the application is
    automatically closed after the match is finished. Not set by default.
- `RCJ_SIM_MATCH_TIME`: Sets the number of seconds for which the match is to be
    played. Defaults to 600 (10 minutes).
- `RCJ_SIM_REC_FORMATS`: When set, the Soccer Sim starts a recording in these
    formats. The available options are `mp4` and `x3d`. Multiple options can be
    set as well, separated by a comma. Not set by default.
- `RCJ_SIM_OUTPUT_PATH`: The path where the reflog outputs as well as the
    recordings are to be saved. Defaults to the `reflog/` folder in
    `controllers/rcj_soccer_referee_supervisor/`.

- `RCJ_SIM_TEAM_YELLOW_NAME`: The name of the yellow team. Defaults to "The Yellows".
- `RCJ_SIM_TEAM_Y_INITIAL_SCORE`: The initial score of the yellow team. Defaults to 0.
- `RCJ_SIM_TEAM_BLUE_NAME`: The name of the blue team. Defaults to "The Blues".
- `RCJ_SIM_TEAM_B_INITIAL_SCORE`: The initial score of the blue team. Defaults to 0.

- `RCJ_SIM_TEAM_YELLOW_ID`: The ID of the yellow team used for internal identification.
    Defaults to "The Yellows".
- `RCJ_SIM_TEAM_BLUE_ID`: The ID of the yellow team used for internal identification.
    Defaults to "The Blues".
- `RCJ_SIM_MATCH_ID`: The ID of the match used for internal identification.
    Defaults to 1.
- `RCJ_SIM_HALF_ID`: The ID of the half time used for internal identification.
    Defaults to 1.
