from enum import Enum
from os import cpu_count
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

def mark_guard(guard, lab_map, mark_char='X'):
  row = lab_map[guard.y]
  tmp = row[0:guard.x] + mark_char + row[guard.x + 1:]
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
  return y < len(row) and row[x] in {'#', 
                                     'O'}

def is_outside(x, y, lab_map):
  return x < 0 or x >= len(lab_map[0]) or y  < 0 or y >= len(lab_map)

def count_unique_visits(lab_map) -> int:
  count = 0
  for row in lab_map:
    for c in row:
      if c == 'X':
        count += 1
  return count

def walk_guard(guard, lab_map, visit_count_map, max_steps, do_mark=True):
  steps = 0
  while not is_outside(guard.x, guard.y, lab_map) and steps < max_steps:
    visit_count_map[guard.y][guard.x] += 1
    if do_mark:
      lab_map = mark_guard(guard, lab_map)
    guard.move(lab_map)
    steps += 1

####
# Main
####
inputs = readlines('sample.txt')
original_inputs = inputs.copy()

guard = find_guard(inputs)
original_guard = GuardLocation(guard.x, guard.y, guard.direction)

mark_guard(guard, inputs)

visit_count_map = list(map(lambda x: list(map(lambda y: 0, x)), inputs))
walk_guard(guard, inputs, visit_count_map, len(inputs) * len(inputs[0]), do_mark=True)
count = count_unique_visits(inputs)
print(f'Part 1: {count}')

###
# Part 2
###

# Find all visited places in the original map as possible places to put the obstruction
candidates = set()
mark_guard(original_guard, inputs, 'G')
for row_index in range(0, len(inputs)):
  for column_index in range(0, len(inputs[0])):
    if inputs[row_index][column_index] == 'X':
      candidates.add((column_index, row_index))

# Try to add an obstruction in the candidate position and see if the guard passes it 
# repeatedly
obstructions = 0
for (x, y) in candidates:
  inputs = original_inputs.copy()
  guard = GuardLocation(original_guard.x, original_guard.y, original_guard.direction)
  mark_guard(GuardLocation(x, y, original_guard.direction), inputs, mark_char='O')
  visit_count_map = list(map(lambda x: list(map(lambda y: 0, x)), inputs))
  walk_guard(guard, inputs, visit_count_map, 
             4 * len(inputs) * len(inputs[0]), 
             do_mark=True)

  if is_outside(guard.x, guard.y, inputs):
    continue
  for row in visit_count_map:
    row.sort(reverse=True)
    if row[0] > 4:
      obstructions += 1
      #debug_map(visit_count_map)
      #debug_map(inputs)
      break

print(f'Part 2: {obstructions}')



