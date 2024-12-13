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


####
# Game
####
class Game:

  def __init__(self, buttons: tuple[Button, Button], prize: Prize):
    self.buttons = buttons
    self.prize = prize

  def __repr__(self):
    return f"Game({self.buttons}, {self.prize})"

  def __eq__(self, other):
    return (self.buttons, self.prize) == (other.buttons, other.prize)


####
# readlines: reads input from file into lines of strings
####
def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


####
# Parses a string into Button or Prize
####
def parse(line: str) -> Union[Button, Prize, None]:
  tmp = line.split(' ')
  if tmp[0].startswith('Button'):
    return Button(label=tmp[1], x_label=tmp[2], y_label=tmp[3])
  if tmp[0].startswith('Prize'):
    return Prize(x_label=tmp[1], y_label=tmp[2])
  return None


####
# Main
####
input = readlines('hint.txt')

button1 = None
button2 = None
prize = None
games = list[Game]()
for line in input:
  result = parse(line)
  if result is None and button1 is not None and button2 is not None and prize is not None:
    game = Game(buttons=(button1, button2), prize=prize)
    games.append(game)
    button1 = None
    button2 = None
    prize = None
  if isinstance(result, Button):
    if button1 is None:
      button1 = result
    else:
      button2 = result
  if isinstance(result, Prize):
    prize = result

# The last game has no blank line divider
if button1 is not None and button2 is not None and prize is not None:
  game = Game(buttons=(button1, button2), prize=prize)
  games.append(game)
print(games)
