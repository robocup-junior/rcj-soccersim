import math


class ProgressChecker(object):
    def __init__(self,
                 steps: int,
                 threshold: float):
        self.steps = steps
        self.threshold = threshold
        self.prev_position = None
        self.reset()

    def reset(self):
        self.A = [0 for _ in range(self.steps)]
        self.iterator = 0

    def update_position(self, position):
        if not self.prev_position:
            self.prev_position = position
            return

        prev_position = self.prev_position

        delta = math.sqrt((prev_position[0] - position[0]) ** 2 +
                          (prev_position[2] - position[2]) ** 2)

        self.A[self.iterator % self.steps] = delta
        self.iterator += 1

        self.prev_position = position

    def is_progress(self, robot=None):
        s = sum(self.A)

        if robot:
            print(f'Robot {robot} iterator: {self.iterator}, '
                  f's: {s}, thr: {self.threshold}')
        else:
            print(f'iterator: {self.iterator}, s: {s}, thr: {self.threshold}')

        if self.iterator < self.steps:
            return True

        return s >= self.threshold
