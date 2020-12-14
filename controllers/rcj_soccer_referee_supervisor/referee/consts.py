MATCH_TIME = 10 * 60  # 10 minutes
GOAL_X_LIMIT = 0.745
TIME_STEP = 64
ROBOT_NAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
N_ROBOTS = len(ROBOT_NAMES)
ROBOT_INITIAL_TRANSLATION = {"B1": [0.3, 0.03817, 0.2],
                             "B2": [0.3, 0.03817, -0.2],
                             "B3": [0.75, 0.03817, 0],
                             "Y1": [-0.3, 0.03817, 0.2],
                             "Y2": [-0.3, 0.03817, -0.2],
                             "Y3": [-0.75, 0.03817, 0]}

ROBOT_INITIAL_ROTATION = {"B1": [0, 1, 0, 1.57],
                          "B2": [0, 1, 0, 1.57],
                          "B3": [0, 1, 0, 3.14],
                          "Y1": [0, 1, 0, 1.57],
                          "Y2": [0, 1, 0, 1.57],
                          "Y3": [0, 1, 0, 3.14]}

BALL_INITIAL_TRANSLATION = [0, 0, 0]
