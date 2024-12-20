from os import error
from typing import Self
from enum import Enum
from heapq import heappush
from heapq import heappop
from dataclasses import dataclass, field
import re
from functools import lru_cache

AVAILABLE_PATTERNS = None


####
# Find patterns that can combine to match this design
####
@lru_cache(maxsize=1028)
def find_patterns(design: str) -> list[str]:
  if AVAILABLE_PATTERNS is None:
    raise Exception('Available patterns not loaded')

  for pattern in AVAILABLE_PATTERNS:
    length = len(pattern)
    prefix = design[0:length]
    suffix = design[length:]

    # Base case found match
    if design == pattern:
      return [design]
    elif prefix == pattern:  # Recursive case
      matches = find_patterns(suffix)
      if len(matches) > 0:
        solution = [pattern]
        solution.extend(matches)
        return solution
    else:
      # Try another pattern
      pass
  return []


####
# Count all possible arrangement of patterns for this design
####


@lru_cache(maxsize=1028)
def find_all_matches(design: str) -> int:
  if AVAILABLE_PATTERNS is None:
    raise Exception('AVAILABLE_PATTERNS not initialized')
  num_solutions = 0
  for pattern in AVAILABLE_PATTERNS:
    length = len(pattern)
    prefix = design[0:length]
    suffix = design[length:]

    # Base case found match
    if design == pattern:
      num_solutions += 1
    elif prefix == pattern:  # Recursive case
      num_solutions += find_all_matches(suffix)
    else:
      # Try another pattern
      pass
  return num_solutions


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
input = readlines('input19.txt')

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

if available_patterns is None:
  raise Exception('Could not find patterns')
pattern_dict = dict[int, list[str]]()
for pattern in available_patterns:
  length = len(pattern)
  matches = pattern_dict.get(length, [])
  matches.append(pattern)
  pattern_dict[length] = matches
count = 0

AVAILABLE_PATTERNS = available_patterns

for design in desired_designs:
  solution = find_patterns(design)
  if len(solution) > 0:
    count += 1
print(f'Solution count: {count}')

total = 0
count_exists = 0
for design in desired_designs:
  matched_dict = dict[str, int]()
  num = find_all_matches(design)
  if num > 0:
    count_exists += 1
  total += num
print(f'Total: {total}, Exists: {count_exists}')
