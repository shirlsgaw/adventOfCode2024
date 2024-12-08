from os import read


def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


def find_operations(total, values):
  #print(f' inputs: {total}: {values}')
  if len(values) < 2:
    raise AssertionError(f'Not enough values: {values}')
  # Base case
  if len(values) == 2:
    if total == values[0] + values[1]:
      return f'{values[0]}+{values[1]}'
    if total == values[0] * values[1]:
      return f'{values[0]}*{values[1]}'
    concat = int(str(values[0]) + str(values[1]))
    #print(f'  concat: {values[0]}||{values[1]}={concat}')
    if total == concat:
      return f'{values[0]}||{values[1]}'
    return None
  else:
    last = values.pop()
    sub_total = total - last
    div_total = int(total / last)

    add_result = find_operations(sub_total, values.copy())
    #print(f'   recurse add {total}={add_result}+{last}')

    if total % last == 0:
      multiply_result = find_operations(div_total, values.copy())
      #print(f'   recurse multiply {total}={multiply_result}*{last}')
    else:
      multiply_result = None
      # print(f'   skip recurse multiply {total} != {div_total} * {last}')

    last_str = str(last)
    total_str = str(total)
    concat_result = None
    if total_str != last_str and total_str.endswith(last_str):      
      prefix = total_str[:len(total_str) - len(last_str)]
      if total_str != prefix + last_str:
        raise AssertionError(f'Concatenation failed: {total_str} != {prefix}+{last_str}')
      concat_result = find_operations(int(prefix), values.copy())

    if add_result is not None:
      return f'{add_result}+{last}'
    if multiply_result is not None:
      return f'{multiply_result}*{last}'
    if concat_result is not None:
      return f'{concat_result}||{last}'
    return None

###
# Main
###
inputs = readlines('input7.txt')
totals_list = list()
operands_list = list()
for row in inputs:
  str1, str2 = row.split(':')
  totals_list.append(int(str1))
  values = str2.split(' ')
  operands = list()
  for v in values:
    if v.isnumeric():
      operands.append(int(v))
  operands_list.append(operands)

#print(find_operations(157, [15, 6, 1]))
#print(find_operations(211, [15, 6, 1]))
#print(find_operations(211, [15, 6, 1]))

part1_total = 0
for i in range(0, len(totals_list)):
  result = find_operations(totals_list[i], operands_list[i].copy())
  if result is not None:
    # print(f' Success: {totals_list[i]} = {result}')
    part1_total += totals_list[i]
print(f'Part 2: {part1_total}')
