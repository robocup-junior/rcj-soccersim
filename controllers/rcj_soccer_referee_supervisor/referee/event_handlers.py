import json
from datetime import datetime
from pathlib import Path
from typing import Optional


class EventHandler:
    def __init__(self):
        pass

    def handle(
        self,
        referee,  # Referee from referee.py
        type: str,
        payload: Optional[dict] = None,
    ):
        """Handle the incoming event

        Args:
            referee (RCJSoccerReferee): Instance of Referee
            type (str): Event type
            payload (dict, optional): More information about the event
        """
        raise NotImplementedError


class JSONLoggerHandler(EventHandler):
    """Handler for writing data to json file."""

    def __init__(self, logfile: Path):
        super().__init__()
        self.logfile = logfile

    def handle(self, referee, type: str, payload: Optional[dict] = None):
        matchtime = referee.match_time - referee.time
        data = {
            "datetime": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "matchtime": matchtime,
            "event": type,
        }

        if payload is not None:
            data["payload"] = payload

        with self.logfile.open("a") as outfile:
            json.dump(data, outfile)
            outfile.write("\n")


class DrawMessageHandler(EventHandler):
    """Handler for creating the message which is drawn onto world window."""

    def create_inside_penalty_for_too_long_msg(
        self,
        robot_name: str,
        **kwargs,
    ) -> str:
        return f"Robot {robot_name}: Inside penalty for too long."

    def create_lack_of_progress_msg(
        self,
        type: str,
        robot_name: Optional[str] = None,
        **kwargs,
    ) -> str:
        if type == "ball":
            return "Ball: Lack of progress."
        return f"Robot {robot_name}: Lack of progress."

    def create_goal_msg(self, team_name: str, **kwargs) -> str:
        return f"A goal was scored by {team_name}."

    def create_kickoff_msg(self, robot_name: str, **kwargs) -> str:
        return f"Robot {robot_name} is kicking off."

    def create_match_start_msg(self, total_match_time: int, **kwargs) -> str:
        return f"The match ({total_match_time}s) has started."

    def create_match_finish_msg(self, total_match_time: int, **kwargs) -> str:
        return f"The match time {total_match_time}s is over."

    def handle(self, referee, type: str, payload: Optional[dict] = None):
        # Call formatter based on event type.
        msg_formatter = getattr(self, f"create_{type.lower()}_msg")
        data = payload if payload is not None else {}
        message = msg_formatter(**data)
        referee.add_event_message_to_queue(message)
