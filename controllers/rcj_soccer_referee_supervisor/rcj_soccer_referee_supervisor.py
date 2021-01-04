from math import ceil
from datetime import datetime
from pathlib import Path, PosixPath

from referee.consts import MATCH_TIME, TIME_STEP
from referee.event_handlers import JSONLoggerHandler, DrawMessageHandler
from referee.referee import RCJSoccerReferee
from recorder.recorder import VideoRecordAssistant

automatic_mode = False

TEAM_YELLOW = "The Yellows"
TEAM_BLUE = "The Blues"


def output_path(
    directory: Path,
    team_blue: str,
    team_yellow: str,
) -> PosixPath:

    now_str = datetime.utcnow().strftime('%Y%m%dT%H%M%S.%fZ')
    team_blue = team_blue.replace(' ', '_')
    team_yellow = team_yellow.replace(' ', '_')

    # Ensure the directory ecists
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)

    p = directory / Path(f'{team_blue}_vs_{team_yellow}-{now_str}')
    return p


output_prefix = output_path(Path('reflog'), TEAM_BLUE, TEAM_YELLOW)
reflog_path = output_prefix.with_suffix('.jsonl')
video_path = output_prefix.with_suffix('.mp4')

referee = RCJSoccerReferee(
    match_time=MATCH_TIME,
    progress_check_steps=ceil(15/(TIME_STEP/1000.0)),
    progress_check_threshold=0.5,
    ball_progress_check_steps=ceil(10/(TIME_STEP/1000.0)),
    ball_progress_check_threshold=0.5,
    team_name_blue=TEAM_BLUE,
    team_name_yellow=TEAM_YELLOW,
    penalty_area_allowed_time=15,
    penalty_area_reset_after=2,
)

recorder = VideoRecordAssistant(
    supervisor=referee,
    output_path=str(video_path),
    resolution="720p",
)

if automatic_mode:
    referee.simulationSetMode(referee.SIMULATION_MODE_FAST)
    recorder.start_recording()

referee.add_event_subscriber(JSONLoggerHandler(reflog_path))
referee.add_event_subscriber(DrawMessageHandler())

referee.kickoff()

# The "event" loop for the referee
while referee.step(TIME_STEP) != -1:
    referee.emit_positions()

    # If the tick does not return True, the match has ended and the event loop
    # can stop
    if not referee.tick():
        break

# When end of match, pause simulator immediately
referee.simulationSetMode(referee.SIMULATION_MODE_PAUSE)

if recorder.is_recording():
    recorder.stop_recording()
    recorder.wait_processing()

if automatic_mode:
    referee.simulationQuit(0)

