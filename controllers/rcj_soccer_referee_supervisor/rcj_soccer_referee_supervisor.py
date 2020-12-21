from math import ceil
from referee.consts import MATCH_TIME, TIME_STEP
from referee.referee import RCJSoccerReferee

referee = RCJSoccerReferee(
    match_time=MATCH_TIME,
    progress_check_steps=ceil(15/(TIME_STEP/1000.0)),
    progress_check_threshold=0.5,
    ball_progress_check_steps=ceil(10/(TIME_STEP/1000.0)),
    ball_progress_check_threshold=0.5,
)

while referee.step(TIME_STEP) != -1:
    referee.emit_positions()

    if not referee.tick():
        break

# When end of match, pause simulator immediately
referee.simulationSetMode(referee.SIMULATION_MODE_PAUSE)
