from os import read

def readlines(source):
  with open(source, "r") as f:
      lines = f.readlines()
      return list(map(lambda x: x.rstrip(), lines))

def is_match(str):
  result = (str == 'XMAS' or str == 'SAMX')
  print(f' {str}: {result}')
  return result

def horizontal(start, str):
  if len(str) < 4:
    return False
  sub = str[start:start+4]
  print(f' {sub}: {is_match(sub)}')
  return is_match(sub)

def vertical(row, col, lstr):
  if len(lstr) < 4:
    return False
  lsub = lstr[row:]
  for x in lsub:
    if len(x) < col + 1:
      return False
  test = ''
  for i in range(0,4):
    test += lsub[i][col]
  print(f' {test}: {is_match(test)}')
  return is_match(test)

def down_diagonal(row, col, lstr):
  print(lstr)
  if len(lstr) < 4:
    print('rows')
    return False
  lsub = lstr[row:row+4]
  for x in lsub:
    if len(x) < col + 4:
      print(f'cols: {x}')
      return False
  test = ''
  for i in range(0,4):
    test += lsub[i][col+i]
  return is_match(test)

def up_diagonal(row, col, lstr):
  print(lstr)
  if row < 3:
    print('rows')
    return False
  lsub = lstr[row-3:row+1]
  print(lsub)
  for x in lsub:
    if len(x) < col + 4:
      print(f'cols: {x}')
      return False
  test = ''
  for i in range(0,4):
    print(f' {3-i},{col+i}')
    test += lsub[3-i][col+i]
  return is_match(test)
  
print('Hello world!')
tests = [['1X11',
          '2M22',
          '3A33',
          '4S44'],
         ['0000',
          '1X11',
          '2M22',
          '3A33',
          '4S44'],
         ['00000',
          '1X111',
          '22M22',
          '333A3',
          '4444S']
        ]
inputs = readlines('test.txt')
#print(vertical(0,0,tests[0]))
#print(vertical(0,1,tests[0]))
#print(vertical(0,1,tests[1]))
#print(vertical(1,1,tests[1]))
#print(down_diagonal(0,0, tests[0]))
#print(down_diagonal(1,1, tests[2]))
print(up_diagonal(1,1, tests[2]))
print(up_diagonal(3,1, tests[2]))
print(up_diagonal(3,1, inputs))
#for line in inputs:
#  for i in range(0, len(line)-3):
#    print(horizontal(i, line))
  

