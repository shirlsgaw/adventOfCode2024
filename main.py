from os import read

def readlines(source):
  with open(source, "r") as f:
      lines = f.readlines()
      return list(map(lambda x: x.rstrip(), lines))

def is_match(str):
  return str == 'XMAS' or str == 'SAMX'

def horizontal(start, str):
  if len(str) < 4:
    return False
  sub = str[start:start+4]
  print(f' {sub}: {is_match(sub)}')
  return is_match(sub)

print('Hello world!')
inputs = readlines('test.txt')
for line in inputs:
  for i in range(0, len(line)-3):
    print(horizontal(i, line))
  

