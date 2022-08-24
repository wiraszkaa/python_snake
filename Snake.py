from enum import Enum
import numpy as np


class Direction(Enum):
    UP = -1
    DOWN = 1
    LEFT = -2
    RIGHT = 2


class Segment:
    def __init__(self, pos, command: int):
        self.pos = pos
        self.command = command


class Move:
    def __init__(self, direction: Direction, pos):
        self.pos = pos
        self.direction = direction


class Snake:
    def __init__(self, bounds: tuple):
        self.bounds = bounds
        self.body = []
        self.head = None
        self.direction = None
        self.moves = []
        self.respawn()

    def respawn(self):
        self.body = []
        self.head = Segment(np.array([32.0, 32.0], dtype=float), 0)
        self.direction = Direction.RIGHT
        self.moves = [Move(self.direction, np.copy(self.head.pos))]

    def change_direction(self, direction: Direction):
        change = False
        match direction:
            case Direction.UP:
                if self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                    change = True
            case Direction.DOWN:
                if self.direction != Direction.UP:
                    self.direction = Direction.DOWN
                    change = True
            case Direction.LEFT:
                if self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                    change = True
            case _:
                if self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                    change = True
        if change:
            self.moves.append(Move(self.direction, self.head.pos))
            self.head.command += 1

    def move(self, distance: float):
        self.head.pos = change_pos(self.head.pos, self.direction, distance)
        for segment in self.body:
            self.move_segment(segment, distance)

    def move_segment(self, segment: Segment, distance: float):
        command = self.moves[segment.command]

        finish_pos = None
        if segment.command + 1 < len(self.moves):
            finish_pos = self.moves[segment.command + 1].pos
        segment.pos = change_pos(segment.pos, command.direction, distance)
        if (segment.pos == finish_pos).all():
            segment.command += 1

    def add_segment(self):
        last = self.head
        if len(self.body) > 0:
            last = self.body[-1]
        self.body.append(Segment(change_pos(last.pos, self.moves[last.command].direction, -64), last.command))


def change_pos(pos, direction: Direction, distance: float):
    pos = np.copy(pos)
    match direction:
        case Direction.UP:
            pos[1] -= distance
            pos[1] = round(pos[1], 2)
            return pos
        case Direction.DOWN:
            pos[1] += distance
            pos[1] = round(pos[1], 2)
            return pos
        case Direction.LEFT:
            pos[0] -= distance
            pos[0] = round(pos[0], 2)
            return pos
        case _:
            pos[0] += distance
            pos[0] = round(pos[0], 2)
            return pos
