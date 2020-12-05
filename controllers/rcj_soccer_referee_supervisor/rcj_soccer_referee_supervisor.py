from referee.consts import MATCH_TIME, TIME_STEP
from referee.referee import RCJSoccerReferee

referee = RCJSoccerReferee(match_time=MATCH_TIME)

while referee.step(TIME_STEP) != -1:
    referee.emit_positions()

    referee.tick()
