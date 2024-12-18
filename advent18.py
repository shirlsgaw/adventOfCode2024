from typing import Self
from enum import Enum
from heapq import heappush
from heapq import heappop
from dataclasses import dataclass, field
import re


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
# PathMark
####
@dataclass(order=True)
class PathMark:
  point: Point = field(compare=False)
  direction: Direction = field(compare=False)
  previous: Self | None = field(compare=False)
  cost: int = field(compare=True)

  def __init__(self,
               point: Point,
               previous: Self | None,
               direction: Direction,
               cost: int = 0):
    self.point = point
    self.previous = previous
    self.direction = direction
    self.cost = cost

  def __repr__(self) -> str:
    return f'PathMark[point=({self.point.x}, {self.point.y}) previous={self.previous} direction={self.direction} cost={self.cost}]'

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, PathMark):
      return False
    return (self.point == other.point)

  def __hash__(self) -> int:
    return hash((self.point.x, self.point.y))


####
# MemorySpace
####
class MemorySpace:

  def __init__(self,
               original: list[str],
               width: int = 70,
               max_falling: int = 1024):
    self.original = original
    self.byte_positions = self.parse_positions(original)
    self.width = width
    self.max_falling = max_falling

  def parse_positions(self, original: list[str]) -> list[Point]:
    byte_positions = list[Point]()
    for line in original:
      matches = re.findall(r'(\d+),(\d+)', line)
      if len(matches) > 0:
        match = matches[0]
        x = int(match[0])
        y = int(match[1])
        byte_positions.append(Point(x, y))
    return byte_positions

  ####
  # Draw the map
  ####
  def draw(self, points: set[Point] = set[Point]()):
    for y in range(0, self.width):
      row = ''
      for x in range(0, self.width):
        p = Point(x, y)
        if p not in self.byte_positions:
          row += '.'
        else:
          found_index = self.byte_positions.index(p)
          if found_index < self.max_falling:
            row += '#'
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
input = readlines('sample.txt')
memory_space = MemorySpace(input, width=6, max_falling=12)
memory_space.draw()
