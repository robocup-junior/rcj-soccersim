import math


class ProgressChecker:
    def __init__(self, steps: int, threshold: float):
        self.steps = steps
        self.threshold = threshold
        self.reset()

    def reset(self):
        # The array which holds all the samples of deltas for each tick
        self.samples = [0 for _ in range(self.steps)]
        self.iterator = 0
        self.prev_position = None

    def track(self, position):
        """
        Make ProgressChecker react to a new position. Internally, it computes
        the Euclidian distance from the previous position and saves it so that
        it can be used when computing whether the given object has made
        progress.
        """
        # If the track function gets called for the first time (i.e. we do not
        # remember the previous position), store the current position as the
        # previous one
        if not self.prev_position:
            self.prev_position = position
            return

        prev_position = self.prev_position

        delta = math.sqrt((prev_position[0] - position[0]) ** 2 +
                          (prev_position[2] - position[2]) ** 2)

        # store the currently computed delta sample
        self.samples[self.iterator % self.steps] = delta
        self.iterator += 1

        self.prev_position = position

    def is_progress(self, robot=None) -> bool:
        """
        Detect whether the object which is being tracked has made some
        "progress". In other words, check whether we have tracked enough
        movement (more than the threshold) since the last reset.

        Args:
            robot (optional): name of robot, used only for debugging purposes.
        """
        s = sum(self.samples)

        # if robot:
        #     print(f'Robot {robot} iterator: {self.iterator}, '
        #           f's: {s}, thr: {self.threshold}')
        # else:
        #     print(f'iterator: {self.iterator}, s: {s}, '
        #           f'thr: {self.threshold}')

        # We we haven't tracked at least as many samples as the number of
        # steps, our default position is "benefit of doubt": we assume enough
        # progress has been made.
        if self.iterator < self.steps:
            return True

        return s >= self.threshold
