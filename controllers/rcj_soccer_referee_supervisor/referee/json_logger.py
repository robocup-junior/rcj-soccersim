import json
from pathlib import Path
from datetime import datetime
from typing import Optional


class JSONLogger(object):
    def __init__(self, logfile: Path):
        self.logfile = logfile

    def event(
        self,
        supervisor,  # Supervisor from supervisor.py
        type: str,
        msg: str,
        robot_name: Optional[str] = None,
        team: Optional[str] = None,
        payload: Optional[dict] = None,
    ):
        matchtime = supervisor.match_time - supervisor.time
        data = {
            "datetime": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "matchtime": matchtime,
            "event": type,
            "msg": msg
        }

        if robot_name is not None:
            data['robot'] = robot_name
            data['team'] = supervisor.robot_name_to_team_name(robot_name)

        if team is not None:
            data['team'] = team

        if payload is not None:
            data['payload'] = payload

        with self.logfile.open('a') as outfile:
            json.dump(data, outfile)
            outfile.write('\n')
