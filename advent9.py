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
    if tmp_block.startswith('.') and target_length <= tmp_length:
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


def compact2(input: list[tuple[int, str]]) -> list[tuple[int, str]]:
  result_stack = list[tuple[int, str]]()
  todo = input.copy()

  # Process blocks from back to front, passing spaces
  while len(todo) > 0:
    #print(f' todo {todo}')
    output = result_stack.copy()
    output.reverse()
    #print(f' output {output}')

    (tmp_length, tmp_block) = todo.pop()

    # Pass through spaces
    while tmp_block.startswith('.'):
      result_stack.append((tmp_length, tmp_block))
      (tmp_length, tmp_block) = todo.pop()

    # Process block
    #print(f'*Block: {tmp_block}, {tmp_length}')
    space_index = first_space_index(tmp_length, todo)
    if space_index == -1:
      #print(f'--not found adding to stack ({tmp_length},{tmp_block})')
      result_stack.append((tmp_length, tmp_block))
    else:
      (space_length, space_block) = todo[space_index]
      prefix = space_block[:tmp_length]
      suffix = space_block[tmp_length:]
      #print(f'++Prefix: {prefix}, Suffix: {suffix}')
      result_stack.append((len(prefix), prefix))
      todo[space_index] = (tmp_length, tmp_block)
      if len(suffix) > 0:
        todo.insert(space_index + 1, (len(suffix), suffix))

  result_stack.reverse()
  return result_stack


def generate_check_sum(input: list[str]) -> int:
  check_sum = 0
  for i in range(0, len(input)):
    if not input[i].startswith('.'):
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
print(f'Part 1 checksum: {check_sum}')

disk2 = expand2('2333133121414131402')
output = ''
for (_, block) in disk2:
  output += block
#print(f'Part 1 expand equals part 2: {pretty == output}')

#disk2 = [(3, 'aaa'), (5, '.....'), (5, 'bbbbb'), (2, 'xx')]
#disk2 = compact2(disk2)
#print(disk2)

disk2 = compact2(disk2)
output = list[str]()
for (_, block) in disk2:
  if len(block) > 0:
    output.append(block)
print('Part 2: ' + ''.join(output))
check_sum = generate_check_sum(output)
print(check_sum)
