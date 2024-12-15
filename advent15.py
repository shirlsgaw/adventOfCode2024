from collections import Counter
from collections.abc import Generator
import re
from enum import Enum
import time


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
  ) -> tuple[set[tuple[int, int]], set[tuple[int, int]], tuple[int, int]]:
    walls = set[tuple[int, int]]()
    boxes = set[tuple[int, int]]()
    robot = tuple[int, int]()
    for y, line in enumerate(original):
      for x, char in enumerate(line):
        if char == '#':
          walls.add((x, y))
        elif char == 'O':
          boxes.add((x, y))
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
        if (x, y) in self.boxes:
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
    if (new_x, new_y) in self.boxes:
      potential_x = new_x
      potential_y = new_y
      while (potential_x, potential_y) in self.boxes:
        potential_x += direction[0]
        potential_y += direction[1]

      # Can't move the box into an empty space therefore, we can't move the robot
      if (potential_x, potential_y) in self.walls:
        #print('...Can\'t move the box')
        return
      # Replace location of box into the space found
      self.boxes.remove((new_x, new_y))
      self.boxes.add((potential_x, potential_y))
      #print(f'...Moved box to ({potential_x},{potential_y})')
    if (new_x, new_y) in self.walls:
      #print('..Location in walls')
      return
    if (new_x, new_y) in self.boxes:
      #print('..Location still in boxes')
      return
    self.robot = (new_x, new_y)
    #print(f'...Moved robot to ({self.robot[0]}, {self.robot[1]})')

  ####
  # Compute the sum of all box Goods Positioning System coordiante
  def sum_box_coordinates(self) -> int:
    sum = 0
    for (bx, by) in self.boxes:
      sum += bx + by * 100
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
input = readlines('sample.txt')
warehouse = Warehouse(input)

instructions = list[str]()
for line in input:
  if line.startswith('#'):
    continue
  if len(line) == 0:
    continue
  instructions.append(line)
warehouse.draw()

for line in instructions:
  for move in line:
    direction = get_direction(move)
    warehouse.move_robot(direction)
warehouse.draw()
sum = warehouse.sum_box_coordinates()
print(f'Sum of box coordinates: {sum}')
