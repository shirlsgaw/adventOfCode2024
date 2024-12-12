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

def get_region_id(x: int, y: int, plots: list[str], 
                  ids_cache: list[list[int], list[int]], next_id: int) -> int:
  # A region is new if it's northern neighbor AND western neighbor are different from the current location
  value = plots[y][x]

  # North
  prev_y = y - 1
  prev_x = x
  north_is_different = is_outside(prev_x, prev_y, plots) or value != plots[prev_y][prev_x]
  

  # West
  prev_y = y
  prev_x = x - 1
  west_is_different = is_outside(prev_x, prev_y, plots) or value != plots[prev_y][prev_x]

  if north_is_different and west_is_different:
    return next_id
  elif north_is_different:
    return ids_cache[y % 2][x - 1]
  else:
    return ids_cache[(y - 1) % 2][x]

def compute_fencing(map: list[str]) -> int:
  
  areas = dict[int, int]()
  perimeters = dict[int, int]()

  # Track the last two rows of IDs
  curr_id = -1
  row_ids = list[list[int], list[int]]()
  row_ids.append(list[int]())
  row_ids.append(list[int]())

  # Initialize list
  for i in range(0, len(map)):
    row_ids[0].append(-1)
    row_ids[1].append(-1)
  
  for y in range(0, len(map)):
    for x in range(0, len(map[0])):
      region_id = get_region_id(x, y, map, row_ids, curr_id + 1)
      row_ids[y % 2][x] = region_id
      
      if region_id > curr_id:
        curr_id += 1
        areas[region_id] = 1
      else:
        areas[region_id] += 1
      print(f'.({map[y][x]}) ({x}, {y}): region id {region_id}, areas={areas[region_id]}')

      perimeter = perimeters.get(region_id, 0)
      perimeter += compute_perimeter(x, y, map)
      perimeters[region_id] = perimeter
      print(f'.. perimeter={perimeter}')

  fencing_cost = 0
  for id in areas:
    fencing = areas[id] * perimeters[id]
    print(f'Type {id}: {areas[id]} * {perimeters[id]} = {fencing}')
    fencing_cost += fencing
  return fencing_cost


####
# Main
####
map = readlines('sample.txt')
print('Fencing cost: ' + str(compute_fencing(map)))
