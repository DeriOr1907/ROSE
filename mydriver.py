"""
NonRandom driver
"""

import random
from typing import Union
from TempObstacle import *
from rose.common import obstacles, actions  # NOQA


driver_name = "LI OR I"


def build_tree(tree: Union["TernaryTree", None], x, y, road, world, tree_level):
    if tree is not None and tree_level < 6:  # until the end of the road
        if x == road + 2:  # right lane
            right_root = None
        else:
            right_root = TernaryTree(TempObstacle(x + 1, y - 1, world))
            right_root.value.set_points()
            right_root.value.finish_line(tree_level)

        if x == road:  # left lane
            left_root = None
        else:
            left_root = TernaryTree(TempObstacle(x - 1, y - 1, world))
            left_root.value.set_points()
            left_root.value.finish_line(tree_level)

        middle_root = TernaryTree(TempObstacle(x, y - 1, world))
        middle_root.value.finish_line(tree_level)

        if tree_level == 0:
            value = TempObstacle(x, y, world)
            tree = TernaryTree(value, left_root, middle_root, right_root)
        else:
            tree.set_children(left_root, middle_root, right_root)

        build_tree(tree.left, x - 1, y - 1, road, world, tree_level + 1)
        build_tree(tree.middle, x, y - 1, road, world, tree_level + 1)
        build_tree(tree.right, x + 1, y - 1, road, world, tree_level + 1)
    return tree


def max_path(tree: Union["TernaryTree", None]):
    if tree is None:  # it means that the turn is not valid
        return -100  # to make sure it stays on the same road
    if tree.is_leaf():  # the edge of the visible road
        return tree.value.points
    return tree.value.points + max(max_path(tree.left), max_path(tree.middle), max_path(tree.right))


def best_move(tree: Union["TernaryTree", None]):
    """
    returns the best move there is to take
    """
    left = max_path(tree.left)  # the maximum points it is possible to earn by turning left
    middle = max_path(tree.middle)  # the maximum by staying in the middle
    right = max_path(tree.right)  # the maximum by turning right

    if left < right > middle:
        return actions.RIGHT
    if middle < left > right:
        return actions.LEFT
    if right == left > middle:
        return random.choice([actions.LEFT, actions.RIGHT])
    return None  # to decide which action needed


def left_or_right(x, road):  # in case both have the same amount points and middle is not clear
    if x == road + 2:
        return actions.LEFT
    if x == road:
        return actions.RIGHT
    return random.choice([actions.LEFT, actions.RIGHT])


def drive(world):
    if TernaryTree.steps == 0:  # last game ended
        TernaryTree.steps = 60  # reset steps
    TernaryTree.steps -= 1

    x = world.car.x
    y = world.car.y

    road = 0
    if 3 <= x:
        road = 3

    tree = TernaryTree(0)
    tree = build_tree(tree, x, y, road, world, 0)  # contains all possible turns and obstacles values

    if best_move(tree) is not None:
        return best_move(tree)

    obstacle = world.get((x, y - 1))
    if obstacle == obstacles.PENGUIN:
        return actions.PICKUP
    if obstacle == obstacles.WATER:
        return actions.BRAKE
    if obstacle == obstacles.CRACK:
        return actions.JUMP
    if obstacle != obstacles.NONE:
        return left_or_right(x, road)
    return actions.NONE
