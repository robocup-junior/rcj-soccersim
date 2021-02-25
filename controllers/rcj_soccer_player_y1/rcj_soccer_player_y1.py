import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
from rcj_soccer_player_ros import rcj_soccer_robot

this_robot = MyRobot()
this_robot.run()
