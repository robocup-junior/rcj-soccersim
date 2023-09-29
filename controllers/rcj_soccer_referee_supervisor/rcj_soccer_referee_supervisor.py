import logging
import os
from datetime import datetime
from math import ceil
from pathlib import Path, PosixPath

from recorder.consts import RecordingFormat
from recorder.recorder import (
    BaseVideoRecordAssistant,
    MP4VideoRecordAssistant,
    X3DVideoRecordAssistant,
)
from referee.consts import DEFAULT_MATCH_TIME, TIME_STEP
from referee.event_handlers import DrawMessageHandler, JSONLoggerHandler
from referee.referee import RCJSoccerReferee
from referee.supervisor import RCJSoccerSupervisor


def get_video_recorder_class(rec_format: str) -> BaseVideoRecordAssistant:
    return {
        RecordingFormat.MP4.value: MP4VideoRecordAssistant,
        RecordingFormat.X3D.value: X3DVideoRecordAssistant,
    }[rec_format]


def output_path(
    directory: Path,
    team_blue_id: str,
    team_yellow_id: str,
    match_id: int,
    half_id: int,
) -> PosixPath:
    now_str = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    team_blue = team_blue_id.replace(" ", "_")
    team_yellow = team_yellow_id.replace(" ", "_")

    # Ensure the directory exists
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)

    name = f"{match_id}_-_{half_id}_-_{team_blue}_vs_{team_yellow}-{now_str}"
    filename = Path(name)
    return directory / filename


TEAM_YELLOW = os.environ.get("RCJ_SIM_TEAM_YELLOW_NAME", "The Yellows")
TEAM_YELLOW_ID = os.environ.get("RCJ_SIM_TEAM_YELLOW_ID", "The Yellows")
YELLOW_INITIAL_SCORE = os.environ.get("RCJ_SIM_TEAM_Y_INITIAL_SCORE", "0")
TEAM_YELLOW_INITIAL_SCORE = int(YELLOW_INITIAL_SCORE or "0")

TEAM_BLUE = os.environ.get("RCJ_SIM_TEAM_BLUE_NAME", "The Blues")
TEAM_BLUE_ID = os.environ.get("RCJ_SIM_TEAM_BLUE_ID", "The Blues")
BLUE_INITIAL_SCORE = os.environ.get("RCJ_SIM_TEAM_B_INITIAL_SCORE", "0")
TEAM_BLUE_INITIAL_SCORE = int(BLUE_INITIAL_SCORE or "0")

MATCH_ID = os.environ.get("RCJ_SIM_MATCH_ID", "1")
HALF_ID = int(os.environ.get("RCJ_SIM_HALF_ID", 1))

REC_FORMATS_RAW = os.environ.get("RCJ_SIM_REC_FORMATS", "").split(",")
REC_FORMATS = [f for f in REC_FORMATS_RAW if f]
MATCH_TIME = int(os.environ.get("RCJ_SIM_MATCH_TIME", DEFAULT_MATCH_TIME))

automatic_mode = True if "RCJ_SIM_AUTO_MODE" in os.environ.keys() else False

REFLOG_OUTPUT_PATH = os.environ.get("RCJ_SIM_OUTPUT_PATH", "reflog")
directory = Path(REFLOG_OUTPUT_PATH)
output_prefix = output_path(
    directory,
    TEAM_BLUE_ID,
    TEAM_YELLOW_ID,
    MATCH_ID,
    HALF_ID,
)
reflog_path = output_prefix.with_suffix(".jsonl")

supervisor = RCJSoccerSupervisor()
referee = RCJSoccerReferee(
    supervisor=supervisor,
    match_time=MATCH_TIME,
    progress_check_steps=ceil(15 / (TIME_STEP / 1000.0)),
    progress_check_threshold=0.5,
    ball_progress_check_steps=ceil(10 / (TIME_STEP / 1000.0)),
    ball_progress_check_threshold=0.5,
    team_name_blue=TEAM_BLUE,
    team_name_yellow=TEAM_YELLOW,
    initial_score_blue=TEAM_BLUE_INITIAL_SCORE,
    initial_score_yellow=TEAM_YELLOW_INITIAL_SCORE,
    penalty_area_allowed_time=15,
    penalty_area_reset_after=2,
    match_id=MATCH_ID,
    half_id=HALF_ID,
)

recorders = []
available_recording_formats = RecordingFormat.all()
for rec_format in REC_FORMATS:
    if rec_format not in available_recording_formats:
        raise ValueError(f"Unexpected video format {rec_format}")

    recorder_class = get_video_recorder_class(rec_format)
    rec_suffix = recorder_class.output_suffix

    recorders.append(
        recorder_class(
            supervisor=supervisor,
            output_path=str(output_prefix.with_suffix(f".{rec_suffix}")),
            resolution="720p",
        )
    )

if automatic_mode:
    supervisor.simulationSetMode(supervisor.SIMULATION_MODE_FAST)
    for recorder in recorders:
        recorder.start_recording()

referee.add_event_subscriber(JSONLoggerHandler(reflog_path))
referee.add_event_subscriber(DrawMessageHandler())

referee.kickoff()

# The "event" loop for the referee
while supervisor.step(TIME_STEP) != -1:
    # If the tick does not return True, the match has ended and the event loop
    # can stop
    if not referee.tick():
        break

# When end of match, pause simulator immediately
supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE)

for recorder in recorders:
    if recorder.is_recording():
        recorder.stop_recording()
        logging.info(f"Processing {recorder.output_suffix} video...")
        recorder.wait_processing()

if automatic_mode:
    supervisor.simulationQuit(0)
