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

1. You use an UNIX-like environment (i.e. something like Linux or macOS)
2. You have Webots installed and cloned the `rcj-soccersim` repository locally
   (check the [Getting Started](./getting_started.md) guide on how to do so)

## Running Soccer Sim (and Webots) in Automatic Mode

As Webots [docs](https://cyberbotics.com/doc/guide/starting-webots#command-line-arguments)
state, it can also be started from a Terminal, or a command line prompt. The
most basic command would look as follows:

    webots --mode=fast worlds/soccer.wbt

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

    RCJ_SIM_AUTO_MODE=True RCJ_SIM_REC_FORMATS=x3d webots --mode=fast worlds/soccer.wbt

## Running Soccer Sim in Docker

To simplify the automatic running of games, Soccer Sim can also be executed
inside a Docker container. We generally recommend using the offical container
provided by Webots and mentioned in the [official
guide](https://cyberbotics.com/doc/guide/installation-procedure#installing-the-docker-image).


Assuming the `rcj-soccersim` repository is located in the current directory,
running Soccer Sim within docker is as simple as executing

    docker run \
        -v $(pwd)/rcj-soccersim:/rcj-soccersim \
        -e RCJ_SIM_AUTO_MODE=True \
        -e RCJ_SIM_REC_FORMATS=x3d \
        cyberbotics/webots:latest /rcj-soccersim/run-in-docker.sh /rcj-soccersim/worlds/soccer.wbt

Let us briefly discuss the respective lines. On the first one the `docker`
command starts the Docker container, on the second one, the `rcj-soccersim`
folder in the current directory is mapped to `/rcj-soccersim` in the
container, on the following two the `RCJ_SIM_AUTO_MODE` and
`RCJ_SIM_REC_FORMATS` environment variables are being set and on the last one
the `worlds/soccer.wbt` world from the `rcj-soccersim` repository is executed
in the Webex environment using the `run-in-docker.sh` script (also part of the
very same repository).

### Extracting the recorded output

By default, the output (recording and reflog) of a match is saved in the
`reflog/` folder in `controllers/rcj_soccer_referee_supervisor/` of the
`rcj-soccersim` repository. This is relatively inconveniet when it comes to
running multiple games and getting data out of the Docker container and hence
the path can be changed using the `RCJ_SIM_OUTPUT_PATH` environment variable.

The command below redirects the output to the `/tmp/outputs` directory inside
the container and maps it to the `outputs/` directory in the current working
directory on the host:

    docker run \
        -v $(pwd)/rcj-soccersim:/rcj-soccersim \
        -v $(pwd)/outputs:/tmp/outputs  \
        -e RCJ_SIM_AUTO_MODE=True \
        -e RCJ_SIM_REC_FORMATS=x3d \
        -e RCJ_SIM_OUTPUT_PATH=/tmp/outputs/ \
        cyberbotics/webots:latest /rcj-soccersim/run-in-docker.sh /rcj-soccersim/worlds/soccer.wbt

## Environment variables

The full list of environment variables supported by the Soccer Sim can be found
below:

- **`RCJ_SIM_AUTO_MODE`**: If set (to any value), the simulation speed is set to
    fast, the recorders are started at the beginning and the application is
    automatically closed after the match is finished. Not set by default.
- **`RCJ_SIM_MATCH_TIME`**: Sets the number of seconds for which the match is to be
    played. Defaults to 600 (10 minutes).
- **`RCJ_SIM_REC_FORMATS`**: When set, the Soccer Sim starts a recording in these
    formats. The available options are `mp4` and `x3d`. Multiple options can be
    set as well, separated by a comma. Not set by default.
- **`RCJ_SIM_OUTPUT_PATH`**: The path where the reflog outputs as well as the
    recordings are to be saved. Defaults to the `reflog/` folder in
    `controllers/rcj_soccer_referee_supervisor/`.

Internal team-related variables:

- **`RCJ_SIM_TEAM_YELLOW_NAME`**: The name of the yellow team. Defaults to "The Yellows".
- **`RCJ_SIM_TEAM_Y_INITIAL_SCORE`**: The initial score of the yellow team. Defaults to 0.
- **`RCJ_SIM_TEAM_BLUE_NAME`**: The name of the blue team. Defaults to "The Blues".
- **`RCJ_SIM_TEAM_B_INITIAL_SCORE`**: The initial score of the blue team. Defaults to 0.

- **`RCJ_SIM_TEAM_YELLOW_ID`**: The ID of the yellow team used for internal identification.
    Defaults to "The Yellows".
- **`RCJ_SIM_TEAM_BLUE_ID`**: The ID of the yellow team used for internal identification.
    Defaults to "The Blues".
- **`RCJ_SIM_MATCH_ID`**: The ID of the match used for internal identification.
    Defaults to 1.
- **`RCJ_SIM_HALF_ID`**: The ID of the half time used for internal identification.
    Defaults to 1.
