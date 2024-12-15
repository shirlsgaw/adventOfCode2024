from collections import Counter
from collections.abc import Generator
import re
from enum import Enum
import time

Quadrant = Enum('Quadrant', [('MID', 0), ('NW', 1), ('NE', 2), ('SW', 3),
                             ('SE', 4)])


####
# Robot
####
class Robot:

  def __init__(self, x: int, y: int, vx: int, vy: int):
    self.x = x
    self.y = y
    self.vx = vx
    self.vy = vy

  def __repr__(self) -> str:
    return f'Robot(({self.x}, {self.y}), v=({self.vx}, {self.vy}))'

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, Robot):
      return False
    return (self.x == other.x and self.y
            == other.y) and (self.vx == self.vy and self.vy == other.vy)

  def __hash__(self) -> int:
    return hash((self.x, self.y, self.vx, self.vy))


####
# Headquarters
####
class Headquarters:

  def __init__(self, width: int, height: int, robots: list[Robot]):
    self.width = width
    self.height = height
    self.robots = robots

  def __repr__(self) -> str:
    return f'Headquarters({self.width}x{self.height}, {self.robots})'

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, Headquarters):
      return False
    return (self.width == other.width
            and self.height == other.height) and (self.robots == other.robots)

  def __hash__(self) -> int:
    return hash((self.width, self.height, self.robots))

  def simulate(self, seconds: int) -> list[tuple[int, int]]:
    result = list[tuple[int, int]]()
    for robot in self.robots:
      location_x = (robot.x + robot.vx * seconds) % self.width
      location_y = (robot.y + robot.vy * seconds) % self.height
      result.append((location_x, location_y))
    return result

  def get_quadrant(self, x: int, y: int) -> Quadrant:
    mid_vertical = int(self.width / 2)
    mid_horizontal = int(self.height / 2)

    if x == mid_vertical:
      return Quadrant.MID
    elif y == mid_horizontal:
      return Quadrant.MID
    else:
      if x < mid_vertical:
        if y < mid_horizontal:
          return Quadrant.NW
        else:
          return Quadrant.SW
      else:
        if y < mid_horizontal:
          return Quadrant.NE
        else:
          return Quadrant.SE


####
# readlines: reads input from file into lines of strings
####
def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


####
# parse: parses string into a robot
####
def parse(line: str) -> Robot:
  matches = re.findall(r'p=(\d+),(\d+) v=(.+),(.+)', line)
  if len(matches) == 1 and len(matches[0]) == 4:
    match = matches[0]
    return Robot(x=int(match[0]),
                 y=int(match[1]),
                 vx=int(match[2]),
                 vy=int(match[3]))
  raise ValueError(f'Invalid line: {line}')


####
# draw
####
def draw(headquarters: Headquarters, locations: list[tuple[int, int]]):
  counter = Counter(locations)
  for y in range(0, headquarters.height):
    row = ''
    for x in range(0, headquarters.width):
      if (x, y) in counter:
        row += str(counter[(x, y)])
      else:
        row += '.'
    print(row)


####
# Find all points that are in the same region as (x, y)
####
directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]


def get_region(x: int, y: int,
               location_set: set[tuple[int, int]]) -> list[tuple[int, int]]:
  explored = set[tuple[int, int]]()
  horizon = list[tuple[int, int]]()
  horizon.append((x, y))
  region = list[tuple[int, int]]()
  while len(horizon) > 0:
    (x, y) = horizon.pop()
    if (x, y) in explored:
      continue
    explored.add((x, y))
    region.append((x, y))
    for (dx, dy) in directions:
      next_x = x + dx
      next_y = y + dy
      next = (next_x, next_y)
      if next in location_set and next not in explored:
        horizon.append((next_x, next_y))
  return region


####
# Region size count
####
def count_region_sizes(headquarters: Headquarters,
                       location_set: set[tuple[int, int]]) -> dict[int, int]:
  visited = set[tuple[int, int]]()
  region_id = 0
  regions = dict[int, int]()
  for (lx, ly) in location_set:
    if (lx, ly) in visited:
      continue
    visited.add((lx, ly))

    region_locations = get_region(lx, ly, location_set)
    visited.update(region_locations)

    regions[region_id] = len(region_locations)
    region_id += 1
  return regions


####
# Count the number of points that have the same x value and repeat for y values
####
def count_x_and_y(
    headquarters: Headquarters,
    robot_locations: list[tuple[int,
                                int]]) -> tuple[Counter[int], Counter[int]]:
  x_list = list[int]()
  y_list = list[int]()
  for (rx, ry) in robot_locations:
    x_list.append(rx)
    y_list.append(ry)
  return Counter(x_list), Counter(y_list)


####
# Main
####
input = readlines('input14.txt')

robots = list[Robot]()
for line in input:
  robot = parse(line)
  robots.append(robot)

# TODO(sgaw): change to (101, 103)
ebhq = Headquarters(width=101, height=103, robots=robots)
s = 100
#print(f'After {s} seconds:')
robot_locations = ebhq.simulate(seconds=s)

for i in range(1, 10_000):
  locations = ebhq.simulate(seconds=i)
  regions_dict = count_region_sizes(ebhq, set(locations.copy()))
  max_region_size = max(regions_dict.values())
  if i % 200 == 0:
    print(f'After {i} seconds: max region size {max_region_size}')
  if max_region_size > 20:
    draw(ebhq, locations)
    print(f'After {i} seconds, max region size: {max_region_size}')
    time.sleep(3)
print('Done')
