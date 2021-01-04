from referee.consts import MATCH_TIME, TIME_STEP
from referee.referee import RCJSoccerReferee
from recorder.recorder import VideoRecordAssistant

automatic_mode = False

referee = RCJSoccerReferee(match_time=MATCH_TIME)
recorder = VideoRecordAssistant(referee)

if automatic_mode:
    referee.simulationSetMode(referee.SIMULATION_MODE_FAST)
    recorder.start_recording()

while referee.step(TIME_STEP) != -1:
    referee.emit_positions()

    if not referee.tick():
        break

# When end of match, pause simulator immediately
referee.simulationSetMode(referee.SIMULATION_MODE_PAUSE)

if recorder.is_recording():
    recorder.stop_recording()
    recorder.wait_processing()

if automatic_mode:
    referee.simulationQuit(0)

