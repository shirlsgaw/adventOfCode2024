from collections import Counter
import re
from enum import Enum

from numpy import quantile

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
# Computes a safety number from the given headquarters and robot locations
####
def compute_safety(headquarters: Headquarters,
                   locations: list[tuple[int, int]]) -> int:
  quadrant_list = list[Quadrant]()
  for (x, y) in locations:
    quadrant = headquarters.get_quadrant(x, y)
    quadrant_list.append(quadrant)
  quadrant_counter = Counter(quadrant_list)
  safety_number = 1
  for quadrant in quadrant_counter:
    if quadrant != Quadrant.MID:
      safety_number *= quadrant_counter[quadrant]
  return safety_number


####
# Main
####
input = readlines('sample.txt')

robots = list[Robot]()
for line in input:
  robot = parse(line)
  robots.append(robot)

# TODO(sgaw): change to (101, 103)
ebhq = Headquarters(width=11, height=7, robots=robots)
s = 100
#print(f'After {s} seconds:')
robot_locations = ebhq.simulate(seconds=s)
#draw(ebhq, robot_locations)
safety = compute_safety(ebhq, robot_locations)
print(f'Safety number: {safety}')
