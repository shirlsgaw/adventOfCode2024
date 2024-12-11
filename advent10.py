from collections.abc import Generator


def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


####
# Return all points with zeros as the value in the map
####
def find_zeros(map: list[str]) -> Generator[tuple[int, int], None, None]:
  for y in range(0, len(map)):
    for x in range(0, len(map[0])):
      if map[y][x] == '0':
        yield (x, y)


####
# Checks if the location is outside the map
####
def is_outside(x: int, y: int, location_map: list[str]):
  return x < 0 or x >= len(location_map[0]) or y < 0 or y >= len(location_map)


####
# Checks that the proposed location matches the following criteria
# 1. The location is not outside the map
# 2. The location is the next value up from the current location
# 3. The location is not a shorter path than already explored
####
def is_valid_location(curr_x: int, curr_y: int, next_x: int, next_y: int,
                      location_map: list[str],
                      visited: set[tuple[int, int]]) -> bool:
  if is_outside(next_x, next_y, location_map):
    return False

  curr_value = location_map[curr_y][curr_x]
  next_value = location_map[next_y][next_x]
  
  if (next_x, next_y) in visited:
    return False

  expected = str(int(curr_value) + 1)
  return next_value == expected


####
# Get at a point from the horizon
####
def get_horizon(
    x: int, y: int, map: list[str],
    visited: set[tuple[int, int]]) -> Generator[tuple[int, int], None, None]:
  # North
  #print(f'. North of ({x}, {y})')
  next_y = y - 1
  next_x = x
  if is_valid_location(x, y, next_x, next_y, map, visited):
    yield (next_x, next_y)

  # South
  #print(f'. South of ({x}, {y})')
  next_y = y + 1
  next_x = x
  if is_valid_location(x, y, next_x, next_y, map, visited):
    yield (next_x, next_y)

  # East
  #print(f'. East of ({x}, {y})')
  next_y = y
  next_x = x + 1
  if is_valid_location(x, y, next_x, next_y, map, visited):
    yield (next_x, next_y)

  # West
  #print(f'. West of ({x}, {y})')
  next_y = y
  next_x = x - 1
  if is_valid_location(x, y, next_x, next_y, map, visited):
    yield (next_x, next_y)

  return None

####
# Main
####
topo_map = readlines('hint.txt')


sum = 0
# Find all 0 points
for (x, y) in find_zeros(topo_map):
  nine_locations = set[tuple[int, int]]()
  visited = set[tuple[int, int]]()

  unexplored = list[tuple[int, int]]()
  #print(f'Trailhead: ({x}, {y})')
  unexplored.append((x, y))

  while len(unexplored) > 0:
    curr_x, curr_y = unexplored.pop(0)
    visited.add((curr_x, curr_y))
    #print(f'({curr_x}, {curr_y}): {topo_map[curr_y][curr_x]}, unexplored: {unexplored}')
    

    if topo_map[curr_y][curr_x] == '9':
      nine_locations.add((curr_x, curr_y))
      #print(f'Found a 9 at ({curr_x}, {curr_y}), locations={nine_locations}')
    else:
      # Start path finding to 9
      for hx, hy in get_horizon(curr_x, curr_y, topo_map, visited):
        unexplored.append((hx, hy))
        #print(f'...Horizon ({curr_x}, {curr_y}): ({hx}, {hy})')
  print(f'Trailhead: ({x}, {y}): {len(nine_locations)}')
  sum += len(nine_locations)
print('Part 1: ' + str(sum))
