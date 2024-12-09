def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


def mark(x: int, y: int, location_map: list[str], mark_char='X'):
  row = location_map[y]
  tmp = row[0:x] + mark_char + row[x + 1:]
  location_map[y] = tmp


def expand(input: str) -> list[str]:
  file_id = 0
  result = list()
  index = 0
  while index < len(input):
    reps = input[index]
    for r in range(0, int(reps)):
      result.append(str(file_id))
    index += 1
    if index < len(input):
      spaces = input[index]
      for s in range(0, int(spaces)):
        result.append('.')
      index += 1
    file_id += 1

  return result


def compact(input: list[str]) -> list[str]:
  result = input.copy()
  i = 0
  j = len(result) - 1
  while i < j:
    while i < j and result[i] != '.':
      i += 1
    while i < j and result[j] == '.':
      j -= 1

    if i < j:
      tmp = result[i]
      result[i] = result[j]
      result[j] = tmp
  return result


def generate_check_sum(input: list[str]) -> int:
  check_sum = 0
  for i in range(0, len(input)):
    if input[i] != '.':
      check_sum += i * int(input[i])
  return check_sum


####
# Main
####
disk_map = readlines('input9.txt')

disk = expand(disk_map[0])
pretty = ''.join(disk)
#print(pretty)

disk = compact(disk)
#print(disk)

check_sum = generate_check_sum(disk)
print(check_sum)
