import json
from pathlib import Path
from datetime import datetime
from typing import Optional


class JSONLogger(object):
    def __init__(self, logfile: Path):

        self.logfile = logfile

    def event(self,
              supervisor,  # Supervisor from supervisor.py
              type: str,
              msg: str,
              robot: Optional[str] = None,
              team: Optional[str] = None,
              payload: Optional[dict] = None):

        matchtime = supervisor.match_time - supervisor.time
        data = {
            "datetime": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "matchtime": matchtime,
            "event": type,
            "msg": msg
        }

        if robot is not None:
            data['robot'] = robot
            data['team'] = supervisor.robot_to_team_name(robot)

        if team is not None:
            data['team'] = team

        if payload is not None:
            data['payload'] = payload

        with self.logfile.open('a') as outfile:
            json.dump(data, outfile)
            outfile.write('\n')
