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

CENTER_NS = "center_ns"
YELLOW_LEFT_NS = "yellow_left_ns"
YELLOW_MIDDLE_NS = "yellow_middle_ns"
YELLOW_RIGHT_NS = "yellow_right_ns"
BLUE_LEFT_NS = "blue_left_ns"
BLUE_MIDDLE_NS = "blue_middle_ns"
BLUE_RIGHT_NS = "blue_right_ns"
NEUTRAL_SPOTS = {
   CENTER_NS : (0, 0),
   YELLOW_LEFT_NS : (-0.3, -0.3),
   YELLOW_MIDDLE_NS : (-0.2, 0),
   YELLOW_RIGHT_NS : (-0.3, 0.3),
   BLUE_LEFT_NS : (0.3, 0.3),
   BLUE_MIDDLE_NS : (0.2, 0),
   BLUE_RIGHT_NS : (0.3, -0.3),
}
