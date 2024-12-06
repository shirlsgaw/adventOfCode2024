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
    if self.direction == Direction.NORTH:
      if has_block(self.x, self.y + 1, lab_map):
        self.direction = Direction.EAST
      else:
        self.y += 1
    elif self.direction == Direction.EAST:
      if has_block(self.x + 1, self.y, lab_map):
        self.direction = Direction.SOUTH
      else:
        self.x += 1
    elif self.direction == Direction.SOUTH:
      if has_block(self.x, self.y - 1, lab_map):
        self.direction = Direction.WEST
      else:
        self.y -= 1
    else:
      if has_block(self.x - 1, self.y, lab_map):
        self.direction = Direction.NORTH
      else:
        self.x -= 1
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
      return (row_index, guard_index, Direction.NORTH)
    guard_index = row.find('>')
    if (guard_index > -1):
      return (row_index, guard_index, Direction.EAST)
    guard_index = row.find('v')
    if (guard_index > -1):
      return (row_index, guard_index, Direction.SOUTH)
    guard_index = row.find('<')
    if (guard_index > -1):
      return (guard_index, row_index, Direction.WEST)


def has_block(x, y, lab_map):
  row = lab_map[y]
  print(f'row {row}')
  return y < len(row) and row[x] == '#'

def is_outside(location, lab_map):
  return location.x < 0 or location.x >= len(lab_map[0]) or location.y  < 0 or location.y >= len(lab_map)

####
# Main
####
inputs = ['.>.']
print(f'Guard: {find_guard(inputs)}')
inputs = ['.v.']
print(f'Guard: {find_guard(inputs)}')
inputs = ['.<.']
print(f'Guard: {find_guard(inputs)}')


inputs = ['....#.....', '.#..^.....']  #readlines('input5.txt')
print(f'Guard: {find_guard(inputs)}')

test = has_block(1, 1, ['..', '.#'])
print(f'Has block: {test}')
test = has_block(0, 0, ['..', '.#'])
print(f'Has block: {test}')

guard = GuardLocation(0, 0, Direction.EAST).move(['..'])
print(f'New guard: {guard}')
guard = guard.move(['..#'])
print(f'New guard: {guard}')
guard = GuardLocation(1, 0, Direction.WEST).move(['#.'])
print(f'New guard: {guard}')