from math import ceil
from datetime import datetime
from pathlib import Path, PosixPath

from referee.consts import MATCH_TIME, TIME_STEP
from referee.referee import RCJSoccerReferee


TEAM_YELLOW = "The Yellows"
TEAM_BLUE = "The Blues"


def reflog_path(
    directory: Path,
    team_blue: str,
    team_yellow: str,
) -> PosixPath:
    now_str = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    team_blue = team_blue.replace(' ', '_')
    team_yellow = team_yellow.replace(' ', '_')

    # Ensure the directory ecists
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)

    p = directory / Path(f'{team_blue}_vs_{team_yellow}-{now_str}.jsonl')
    return p


reflog = reflog_path(Path('reflog'), TEAM_BLUE, TEAM_YELLOW)

referee = RCJSoccerReferee(
    match_time=MATCH_TIME,
    progress_check_steps=ceil(15/(TIME_STEP/1000.0)),
    progress_check_threshold=0.5,
    ball_progress_check_steps=ceil(10/(TIME_STEP/1000.0)),
    ball_progress_check_threshold=0.5,
    reflog_path=reflog,
    team_name_blue=TEAM_BLUE,
    team_name_yellow=TEAM_YELLOW,
    penalty_area_allowed_time=15,
    penalty_area_reset_after=2,
)

while referee.step(TIME_STEP) != -1:
    referee.emit_positions()

    if not referee.tick():
        break

# When end of match, pause simulator immediately
referee.simulationSetMode(referee.SIMULATION_MODE_PAUSE)
