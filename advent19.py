from typing import Self
from enum import Enum
from heapq import heappush
from heapq import heappop
from dataclasses import dataclass, field
import re


####
# Find patterns that can combine to match this design
####
def find_patterns(available_patterns: list[str], design: str) -> list[str]:
  min_length = None
  for pattern in available_patterns:
    if min_length is None or len(pattern) < min_length:
      min_length = len(pattern)
  if min_length is None:
    raise Exception('Could not detect minimum')

  # Base case: all patterns are too long for this design
  if len(design) < min_length:
    #print(f'Base case 1: *{design}* is too short')
    return []

  for pattern in available_patterns:
    if design.startswith(pattern):
      #print(f'Found prefix {pattern} for {design}')
      remaining_design = design[len(pattern):]
      # Base case 2: found exact match
      if len(remaining_design) == 0:
        return [pattern]

      # Recursive case:
      matches = find_patterns(available_patterns, remaining_design)
      if len(matches) > 0:
        #print(f'. Found match [\'{pattern}\'] + {matches} = {design}')
        return [pattern] + matches
      else:
        #print(f'. No match found for {pattern} + {remaining_design}')
        return []
  return []


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
desired_designs = list[str]()
for line in input:
  tokens = line.split(',')
  if len(tokens) > 1:
    available_patterns = list[str]()
    for token in tokens:
      available_patterns.append(token.lstrip())
  elif len(line) > 0:
    desired_designs.append(line)
print(f'Available patterns: {available_patterns}')
print(f'Desired designs: {desired_designs}')

if available_patterns is None:
  raise Exception('Could not find patterns')
available_patterns.sort(key=len, reverse=True)
#print(f'Sorted patterns: {available_patterns}')
count = 0
for design in desired_designs:
  solution = find_patterns(available_patterns, design)
  print(f'Solution: {solution} for {design}')
  if len(solution) > 0:
    count += 1
print(f'Solution count: {count}')
