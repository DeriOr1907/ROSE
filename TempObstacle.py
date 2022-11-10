from TernaryTree import *
from rose.common import obstacles, actions  # NOQA

side_obstacles = (obstacles.WATER, obstacles.CRACK)  # only they take off points by crossing
obstacles_dict = {obstacles.NONE: 0,
                  obstacles.TRASH: -10,
                  obstacles.BIKE: -10,
                  obstacles.BARRIER: -10,
                  obstacles.CRACK: 5,
                  obstacles.WATER: 4,
                  obstacles.PENGUIN: 10}


class TempObstacle:
    def __init__(self, x, y, world):
        self.x = x
        self.o = world.get((x, y))
        self.points = obstacles_dict[self.o]

    def set_points(self):
        """ if the obstacle is not in the middle, set right points values """
        self.points = 0
        if self.o in side_obstacles:
            self.points = -10

    def finish_line(self, tree_level):
        """ if the obstacle is beyond the finish line -> ignore it """
        if TernaryTree.steps - tree_level < 0:
            self.points = 0
