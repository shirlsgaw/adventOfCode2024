from typing import Self
from enum import Enum
from heapq import heappush
from heapq import heappop
from dataclasses import dataclass, field


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
# Maze
####
class Maze:

  def __init__(self, original: list[str]):
    self.original = original
    self.walls, self.start, self.end = self.parse_map(original)

  ####
  # Break the map into the locations of walls as well as the start and end points
  ####
  def parse_map(self, original: list[str]) -> tuple[set[Point], Point, Point]:
    walls = set[Point]()
    start = None
    end = None
    for y, line in enumerate(original):
      for x, char in enumerate(line):
        if char == '#':
          walls.add(Point(x, y))
        elif char == 'S':
          start = Point(x, y)
        elif char == 'E':
          end = Point(x, y)
    if start is None or end is None:
      raise ValueError(f'Invalid map, start={start} end={end}')
    return walls, start, end

  ####
  # Draw the map
  ####
  def draw(self, path: list[PathMark] = list[PathMark]()):
    path_dict = dict[Point, PathMark]()
    for mark in path:
      path_dict[mark.point] = mark
    for y in range(0, len(self.original)):
      row = ''
      for x in range(0, len(self.original[y])):
        p = Point(x, y)
        if p in self.walls:
          row += '#'
        elif p == self.start:
          row += 'S'
        elif p == self.end:
          row += 'E'
        elif p in path_dict:
          direction = path_dict[p].direction
          if direction is Direction.UP:
            row += '^'
          elif direction is Direction.DOWN:
            row += 'v'
          elif direction is Direction.LEFT:
            row += '<'
          elif direction is Direction.RIGHT:
            row += '>'
        else:
          row += '.'
      print(row)

  ####
  # Find path between and the start and end with the cost of the path
  ####
  def find_path(self) -> tuple[list[PathMark], int]:
    print(f'Finding path from {self.start} to {self.end}')
    priority_queue = list[PathMark]()
    visited_cost = dict[Point, int]()
    directions = [
        Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT
    ]

    priority_queue.append(PathMark(self.start, None, Direction.RIGHT))
    visited_cost[self.start] = 0

    path_end = None
    while len(priority_queue) > 0:
      item = heappop(priority_queue)
      #print(f'. Current item: {item}')
      if item.point == self.end:
        path_end = item
        break

      # Check if this item is a duplicate and we've found a lower cost
      # way to reach this point
      if visited_cost[item.point] < item.cost:
        #print(f'.  found lower cost way to {item.point}')
        continue

      for direction in directions:
        x = item.point.x + direction.value[0]
        y = item.point.y + direction.value[1]
        p = Point(x, y)
        #print(f'. Checking point {p}')
        if p in self.walls:
          #print(f'.  {p} is a wall')
          continue

        cost = item.cost + 1
        delta_x = direction.value[0] - item.direction.value[0]
        sq_x = delta_x * delta_x

        delta_y = direction.value[1] - item.direction.value[1]
        sq_y = delta_y * delta_y

        # 180 degree turn
        if sq_x == 2 or sq_y == 2:
          cost += 2000
        # 90 degree turn
        elif sq_x + sq_y > 0:
          cost += 1000
        # Allow duplicate path points if the cost of the new path is lower
        if p not in visited_cost or visited_cost[p] > cost:
          path_mark = PathMark(p, item, direction, cost=cost)
          #print(f'. Adding to priority queue {path_mark}')
          visited_cost[p] = cost
          heappush(priority_queue, path_mark)

    if path_end is None:
      raise ValueError(f'No path found from {self.start} to {self.end}')
    path = list[PathMark]()
    curr = path_end
    #print(f'Found path: end={path_end}')
    while curr is not None:
      path.append(curr)
      curr = curr.previous
    cost = path_end.cost
    path.reverse()
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
input = readlines('input17.txt')
maze = Maze(input)
path, cost = maze.find_path()
print(f'Path cost: {cost}')
#maze.draw(path=path)
