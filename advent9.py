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


def expand2(input: str) -> list[tuple[int, str]]:
  file_id = 0
  result = list[tuple[int, str]]()
  index = 0
  while index < len(input):
    reps = input[index]
    block = ''
    for r in range(0, int(reps)):
      block += str(file_id)
    result.append((int(reps), block))
    file_id += 1

    index += 1
    if index < len(input):
      spaces = input[index]
      space_block = ''
      for s in range(0, int(spaces)):
        space_block += '.'
      result.append((int(spaces), space_block))
      index += 1
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


def first_space_index(target_length: int, input: list[tuple[int, str]]) -> int:
  index = 0
  while index < len(input):
    (tmp_length, tmp_block) = input[index]
    if tmp_block.startswith('.') and tmp_length == target_length:
      return index
    index += 1
  return -1


def first_block_index(start_at: int, input: list[tuple[int, str]]) -> int:
  index = start_at
  while index >= 0:
    (tmp_length, tmp_block) = input[index]
    if not tmp_block.startswith('.'):
      return index
    index -= 1
  return index


def compact2(input: list[tuple[int, str]]):
  block_index = first_block_index(len(input) - 1, input)
  while block_index >= 0:
    (tmp_length, tmp_block) = input[block_index]
    space_index = first_space_index(tmp_length, input)
    if space_index < block_index:
      tmp = input[space_index]
      input[space_index] = input[block_index]
      input[block_index] = tmp

    # Move to the next block
    block_index -= 1
    block_index = first_block_index(block_index, input)


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

disk = compact(disk)
check_sum = generate_check_sum(disk)
print(check_sum)

disk2 = expand2(disk_map[0])
output = ''
for (_, block) in disk2:
  output += block
#print(f'Part 1 expand equals part 2: {pretty == output}')

disk2 = [(3, 'aaa'), (5, '.....'), (5, 'bbbbb'), (1, 'a'), (3, '...')]
print(first_block_index(len(disk2) - 1, disk2))
print(first_block_index(2, disk2))
print(first_block_index(1, disk2))

print(first_space_index(5, disk2))
print(first_space_index(3, disk2))
compact2(disk2)
print(disk2)
