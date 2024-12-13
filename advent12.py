from collections.abc import Generator


def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


####
# Checks if the location is outside the map
####
def is_outside(x: int, y: int, location_map: list[str]):
  return x < 0 or x >= len(location_map[0]) or y < 0 or y >= len(location_map)


####
# Returns the number of sides that need fencing for this location
####
def compute_perimeter(x: int, y: int, plots: list[str]) -> int:
  border_sides = 0

  # A fence needs to be build between plots that are not the same type
  value = plots[y][x]

  # North
  next_y = y - 1
  next_x = x
  if is_outside(next_x, next_y, plots) or value != plots[next_y][next_x]:
    border_sides += 1

  # South
  next_y = y + 1
  next_x = x
  if is_outside(next_x, next_y, plots) or value != plots[next_y][next_x]:
    border_sides += 1

  # East
  next_y = y
  next_x = x + 1
  if is_outside(next_x, next_y, plots) or value != plots[next_y][next_x]:
    border_sides += 1

  # West
  next_y = y
  next_x = x - 1
  if is_outside(next_x, next_y, plots) or value != plots[next_y][next_x]:
    border_sides += 1
  return border_sides

####
# Find all points that are in the same region as (x, y)
####
explored = set[tuple[int, int]]()
def get_region(x: int, y: int, plots: list[str]) -> Generator[tuple[int, int], None, None]:
  if (x, y) in explored:
    return None

  value = plots[y][x]
  explored.add((x, y))
  yield (x, y)
  # North
  next_y = y - 1
  next_x = x
  if not is_outside(next_x, next_y, plots) and value == plots[next_y][next_x]:
    yield from get_region(next_x, next_y, plots)

  # East
  next_y = y
  next_x = x + 1
  if not is_outside(next_x, next_y, plots) and value == plots[next_y][next_x]:
    yield from get_region(next_x, next_y, plots)

  # South
  next_y = y + 1
  next_x = x
  if not is_outside(next_x, next_y, plots) and (next_x, next_y) not in explored and value == plots[next_y][next_x]:
    yield from get_region(next_x, next_y, plots)

  # West
  next_y = y
  next_x = x - 1
  if not is_outside(next_x, next_y, plots) and value == plots[next_y][next_x]:
    yield from get_region(next_x, next_y, plots)

####
# North
####
def has_north_border(x: int, y: int, plots: list[str], target_value: str) -> bool:
  next_y = y - 1
  next_x = x
  return is_outside(next_x, next_y, plots) or target_value != plots[next_y][next_x]

####
# West
####
def has_west_border(x: int, y: int, plots: list[str], target_value: str) -> bool:
  next_y = y
  next_x = x - 1
  return is_outside(next_x, next_y, plots) or target_value != plots[next_y][next_x]

####
# East
####
def has_east_border(x: int, y: int, plots: list[str], target_value: str) -> bool:
  next_y = y
  next_x = x + 1
  return is_outside(next_x, next_y, plots) or target_value != plots[next_y][next_x]

####
# South
####
def has_south_border(x: int, y: int, plots: list[str], target_value: str) -> bool:
  next_y = y + 1
  next_x = x
  return is_outside(next_x, next_y, plots) or target_value != plots[next_y][next_x]


def compute_fencing(map: list[str], regions: list[list[tuple[int, int]]]) -> int:
  cost = 0
  for region in regions:
    value = None    
    area = len(region)
    region_set = set[tuple[int, int]](region)
    
    sides = 0
    for (x, y) in region:
      #print(f'({x}, {y})')
      value = map[y][x]
      # West
      west_y = y
      west_x = x - 1

      # East
      east_y = y
      east_x = x + 1

      # North
      north_y = y - 1
      north_x = x

      # South
      south_y = y + 1
      south_x = x
      if has_north_border(x, y, map, value):
        if (west_x, west_y) not in region or not has_north_border(west_x, west_y, map, value):
          #print(f'. ({x}, {y}) North')
          sides += 1
      if has_south_border(x, y, map, value):
        if (west_x, west_y) not in region or not has_south_border(west_x, west_y, map, value):
          #print(f'. ({x}, {y}) South')
          sides += 1
      if has_west_border(x, y, map, value):
        if (north_x, north_y) not in region or not has_west_border(north_x, north_y, map, value):
          #print(f'. ({x}, {y}) West')
          sides += 1
      if has_east_border(x, y, map, value):
        if (north_x, north_y) not in region or not has_east_border(north_x, north_y, map, value):
          #print(f'. ({x}, {y}) East')
          sides += 1
          
    fencing = area * sides
    print(f'Region {region} has {area} * {sides} = {fencing}')
    cost += fencing
  return cost


####
# Main
####
map = readlines('sample.txt')
regions = list(list[tuple[int, int]]())
for y in range(0, len(map)):
  for x in range(0, len(map[0])):
    if (x, y) not in explored:
      points = list[tuple[int, int]]()
      for (px, py) in get_region(x, y, map):
        points.append((px, py))
      regions.append(points)
      #print(f'Region ({map[y][x]}): {points}')

fencing_cost = compute_fencing(map, regions)
print(f'Part 1: {fencing_cost}')