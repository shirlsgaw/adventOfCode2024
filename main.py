from os import read


def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


def is_match(str):
  result = (str == 'XMAS' or str == 'SAMX')
  return result


def horizontal(start, str):
  if len(str) < 4:
    return False
  sub = str[start:start + 4]
  return is_match(sub)


def vertical(row, col, lstr):
  lsub = lstr[row:]
  if len(lsub) < 4:
    return False
  for x in lsub:
    if len(x) < col + 1:
      return False
  test = ''
  for i in range(0, 4):
    test += lsub[i][col]
  return is_match(test)


def down_diagonal(row, col, lstr):
  lsub = lstr[row:row + 4]
  if len(lsub) < 4:
    return False
  for x in lsub:
    if len(x) < col + 4:
      return False
  test = ''
  for i in range(0, 4):
    test += lsub[i][col + i]
  return is_match(test)


def up_diagonal(row, col, lstr):
  if row < 3:
    return False
  lsub = lstr[row - 3:row + 1]
  for x in lsub:
    if len(x) < col + 4:
      return False
  test = ''
  for i in range(0, 4):
    test += lsub[3 - i][col + i]
  return is_match(test)


tests = [['1X11', '2M22', '3A33', '4S44'],
         ['0000', '1X11', '2M22', '3A33', '4S44'],
         ['00000', '1X111', '22M22', '333A3', '4444S']]
inputs = readlines('sample.txt')
#print(vertical(0,0,tests[0]))
#print(vertical(0,1,tests[0]))
#print(vertical(0,1,tests[1]))
#print(vertical(1,1,tests[1]))
#print(down_diagonal(0,0, tests[0]))
#print(down_diagonal(1,1, tests[2]))
#print(up_diagonal(1,1, tests[2]))
#print(up_diagonal(3,1, tests[2]))
#print(up_diagonal(3,1, inputs))

total = 0
for row in range(0, len(inputs)):
  for column in range(0, len(inputs[row])):
    if horizontal(column, inputs[row]):
      total += 1
    if vertical(row, column, inputs):
      total += 1
    if down_diagonal(row, column, inputs):
      total += 1
    if up_diagonal(row, column, inputs):
      total += 1
print(f'Total: {total}')
