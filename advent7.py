from os import read


def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))

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
print(totals_list)
print(operands_list)
print('Day 7')
