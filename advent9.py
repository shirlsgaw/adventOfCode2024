from enum import Enum


def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


def mark(x: int, y: int, location_map: list[str], mark_char='X'):
  row = location_map[y]
  tmp = row[0:x] + mark_char + row[x + 1:]
  location_map[y] = tmp


def expand(input: str) -> str:
  return 'foobar'


def compact(input: str) -> str:
  result = input
  i = 0
  j = len(result) - 1
  while i < j:
    while i < j and result[i] != '.':
      i += 1
    while i < j and result[j] == '.':
      j -= 1

    if i < j:
      tmp = result[i]
      input_l = [result]
      mark(i, 0, input_l, mark_char=result[j])
      mark(j, 0, input_l, mark_char=tmp)
      result = input_l[0]
  return result


def generate_check_sum(input: str) -> int:
  check_sum = 0
  for i in range(0, len(input)):
    if input[i].isdigit():
      check_sum += i * int(input[i])
  return check_sum


####
# Main
####
disk_map = readlines('input9.txt')
print('number of lines: ' + str(len(disk_map)))

disk = expand(disk_map[0])
print(disk)

disk = compact('0..1.3.')
print(disk)

check_sum = generate_check_sum('13..5..')
print(check_sum)
