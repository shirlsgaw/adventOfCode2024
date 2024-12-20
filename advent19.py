from typing import Self
from enum import Enum
from heapq import heappush
from heapq import heappop
from dataclasses import dataclass, field
import re


####
# readlines: reads input from file into lines of strings
####
def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


####
# Main
####
input = readlines('sample.txt')

available_patterns = None
min_length = None
patterns_dict = dict[int, list[str]]()
desired_designs = list[str]()
for line in input:
  tokens = line.split(',')
  if len(tokens) > 1:
    available_patterns = tokens
    for pattern in available_patterns:
      length = len(pattern)
      if min_length is None or length < min_length:
        min_length = length
      matches = patterns_dict.get(length, list[str]())
      matches.append(pattern)
  elif len(line) > 0:
    desired_designs.append(line)
print(f'Available patterns: {available_patterns}')
print(f'Desired designs: {desired_designs}')
