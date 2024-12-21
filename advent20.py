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
    self.cost_cache = dict[Point, int]()
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
    self.cost_cache[self.start] = 0
    if self.end is None:
      raise Exception('No end')

  def draw(self, point: Point | None = None) -> None:
    for y in range(0, len(self.original)):
      row = ''
      for x in range(0, len(self.original[y])):
        if Point(x, y) == point:
          row += '1'
        elif Point(x, y) in self.walls:
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
            self.cost_cache[next_point] = self.cost_cache[current.point] + 1
    return []

  ####
  # Satifies cheat conditions
  ####
  def is_valid_cheat(self, begin: Point, end: Point, candidate: Point,
                     steps: int) -> bool:
    if candidate not in self.walls:
      return False
    cost_begin = self.cost_cache[begin]
    cost_end = self.cost_cache[end]
    diff = cost_end - cost_begin - 2
    return diff >= steps

  ####
  # find walls to remove that would shorten the path by N steps
  ####
  def find_cheats(self, path: list[Point], steps: int) -> list[Point]:
    potential_cheats = list[Point]()
    for i in range(0, len(path) - 1):
      for j in range(i + 1, len(path)):
        delta_x = path[j].x - path[i].x
        delta_y = path[j].y - path[i].y
        if delta_x == 0 and delta_y * delta_y == 4:
          candidate = Point(path[i].x, path[i].y + delta_y // 2)
          if self.is_valid_cheat(path[i], path[j], candidate, steps):
            potential_cheats.append(candidate)
        elif delta_y == 0 and delta_x * delta_x == 4:
          candidate = Point(path[i].x + delta_x // 2, path[i].y)
          if self.is_valid_cheat(path[i], path[j], candidate, steps):
            potential_cheats.append(candidate)
    return potential_cheats


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

input = readlines('input20.txt')
racetrack = Racetrack(input)
#racetrack.draw()
original_path = racetrack.find_path()
cost = len(original_path) - 1
print(f'Original cost = {cost}')

saves = []#20, 38, 64]
for save in saves:
  cheats = racetrack.find_cheats(original_path, save)
  print(f'Cheats for {save} steps: {cheats}')
  for cheat in cheats:
    print(f'. Save: {save}, Cheat: {cheat}')
    #racetrack.draw(point=cheat)

# Part 1: find all cheats >= 100
cheats = racetrack.find_cheats(original_path, 100)
num_cheats = len(cheats)
print(f'Part 1: {num_cheats}')
