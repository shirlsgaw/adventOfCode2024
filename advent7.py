from os import read


def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


def find_operations(total, values):
  print(f' inputs: {total}: {values}')
  if len(values) < 2:
    raise AssertionError(f'Not enough values: {values}')
  # Base case
  if len(values) == 2:
    if total == values[0] + values[1]:
      return f'{values[0]}+{values[1]}'
    if total == values[0] * values[1]:
      return f'{values[0]}*{values[1]}'
    return None
  else:
    last = values.pop()
    sub_total = total - last
    div_total = int(total / last)
    
    add_result = find_operations(sub_total, values.copy())
    print(f'   recurse add {total}={add_result}+{last}')

    if total % last == 0:
      multiply_result = find_operations(div_total, values.copy())
      #print(f'   recurse multiply {total}={multiply_result}*{last}')
    else:
      multiply_result = None
      #print(f'   skip recurse multiply {total} != {div_total} * {last}')
    

    if add_result is not None:
      return f'{add_result}+{last}'
    if multiply_result is not None:
      return f'{multiply_result}*{last}'
    return None


###
# Main
###
inputs = readlines('sample.txt')
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

# Test base cases
#print(find_operations(190, [10, 19]))
#print(find_operations(100, [10, 19]))
#print(find_operations(125, [100, 25]))

# Test recursive cases
#print(find_operations(3267, [81, 40, 27]))
#print(find_operations(464, [12, 34, 56]))
#print(find_operations(7290, [6, 8, 6, 15]))
#print(find_operations(292, [11,6,16,20]))
#print(find_operations(272, [11, 6, 16]))
#print(find_operations(663936, [8, 920, 25, 272, 855, 78]))
#print(find_operations(8512, [8, 920, 25, 272, 855]))
#print(find_operations(36, [1, 2, 3, 4]))

part1_total = 0
for i in range(0, len(totals_list)):
  result = find_operations(totals_list[i], operands_list[i].copy())
  if result is None:
    multiply_all = 1
    for y in operands_list[i]:
      print(y)
      multiply_all *= y
    print(
        f' Failed for {totals_list[i]}, debug multiply_all={multiply_all}, operands={operands_list[i]}'
    )
  else:
    print(f' Success: {totals_list[i]} = {result}')
    part1_total += totals_list[i]
print(f'Part 1: {part1_total}')
