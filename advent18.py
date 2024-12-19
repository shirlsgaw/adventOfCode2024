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
  previous: Self | None = field(compare=False)
  cost: int = field(compare=True)

  def __init__(self, point: Point, previous: Self | None, cost: int):
    self.point = point
    self.previous = previous
    self.cost = cost

  def __repr__(self) -> str:
    return f'PathMark[point=({self.point.x}, {self.point.y}) cost={self.cost}]'

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, PathMark):
      return False
    return (self.point == other.point) and (self.cost == other.cost)

  def __hash__(self) -> int:
    return hash((self.point.x, self.point.y, self.cost))


####
# MemorySpace
####
class MemorySpace:

  def __init__(self, original: list[str], width: int = 71):
    self.original = original
    self.byte_positions = self.parse_positions(original)
    self.width = width
    self.cost_cache = dict[Point, int]()
    self.path_cache = dict[Point, list[PathMark]]()

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
  def draw(
      self,
      max_falling: int,
      points: set[Point] = set[Point](),
      path: list[PathMark] = list[PathMark](),
  ):
    visited_points = [pm.point for pm in path]
    for y in range(0, self.width):
      row = ''
      for x in range(0, self.width):
        p = Point(x, y)
        if p in visited_points:
          row += 'O'
        elif p not in self.byte_positions:
          row += '.'
        else:
          found_index = self.byte_positions.index(p)
          if found_index < max_falling:
            row += '#'
          else:
            row += '.'
      print(row)

  ####
  # cost
  ####
  def cost(self, path_mark: PathMark, direction: Direction) -> int:
    cost = path_mark.cost + 1
    return cost

  ####
  # Find maximum bytes that can fall while still being able to have a path between (0, 0) and (width - 1, width - 1)
  ####
  def find_max_falling(self) -> int:
    test_max = len(self.byte_positions) - 1

    while test_max > 1024:
      test_max -= 1

      self.cost_cache.clear()
      start = PathMark(Point(0, 0), None, 0)
      self.cost_cache[start.point] = start.cost
      path, cost = self.find_path([start], test_max)
      if len(path) > 0:
        return test_max
    raise Exception('Could not find a higher position than part 1')

  ####
  # Find a path between (0, 0) and (width - 1 , width - 1)
  ####
  def find_path(self, starts: list[PathMark],
                max_falling: int) -> tuple[list[PathMark], int]:
    priority_queue = list[PathMark]()
    directions = [
        Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT
    ]

    for start in starts:
      heappush(priority_queue, start)

    path_end = None
    while len(priority_queue) > 0:
      item = heappop(priority_queue)
      #print(f'. Current item: {item}')
      if item.point == Point(self.width - 1, self.width - 1):
        path_end = item
        break

      # Check if this item is a duplicate and we've found a lower cost
      # way to reach this point
      if self.cost_cache[item.point] < item.cost:
        #print(f'.  found lower cost way to {item.point}')
        continue

      for direction in directions:
        x = item.point.x + direction.value[0]
        y = item.point.y + direction.value[1]
        p = Point(x, y)
        #print(f'. Checking point {p}')
        if x < 0 or x >= self.width or y < 0 or y >= self.width:
          continue

        neighbors = self.path_cache.get(p, list[PathMark]())
        neighbors.append(item)

        if p in self.byte_positions and self.byte_positions.index(
            p) < max_falling:
          #print(f'.  {p} is a byte')
          continue

        cost = self.cost(item, direction)
        # Allow duplicate path points if the cost of the new path is lower
        if p not in self.cost_cache or self.cost_cache[p] > cost:
          path_mark = PathMark(p, item, cost=cost)
          #print(f'. Adding to priority queue {path_mark.point}, cost={cost}')
          self.cost_cache[p] = cost
          heappush(priority_queue, path_mark)

    path = list[PathMark]()
    curr = path_end
    #print(f'Found path: end={path_end}')
    while curr is not None:
      path.append(curr)
      curr = curr.previous
    cost = -1
    if path_end is not None:
      cost = path_end.cost
    path.reverse()
    #points = [pm.point for pm in path]
    #print(f'Found path: {points}')
    return (path, cost)


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
input = readlines('input18.txt')

max_falling = 1024
memory_space = MemorySpace(input)  #, width=7, max_falling=max_falling)
byte_index = memory_space.find_max_falling()
#memory_space.draw(max_falling=max_falling, path=path)
print(f'Max falling bytes: {memory_space.byte_positions[byte_index]}')
