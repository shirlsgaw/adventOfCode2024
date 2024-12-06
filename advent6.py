from enum import Enum
from typing import Self

Direction = Enum('Direction', [('NORTH', 1), ('EAST', 2), ('SOUTH', 3),
                               ('WEST', 4)])


class GuardLocation:
  x = 0
  y = 0
  direction = Direction.NORTH

  def __init__(self, x, y, direction):
    self.x = x
    self.y = y
    self.direction = direction

  def __str__(self) -> str:
    return f'Guard at {self.x}, {self.y} facing {self.direction}'

  def move(self, lab_map) -> Self:
    has_moved = False
    while not has_moved and not is_outside(self.x, self.y, lab_map):
      #print(self)
      if self.direction == Direction.NORTH:
        if has_block(self.x, self.y - 1, lab_map):
          self.direction = Direction.EAST
        else:
          self.y -= 1
          has_moved = True
      elif self.direction == Direction.EAST:
        if has_block(self.x + 1, self.y, lab_map):
          self.direction = Direction.SOUTH
        else:
          self.x += 1
          has_moved = True
      elif self.direction == Direction.SOUTH:
        if has_block(self.x, self.y + 1, lab_map):
          self.direction = Direction.WEST
        else:
          self.y += 1
          has_moved = True
      else:
        if has_block(self.x - 1, self.y, lab_map):
          self.direction = Direction.NORTH
        else:
          self.x -= 1
          has_moved = True
      
    return self

def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


def find_guard(lab_map):
  for row_index in range(0, len(lab_map)):
    row = lab_map[row_index]
    guard_index = row.find('^')
    if (guard_index > -1):
      return GuardLocation(guard_index, row_index, Direction.NORTH)
    guard_index = row.find('>')
    if (guard_index > -1):
      return GuardLocation(guard_index, row_index, Direction.EAST)
    guard_index = row.find('v')
    if (guard_index > -1):
      return GuardLocation(guard_index, row_index, Direction.SOUTH)
    guard_index = row.find('<')
    if (guard_index > -1):
      return GuardLocation(row_index, guard_index, Direction.WEST)

def mark_guard(guard, lab_map):
  row = lab_map[guard.y]
  tmp = row[0:guard.x] + 'X' + row[guard.x + 1:]
  lab_map[guard.y] = tmp
  return lab_map

def debug_map(lab_map):
  for row in lab_map:
    print(row)
  print()

def has_block(x, y, lab_map):
  if is_outside(x, y, lab_map):
    return False
  row = lab_map[y]
  # print(f' row {row}')
  return y < len(row) and row[x] == '#'

def is_outside(x, y, lab_map):
  return x < 0 or x >= len(lab_map[0]) or y  < 0 or y >= len(lab_map)

####
# Main
####
inputs = readlines('sample.txt')

guard = find_guard(inputs)
mark_guard(guard, inputs)

while not is_outside(guard.x, guard.y, inputs):
  guard = guard.move(inputs)
  if not is_outside(guard.x, guard.y, inputs):
    mark_guard(guard, inputs)
    debug_map(inputs)

