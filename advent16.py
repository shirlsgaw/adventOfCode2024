from typing import Self
from enum import Enum


####
# Direction
####
class Direction(Enum):
  UP = (0, -1)
  DOWN = (0, 1)
  LEFT = (-1, 0)
  RIGHT = (1, 0)


####
# Point
####
class Point:

  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y

  def __repr__(self) -> str:
    return f'Point[({self.x}, {self.y})'

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, Point):
      return False
    return (self.x == other.x and self.y == other.y)

  def __hash__(self) -> int:
    return hash((self.x, self.y))


####
# PathMark
####
class PathMark:

  def __init__(self, point: Point, previous: Self, direction):
    self.point = point
    self.previous = previous
    self.direction = direction

  def __repr__(self) -> str:
    return f'PathMark[point=({self.point.x}, {self.point.y}) previous={self.previous.point} direction={self.direction}]'

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, PathMark):
      return False
    return (self.point == other.point)

  def __hash__(self) -> int:
    return hash((self.point.x, self.point.y))


####
# Maze
####
class Maze:

  def __init__(self, original: list[str]):
    self.original = original
    self.walls, self.start, self.end = self.parse_map(original)

  ####
  # Break the map into the locations of walls as well as the start and end points
  ####
  def parse_map(
      self, original: list[str]
  ) -> tuple[set[tuple[int, int]], tuple[int, int], tuple[int, int]]:
    walls = set[tuple[int, int]]()
    start = None
    end = None
    for y, line in enumerate(original):
      for x, char in enumerate(line):
        if char == '#':
          walls.add((x, y))
        elif char == 'S':
          start = (x, y)
        elif char == 'E':
          end = (x, y)
    if start is None or end is None:
      raise ValueError(f'Invalid map, start={start} end={end}')
    return walls, start, end

  ####
  # Draw the map
  ####
  def draw(self):
    #print(f'Robot expected location: {self.robot}')
    for y in range(0, len(self.original)):
      row = ''
      for x in range(0, len(self.original[y])):
        if (x, y) in self.walls:
          row += '#'
        elif (x, y) == self.start:
          row += 'S'
        elif (x, y) == self.end:
          row += 'E'
        else:
          row += '.'
      print(row)


####
# readlines: reads input from file into lines of strings
####
def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


####
# Main
####
input = readlines('hint.txt')
maze = Maze(input)
maze.draw()
