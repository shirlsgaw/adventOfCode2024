from os import read


def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


def is_match(str):
  result = (str == 'MAS' or str == 'SAM')
  return result


def horizontal(start, str):
  if len(str) < 3:
    return False
  sub = str[start:start + 3]
  return is_match(sub)


def vertical(row, col, lstr):
  lsub = lstr[row:]
  if len(lsub) < 3:
    return False
  for x in lsub:
    if len(x) < col + 1:
      return False
  test = ''
  for i in range(0, 3):
    test += lsub[i][col]
  return is_match(test)


def down_diagonal(row, col, lstr):
  lsub = lstr[row:row + 3]
  if len(lsub) < 3:
    return False
  for x in lsub:
    if len(x) < col + 3:
      return False
  test = ''
  for i in range(0, 3):
    test += lsub[i][col + i]
  return is_match(test)


def up_diagonal(row, col, lstr):
  if row < 2:
    return False
  lsub = lstr[row - 2:row + 1]
  for x in lsub:
    if len(x) < col + 3:
      return False
  test = ''
  for i in range(0, 3):
    test += lsub[2 - i][col + i]
  return is_match(test)


inputs = readlines('input4-2.txt')

def check_x_formation(row, column, board):
  if len(board) < row + 3:  # Not enough rows for cross
    return False
  if len(board[row]) < column + 3:  # Not enough columns for cross
    return False
  return down_diagonal(row, column, inputs) and up_diagonal(
      row + 2, column, inputs)


total = 0
for row in range(0, len(inputs)):
  for column in range(0, len(inputs[row])):
    if check_x_formation(row, column, inputs):
      total += 1
print(f'Total: {total}')
