from enum import Enum
from typing import Self

Direction = Enum('Direction', [('NORTH', 1), ('EAST', 2), ('SOUTH', 3),
                               ('WEST', 4)])


class GuardLocation:
  x = 0
  y = 0
  direction = Direction.NORTH

  def __init__(self, x: int, y: int, direction: Direction):
    self.x = x
    self.y = y
    self.direction = direction

  def __str__(self) -> str:
    return f'Guard at {self.x}, {self.y} facing {self.direction}'

  def copy(self):
    return GuardLocation(self.x, self.y, self.direction)

  def move(self, lab_map: list[str]) -> Self:
    next_location = get_next_move(self, lab_map)
    self.x = next_location.x
    self.y = next_location.y
    self.direction = next_location.direction
    return self


def get_next_move(location: GuardLocation,
                  lab_map: list[str]) -> GuardLocation:
  x = location.x
  y = location.y
  direction = location.direction
  while not is_outside(x, y, lab_map):
    if direction == Direction.NORTH:
      if has_block(x, y - 1, lab_map):
        direction = Direction.EAST
      else:
        return GuardLocation(x, y - 1, direction)
    elif direction == Direction.EAST:
      if has_block(x + 1, y, lab_map):
        direction = Direction.SOUTH
      else:
        return GuardLocation(x + 1, y, direction)
    elif direction == Direction.SOUTH:
      if has_block(x, y + 1, lab_map):
        direction = Direction.WEST
      else:
        return GuardLocation(x, y + 1, direction)
    else:
      if has_block(x - 1, y, lab_map):
        direction = Direction.NORTH
      else:
        return GuardLocation(x - 1, y, direction)
  return GuardLocation(x, y, direction)


def readlines(source: str) -> list[str]:
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


def find_guard(lab_map: list[str]) -> (GuardLocation | None):
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
  return None


def mark_guard(guard: GuardLocation, lab_map: list[str]) -> list[str]:
  row = lab_map[guard.y]
  tmp = row[0:guard.x] + 'X' + row[guard.x + 1:]
  lab_map[guard.y] = tmp
  return lab_map


def debug_map(lab_map: list[str]):
  for row in lab_map:
    print(row)
  print()


def has_block(x: int, y: int, lab_map: list[str]) -> bool:
  if is_outside(x, y, lab_map):
    return False
  row = lab_map[y]
  # print(f' row {row}')
  return y < len(row) and row[x] == '#'


def is_outside(x: int, y: int, lab_map: list[str]) -> bool:
  return x < 0 or x >= len(lab_map[0]) or y < 0 or y >= len(lab_map)


def move_guard_max_steps(guard: GuardLocation, lab_map: list[str],
                         max_steps: int) -> (GuardLocation | None):
  steps = 0
  while not is_outside(guard.x, guard.y, inputs) and steps < max_steps:
    guard = guard.move(inputs)
    steps += 1
    if not is_outside(guard.x, guard.y, inputs):
      mark_guard(guard, inputs)
    else:
      return guard
  return guard


def count_unique_visits(lab_map: list[str]) -> int:
  count = 0
  for row in lab_map:
    for c in row:
      if c == 'X':
        count += 1
  return count


####
# Main
####
inputs = readlines('sample.txt')
original_input = inputs.copy()
guard = find_guard(inputs)
original_guard = GuardLocation(guard.x, guard.y, guard.direction)

if guard is None:
  print('No guard found')
  exit()

mark_guard(guard, inputs)

guard = move_guard_max_steps(guard, inputs, len(inputs) * len(inputs[0]))
if guard is None:
  print('Ended moves with no guard')
  exit()
print(f'Final guard at {guard.x}, {guard.y} facing {guard.direction}')
count = count_unique_visits(inputs)
print(f'Part 1: {count}')

inputs = original_input.copy()
guard = GuardLocation(original_guard.x, original_guard.y,
                      original_guard.direction)
mark_guard(guard, inputs)

guard = move_guard_max_steps(guard, inputs, 3)
if guard is None:
  print('Ended moves with no guard')
  exit()
print(f'Final guard at {guard.x}, {guard.y} facing {guard.direction}')
debug_map(inputs)
count = count_unique_visits(inputs)
print(
    f'Part 2: {count}, guard location ({guard})character: {inputs[guard.y][guard.x]}'
)
