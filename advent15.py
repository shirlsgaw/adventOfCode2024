from collections import Counter
from collections.abc import Generator
import re
from enum import Enum
import time


####
# Box
####
class Box:

  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y

  def __repr__(self) -> str:
    return f'Box({self.x}, {self.y})'

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, Box):
      return False
    return (self.x == other.x and self.y == other.y)

  def __hash__(self) -> int:
    return hash((self.x, self.y))

  def contains_point(self, x: int, y: int) -> bool:
    return self.x == x and self.y == y


####
# Warehouse
####
class Warehouse:

  def __init__(self, original: list[str]):
    self.original = original
    self.walls, self.boxes, self.robot = self.parse_map(original)

  ####
  # Break the map into the locations of walls, boxes, and the robot
  ####
  def parse_map(
      self, original: list[str]
  ) -> tuple[set[tuple[int, int]], set[Box], tuple[int, int]]:
    walls = set[tuple[int, int]]()
    boxes = set[Box]()
    robot = tuple[int, int]()
    for y, line in enumerate(original):
      for x, char in enumerate(line):
        if char == '#':
          walls.add((x, y))
        elif char == 'O':
          boxes.add(Box(x, y))
        elif char == '@':
          robot = (x, y)
    return walls, boxes, robot

  ####
  # Draw the map
  ####
  def draw(self):
    #print(f'Robot expected location: {self.robot}')
    for y in range(0, len(self.original)):
      row = ''
      for x in range(0, len(self.original[y])):
        if self.original[y][0] != '#':
          continue
        b = Box(x, y)
        if b in self.boxes:
          row += 'O'
        elif (x, y) in self.walls:
          row += '#'
        elif (x, y) == self.robot:
          row += '@'
        else:
          row += '.'
      print(row)

  ####
  # Simulate the robot moving
  ####
  def move_robot(self, direction: tuple[int, int]):
    new_x = self.robot[0] + direction[0]
    new_y = self.robot[1] + direction[1]
    #print(f'Moving robot to ({new_x}, {new_y})')

    # Try to move the closest box to an empty space in the same
    # direction as the robot is supposed to move, freeing space
    # for the robot to move
    b = Box(new_x, new_y)
    if b in self.boxes:
      self.move_box(new_x, new_y, direction)

    if (new_x, new_y) in self.walls:
      #print('..Location in walls')
      return
    if b in self.boxes:
      #print('..Location still in boxes')
      return
    self.robot = (new_x, new_y)
    #print(f'...Moved robot to ({self.robot[0]}, {self.robot[1]})')

  ####
  # Attempt to move a box in the direction specified, recursively calling all adjacent
  # blocking boxs until the box is free (if possible)
  ####
  def move_box(self, bx: int, by: int, direction: tuple[int, int]):
    b = Box(bx, by)
    if b not in self.boxes:
      raise ValueError(f'({bx},{by}) is not a box')
    next_x = bx + direction[0]
    next_y = by + direction[1]
    next_b = Box(next_x, next_y)

    # Can't move box
    if (next_x, next_y) in self.walls:
      return
    if next_b in self.boxes:
      self.move_box(next_x, next_y, direction)
    # The adjacent moves must have been unsuccessful, so we cannot move this box
    if next_b in self.boxes:
      return
    # Move box
    self.boxes.remove(b)
    self.boxes.add(next_b)

  ####
  # Compute the sum of all box Goods Positioning System coordiante
  def sum_box_coordinates(self) -> int:
    sum = 0
    for b in self.boxes:
      sum += b.x + b.y * 100
    return sum


####
# readlines: reads input from file into lines of strings
####
def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


####
# Translate a move into a vector representing the direction of movement
####
def get_direction(move: str) -> tuple[int, int]:
  if move == '<':
    return (-1, 0)
  elif move == '>':
    return (1, 0)
  elif move == '^':
    return (0, -1)
  elif move == 'v':
    return (0, 1)
  raise ValueError(f'Invalid move: {move}')


####
# Main
####
input = readlines('input15.txt')
warehouse = Warehouse(input)

instructions = list[str]()
for line in input:
  if line.startswith('#'):
    continue
  if len(line) == 0:
    continue
  instructions.append(line)
#warehouse.draw()

for line in instructions:
  for move in line:
    direction = get_direction(move)
    warehouse.move_robot(direction)
#warehouse.draw()
sum = warehouse.sum_box_coordinates()
print(f'Sum of box coordinates: {sum}')
