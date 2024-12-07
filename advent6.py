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
                         lab_map: list[str],
                         max_steps: int
                        ) -> bool:
  mark_guard(GuardLocation(obstruction[0], obstruction[1], Direction.NORTH), 
             inputs, 
             mark_char='O')  # Add test barrier in original path
  obstruction_hits = 0
  replay_steps = 0
  collision_location = None
  steps_to_hit = max_steps
  while obstruction_hits < 2 and not is_outside(guard.x, guard.y,
                                            inputs) and replay_steps < max_steps:
    (next, found_obstruction) = get_next_move(guard, inputs)    
    if found_obstruction:
      collision_location = (guard.x, guard.y)
      obstruction_hits += 1
    if guard.direction != next.direction:
      mark_guard(guard, inputs, mark_char='+')
    elif guard.direction in {Direction.EAST, Direction.WEST}:
      mark_guard(guard, inputs, mark_char='-')
    else:
      mark_guard(guard, inputs, mark_char='|')
    guard = next
    replay_steps += 1
  if is_outside(guard.x, guard.y, inputs):
    return False
  if collision_location is None:
    return False
  obstruction_str= inputs[collision_location[1]][collision_location[0]]
  print(f'Obstruction: {obstruction_str} at {collision_location}')
  return obstruction_str == '+'
    
  #if obstruction_hits >= 2:
  #  return True
  #if obstruction_hits == 0:
  #  return False
  #if steps_to_hit != max_steps:
  #  print(f'Obstruction {obstruction} hit {obstruction_hits} in {steps_to_hit} steps')
  #return False

####
# Main
####
inputs = readlines('hint.txt')
original_input = inputs.copy()
guard = find_guard(inputs)
original_guard = GuardLocation(guard.x, guard.y, guard.direction)

mark_guard(guard, inputs)

(guard, orig_steps) = move_guard_max_steps(guard, inputs,
                                           len(inputs) * len(inputs[0]))
#print(f'Final guard at {guard.x}, {guard.y} facing {guard.direction}')
count = count_unique_visits(inputs)
print(f'Part 1: count={count}, steps={orig_steps}')
debug_map(inputs)
obstructions = set()
candidates = list()

# Disallow the original guard location from candidates
mark_guard(original_guard, inputs, 'G')
# Find all of the original visited locations, these are potential areas to block
for row_index in range(0, len(inputs)):
  for column_index in range(0, len(inputs[0])):
    if inputs[row_index][column_index] == 'X':
      candidates.append((column_index, row_index))
inputs = original_input.copy()

# Test all candidates
#candidates = list()
#candidates.append((118, 117)) # Obstruction (118, 11) hit 1 in 4648 steps
#candidates.append((121, 17)) # Obstruction (121, 17) hit 1 in 4657 steps
#candidates.append((123, 17)) # Obstruction (123, 17) hit 1 in 4747 steps
#candidates.append((115, 18)) # Obstruction (115, 18) hit 1 in 3420 steps
for (cadidate_x, candidate_y) in candidates:
  guard = GuardLocation(original_guard.x, original_guard.y,
                        original_guard.direction)
  inputs = original_input.copy()
  if is_valid_obstruction((cadidate_x, candidate_y), 
                          guard, inputs, len(inputs) * len(inputs[0])):
    obstructions.add((cadidate_x, candidate_y))
  debug_map(inputs)    
print(f'Part 2: count={len(obstructions)}')
