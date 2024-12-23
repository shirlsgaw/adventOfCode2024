from collections.abc import Generator
from typing import Union
from numpy._typing import _UnknownType
from scipy import optimize
import re
from scipy.optimize import NonlinearConstraint, OptimizeResult
import numpy as np


####
# Button
####
class Button:

  def __init__(self, label: str, x: int, y: int):
    self.label = label
    self.x = x
    self.y = y

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

  def __init__(self, x: int, y: int):
    self.x = 10000000000000 + x
    self.y = 10000000000000 + y

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

  def sq_euclidian_distance(self, multiplier1: int, multiplier2: int) -> int:
    delta_x = self.buttons[0].x * multiplier1 + self.buttons[
        1].x * multiplier2 - self.prize.x
    delta_y = self.buttons[0].y * multiplier1 + self.buttons[
        1].y * multiplier2 - self.prize.y
    return (delta_x * delta_x + delta_y * delta_y)

  def cost(self, x) -> float:
    return self.buttons[0].cost * x[0] + self.buttons[1].cost * x[1]

  def solve2(self) -> list[int]:
    a = self.buttons[0]
    b = self.buttons[1]
    c = self.prize
    m = -(b.y * c.x - b.x * c.y) * 1.0 / (a.y * b.x - a.x * b.y)
    n = (a.y * c.x - a.x * c.y) * 1.0 / (a.y * b.x - a.x * b.y)
    return [round(m), round(n)]

  def check(self, x: list[int]) -> bool:
    return self.sq_euclidian_distance(x[0], x[1]) == 0


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
  matches = re.findall(r'Button (A|B): X\+(\d+), Y\+(\d+)', line)
  if len(matches) > 0:
    match = matches[0]
    return Button(label=match[0], x=int(match[1]), y=int(match[2]))

  matches = re.findall(r'Prize: X\=(\d+), Y\=(\d+)', line)
  if len(matches) > 0:
    match = matches[0]
    return Prize(x=int(match[0]), y=int(match[1]))
  return None


####
# Main
####
input = readlines('input13.txt')

button1 = None
button2 = None
prize = None
games = list[Game]()

index = 0
while index < len(input):
  line = input[index]
  if len(line) == 0:
    index += 1
  elif index + 2 < len(input):
    button1 = parse(input[index])
    if not isinstance(button1, Button):
      raise Exception(f"Expected button at index {index}")
    button2 = parse(input[index + 1])
    if not isinstance(button2, Button):
      raise Exception(f"Expected button at index {index + 1}")
    prize = parse(input[index + 2])
    if not isinstance(prize, Prize):
      raise Exception(f"Expected prize at index {index + 2}")
    game = Game(buttons=(button1, button2), prize=prize)
    games.append(game)
    index += 3

total_cost = 0
for game in games:
  result = game.solve2()

  if len(result) > 0:
    #print(f". Solution: {result}")
    check_result = game.check(result)
    if check_result:
      cost = game.cost(result)
      #print(f"cost={cost}, result={result}")
      total_cost += cost
print('Total cost:' + str(total_cost))
