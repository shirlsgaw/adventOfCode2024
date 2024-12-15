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
warehouse = Warehouse(input)
warehouse.draw()
