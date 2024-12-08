from enum import Enum


def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


def mark(x: int, y: int, location_map: list[str], mark_char='X'):
  row = location_map[y]
  tmp = row[0:x] + mark_char + row[x + 1:]
  location_map[y] = tmp


def debug_map(location_map: list[str]):
  for row in location_map:
    print(row)
  print()


def is_outside(x: int, y: int, location_map: list[str]):
  return x < 0 or x >= len(location_map[0]) or y < 0 or y >= len(location_map)


def find_antennas(location_map: list[str]) -> dict[str, list[tuple[int, int]]]:
  antennas = dict()
  for row_index in range(0, len(location_map)):
    for col_index in range(0, len(location_map[0])):
      char = location_map[row_index][col_index]
      if char != '.':
        if char not in antennas:
          antennas[char] = list()
        antennas[char].append((col_index, row_index))
  return antennas


def find_antipodes(
    location_map: list[str], antennas: dict[str, list[tuple[int, int]]]
) -> dict[str, list[tuple[int, int]]]:
  antipodes = dict()
  for antenna, locations in antennas.items():
    if antenna not in antipodes:
      antipodes[antenna] = list()
    #print(f'Antenna: {antenna}: {locations}')
    for first_index in range(0, len(locations)):
      first_x, first_y = locations[first_index]
      for second_index in range(first_index + 1, len(locations)):
        second_x, second_y = locations[second_index]
        delta_x = second_x - first_x
        delta_y = second_y - first_y
        #print(f'  Delta: {delta_x}, {delta_y}')

        antipode1 = (first_x - delta_x, first_y - delta_y)
        antipode2 = (second_x + delta_x, second_y + delta_y)

        if is_outside(antipode1[0], antipode1[1], location_map):
          #print(f'Antipode 1: {antipode1} is outside')
          pass
        else:
          mark(antipode1[0], antipode1[1], location_map, mark_char='#')
          antipodes[antenna].append(antipode1)

        if is_outside(antipode2[0], antipode2[1], location_map):
          #print(f'Antipode 2: {antipode2} is outside')
          pass
        else:
          mark(antipode2[0], antipode2[1], location_map, mark_char='#')
          antipodes[antenna].append(antipode2)

  return antipodes


def count_antipodes(antipodes: dict[str, list[tuple[int, int]]]) -> int:
  locations = set()
  for _, ls in antipodes.items():
    for location in ls:
      locations.add(location)
  return len(locations)


####
# Main
####
inputs = readlines('input8.txt')
ants = find_antennas(inputs)
#print(ants)
antipodes = find_antipodes(inputs, ants)
#print(antipodes)
#debug_map(inputs)

print(f'Part 1: {count_antipodes(antipodes)}')