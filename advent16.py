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
# VisitedMark: Same as a PathMark but tracks all potential neighbors leading to this one with
# the same cost.
####
@dataclass(order=True)
class VisitedMark:
  point: Point = field(compare=False)
  paths: list[PathMark] = field(compare=False)
  cost: int = field(compare=True)

  def __init__(self,
               point: Point,
               paths: list[PathMark] = list[PathMark](),
               cost: int = 0):
    self.point = point
    self.paths = paths
    self.cost = cost

  def __repr__(self) -> str:
    return f'VisitedMark[point=({self.point.x}, {self.point.y}) cost={self.cost}]'

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, VisitedMark):
      return False
    return (self.point == other.point) and (self.cost == other.cost)

  def __hash__(self) -> int:
    return hash((self.point.x, self.point.y, self.cost))


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
  def draw(self,
           path: list[PathMark] = list[PathMark](),
           points: set[Point] = set[Point]()):
    path_dict = dict[Point, PathMark]()
    for mark in path:
      path_dict[mark.point] = mark
    for y in range(0, len(self.original)):
      row = ''
      for x in range(0, len(self.original[y])):
        p = Point(x, y)
        if p in self.walls:
          row += '#'
        elif p in points:
          row += 'O'
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
  # Cost from going from the current position in the direction specified
  ####
  def cost(self, item: PathMark, direction: Direction) -> int:
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
    return cost

  ####
  # Find path between and the start and end with the cost of the path
  ####
  def find_path(
      self, visited_cost: dict[Point, int] = dict[Point, int]()
  ) -> tuple[list[PathMark], int]:
    priority_queue = list[PathMark]()
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

        cost = self.cost(item, direction)
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
  # Mark all points that can be discovered on a path with a cost
  # equal to the submitted point_cost dictionary
  ####
  def mark_paths(self, max_cost: int) -> set[Point]:
    priority_queue = list[VisitedMark]()
    directions = [
        Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT
    ]
    visited_cost = dict[Point, int]()

    priority_queue.append(
        VisitedMark(self.start,
                    paths=[PathMark(self.start, None, Direction.RIGHT)]))
    end_mark = None

    while len(priority_queue) > 0:
      item = heappop(priority_queue)
      visited_cost[item.point] = item.cost
      #print(f'. Current item: {item.point}, cost={item.cost}')

      # Stop exploring after we surpass the known optimal path cost
      if item.cost > max_cost:
        break

      if item.point == self.end:
        size = len(item.paths)
        print(
            f'.  found end point {item.point} cost={item.cost}, num_paths={size}'
        )
        if end_mark is None or item.cost < end_mark.cost:
          end_mark = item
          continue

      for direction in directions:
        x = item.point.x + direction.value[0]
        y = item.point.y + direction.value[1]
        p = Point(x, y)
        #print(f'.  Checking point {p}')
        if p in self.walls:
          continue

        # Don't revisit points that have already been visited
        if len(item.paths) > 0:
          parents = [path.point for path in item.paths]
          if p in parents:
            #print(f'.    {p} already visited')
            continue

        for mark in item.paths:
          cost = self.cost(mark, direction)
          if cost > max_cost:
            continue
          if p in visited_cost and visited_cost[p] + 1000 < cost:
            continue
          path_mark = PathMark(p, mark, direction, cost=cost)
          visited_mark = VisitedMark(p, [path_mark], cost=cost)
          if visited_mark not in priority_queue:
            #print(
            #    f'. Adding to priority queue {p}, cost={cost}, direction={direction}'
            #)
            heappush(priority_queue, visited_mark)
          else:
            existing_mark = priority_queue[priority_queue.index(visited_mark)]
            #size = len(existing_mark.paths)
            existing_mark.paths.append(path_mark)
            #print(
            #    f'.  found existing mark {existing_mark.point}, cost={existing_mark.cost}, direction={direction}, size={size}'
            #)

    if end_mark is None:
      raise Exception('Expected to find end mark')
    result = set[Point]()
    for pm in end_mark.paths:
      while pm is not None:
        result.add(pm.point)
        pm = pm.previous
    return result


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
input = readlines('input16.txt')
maze = Maze(input)
path, cost = maze.find_path()
print(f'Path cost: {cost}')
last = path.pop()
path.append(last)
points = maze.mark_paths(last.cost)
#maze.draw(points=points)
size = len(points)
print(f'Number of tiles: {size}')
