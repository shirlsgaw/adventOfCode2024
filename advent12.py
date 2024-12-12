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


def compute_fencing(map: list[str]) -> int:
  areas = dict[str, int]()
  perimeters = dict[str, int]()

  for y in range(0, len(map)):
    for x in range(0, len(map[0])):
      type = map[y][x]
      type_area = areas.get(type, 0)
      type_area += 1
      areas[type] = type_area

      type_perimeter = perimeters.get(type, 0)
      type_perimeter += compute_perimeter(x, y, map)
      perimeters[type] = type_perimeter

  fencing_cost = 0
  for type in areas:
    type_fencing = areas[type] * perimeters[type]
    print(f'Type {type}: {type_fencing}')
    fencing_cost += type_fencing
  return fencing_cost


####
# Main
####
map = readlines('hint.txt')
print('Fencing cost: ' + str(compute_fencing(map)))
