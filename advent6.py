from enum import Enum, unique
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
    (next_location, _) = get_next_move(self, lab_map)
    self.x = next_location.x
    self.y = next_location.y
    self.direction = next_location.direction
    return self


def get_next_move(location: GuardLocation,
                  lab_map: list[str]) -> tuple[GuardLocation,bool]:
  x = location.x
  y = location.y
  direction = location.direction
  found_obstruction = False
  next_direction = direction
  while not is_outside(x, y, lab_map):
    if direction == Direction.NORTH:
      if has_block(x, y - 1, lab_map):
        direction = Direction.EAST
        found_obstruction = 'O' == lab_map[y - 1][x]
      else:
          return (GuardLocation(x, y-1, direction), found_obstruction)
    elif direction == Direction.EAST:
      if has_block(x + 1, y, lab_map):
        direction = Direction.SOUTH
        found_obstruction = 'O' == lab_map[y][x + 1]
      else:
        return (GuardLocation(x + 1, y, direction), found_obstruction)
    elif direction == Direction.SOUTH:
      if has_block(x, y + 1, lab_map):
        direction = Direction.WEST
        found_obstruction = 'O' == lab_map[y + 1][x]
      else:
            return (GuardLocation(x, y + 1, direction), found_obstruction)
    else:
      if has_block(x - 1, y, lab_map):
        direction = Direction.NORTH
        found_obstruction = 'O' == lab_map[y][x - 1]
      else:
        return (GuardLocation(x - 1, y, direction), found_obstruction)
  return (GuardLocation(x, y, direction), found_obstruction)

def readlines(source: str) -> list[str]:
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


def find_guard(lab_map: list[str]) -> GuardLocation:
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
  raise AssertionError(f'No guard found in {lab_map}')


def mark_guard(guard: GuardLocation,
               lab_map: list[str],
               mark_char: str = 'X') -> list[str]:
  row = lab_map[guard.y]
  tmp = row[0:guard.x] + mark_char + row[guard.x + 1:]
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
  return row[x] in set(['#', 'O'])


def is_outside(x: int, y: int, lab_map: list[str]) -> bool:
  return x < 0 or x >= len(lab_map[0]) or y < 0 or y >= len(lab_map)


def move_guard_max_steps(guard: GuardLocation, lab_map: list[str],
                         max_steps: int) -> tuple[GuardLocation, int]:
  steps: int = 0
  while not is_outside(guard.x, guard.y, inputs) and steps < max_steps:
    guard = guard.move(inputs)
    if not is_outside(guard.x, guard.y, inputs):
      steps += 1
      mark_guard(guard, inputs)
  return (guard, steps)


def count_unique_visits(lab_map: list[str]) -> int:
  count = 0
  for row in lab_map:
    for c in row:
      if c == 'X':
        count += 1
  return count

def is_valid_obstruction(obstruction: tuple[int,int], 
                         guard: GuardLocation, 
                         lab_map: list[str]) -> bool:
  #mark_guard(guard, inputs)
  mark_guard(GuardLocation(obstruction[0], obstruction[1], Direction.NORTH), 
             inputs, 
             mark_char='O')  # Add test barrier in original path
  obstruction_hits = 0
  # Circle every step multiple times
  max_steps = 2 * len(lab_map) * len(lab_map[0])
  replay_steps = 0
  while obstruction_hits < 2 and not is_outside(guard.x, guard.y,
                                            inputs) and replay_steps < max_steps:
    (next, found_obstruction) = get_next_move(guard, inputs)    
    if found_obstruction:
      obstruction_hits += 1
    if not is_outside(next.x, next.y, inputs):
      pass
      #mark_guard(next, inputs)
    guard = next
    replay_steps += 1
  mark_guard(GuardLocation(obstruction[0], obstruction[1], Direction.NORTH), 
     inputs, 
     mark_char='.')  # Reset
  return obstruction_hits >= 2

####
# Main
####
inputs = readlines('input6.txt')
original_input = inputs.copy()
guard = find_guard(inputs)
original_guard = GuardLocation(guard.x, guard.y, guard.direction)

mark_guard(guard, inputs)

(guard, orig_steps) = move_guard_max_steps(guard, inputs,
                                           len(inputs) * len(inputs[0]))
print(f'Final guard at {guard.x}, {guard.y} facing {guard.direction}')
count = count_unique_visits(inputs)
print(f'Part 1: count={count}, steps={orig_steps}')
#debug_map(inputs)
obstructions = set()
inputs = original_input.copy()
for steps in range(4, orig_steps):
  guard = GuardLocation(original_guard.x, original_guard.y,
                        original_guard.direction)
#  mark_guard(guard, inputs)
  move_guard_max_steps(guard, inputs, steps)
  (next, _) = get_next_move(guard, inputs)
  is_inside = not is_outside(next.x, next.y, inputs)
  not_origin = next.x != original_guard.x or next.y != original_guard.y
  if is_inside and not_origin:
    # Replay the scenario with a test barrier
    inputs = original_input.copy()
    guard = GuardLocation(original_guard.x, original_guard.y,
                          original_guard.direction)
    if is_valid_obstruction((next.x, next.y), guard, inputs):
      obstructions.add((next.x, next.y))
      
print(f'Part 2: count={len(obstructions)}')
