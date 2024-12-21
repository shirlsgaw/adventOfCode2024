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
    return f'Point({self.x}, {self.y})'

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, Point):
      return False
    return (self.x == other.x and self.y == other.y)

  def __hash__(self) -> int:
    return hash((self.x, self.y))


####
# Node
####
class Node:

  def __init__(self, point: Point, parent: Self | None):
    self.point = point
    self.parent = parent


####
# Racetrack
####
class Racetrack:

  def __init__(self, original: list[str]) -> None:
    self.original = original
    self.walls = set[Point]()
    self.start = None
    self.end = None
    for y, row in enumerate(original):
      for x, cell in enumerate(row):
        if cell == '#':
          self.walls.add(Point(x, y))
        if cell == 'S':
          self.start = Point(x, y)
        if cell == 'E':
          self.end = Point(x, y)
    if self.start is None:
      raise Exception('No start')
    if self.end is None:
      raise Exception('No end')

  def draw(self) -> None:
    for y in range(0, len(self.original)):
      row = ''
      for x in range(0, len(self.original[y])):
        if Point(x, y) in self.walls:
          row += '#'
        elif Point(x, y) == self.start:
          row += 'S'
        elif Point(x, y) == self.end:
          row += 'E'
        else:
          row += '.'
      print(row)

  def find_path(self) -> list[Point]:
    # BFS
    queue = list[Node]()
    queue.append(Node(self.start, None))
    visited = set[Point]()
    visited.add(self.start)
    while len(queue) > 0:
      current = queue.pop(0)
      if current.point == self.end:
        path = list[Point]()
        tmp = current
        while tmp is not None:
          path.append(tmp.point)
          tmp = tmp.parent
        path.reverse()
        return path
      else:
        for direction in Direction:
          next_point = Point(current.point.x + direction.value[0],
                             current.point.y + direction.value[1])
          if next_point not in visited and next_point not in self.walls:
            visited.add(next_point)
            queue.append(Node(next_point, current))
    return []


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

input = readlines('sample.txt')
racetrack = Racetrack(input)
racetrack.draw()
path = racetrack.find_path()
cost = len(path) - 1
print(f'Cost = {cost}')
