from collections.abc import Generator
from typing import Union


####
# Button
####
class Button:

  def __init__(self, label: str, x_label: str, y_label: str):
    print(label)
    index = label.index(':')
    self.label = label[:index]

    index = x_label.index(',')
    x_label = x_label[:index]
    tmp = x_label.split('+')
    self.x = int(tmp[1])

    tmp = y_label.split('+')
    self.y = int(tmp[1])

    if self.label == 'A':
      self.cost = 3
    else:
      self.cost = 1

  def __repr__(self):
    return f"Button({self.label}, ({self.x}, {self.y}), cost = {self.cost})"

  def __eq__(self, other):
    return (self.x, self.y, self.label, self.cost) == (other.x, other.y,
                                                       other.label, other.cost)

  def __hash__(self):
    return hash((self.x, self.y, self.label, self.cost))


####
# Prize
####
class Prize:

  def __init__(self, x_label: str, y_label: str):

    index = x_label.index(',')
    x_label = x_label[:index]
    tmp = x_label.split('=')
    self.x = int(tmp[1])

    tmp = y_label.split('=')
    self.y = int(tmp[1])

  def __repr__(self):
    return f"Prize(({self.x}, {self.y}))"

  def __eq__(self, other):
    return (self.x, self.y) == (other.x, other.y)


def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


####
# Parses the input into Buttons and Prizes
####
def parse(input: list[str]) -> Generator[Union[Button, Prize], None, None]:
  for line in input:
    tmp = line.split(' ')
    if tmp[0].startswith('Button'):
      yield Button(label=tmp[1], x_label=tmp[2], y_label=tmp[3])
    if tmp[0].startswith('Prize'):
      yield Prize(x_label=tmp[1], y_label=tmp[2])


####
# Main
####
input = readlines('hint.txt')
for line in parse(input):
  print(line)
