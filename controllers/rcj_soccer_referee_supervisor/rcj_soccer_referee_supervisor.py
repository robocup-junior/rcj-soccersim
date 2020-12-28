from referee.consts import MATCH_TIME, TIME_STEP
from referee.referee import RCJSoccerReferee
from recorder.recorder import VideoRecordAssistant

referee = RCJSoccerReferee(match_time=MATCH_TIME)

recorder = VideoRecordAssistant(referee)
recorder.start_recording()

while referee.step(TIME_STEP) != -1:
    referee.emit_positions()

    if not referee.tick():
        break

recorder.stop_recording()

# When end of match, pause simulator immediately
referee.simulationSetMode(referee.SIMULATION_MODE_PAUSE)
