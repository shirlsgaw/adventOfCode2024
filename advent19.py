from os import error
from typing import Self
from enum import Enum
from heapq import heappush
from heapq import heappop
from dataclasses import dataclass, field
import re
from functools import lru_cache


####
# Find patterns that can combine to match this design
####
def find_patterns(available_patterns: list[str], unmatched: set[str],
                  design: str) -> tuple[list[str], set[str]]:
  #print('Finding patterns for design: ' + design)
  # Early terminate if we know there's no matches due to previous iterations
  if design in unmatched:
    #print(f'. Early terminate {design}')
    return ([], unmatched)

  for pattern in available_patterns:
    #print(f'  Checking pattern: {pattern}')
    length = len(pattern)
    prefix = design[0:length]
    suffix = design[length:]

    # Base case found match
    if design == pattern:
      return [design], unmatched
    elif prefix == pattern:  # Recursive case
      matches, fails = find_patterns(available_patterns, unmatched, suffix)
      unmatched.union(fails)
      if len(matches) > 0:
        return [pattern] + matches, unmatched
      else:
        # Prefix did not work, try another prefix
        unmatched.add(design)
    else:
      # Try another pattern
      pass
  #print(f'. No match found for *{design}*')
  unmatched.add(design)
  return [], unmatched


####
# Count all possible arrangement of patterns for this design
####
UNMATCHED = None
AVAILABLE_PATTERNS = None


@lru_cache(maxsize=1028)
def find_all_matches(design: str) -> int:
  if UNMATCHED is None:
    raise Exception('UNMATCHED not initialized')
  if AVAILABLE_PATTERNS is None:
    raise Exception('AVAILABLE_PATTERNS not initialized')
  if design in UNMATCHED:
    return 0
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
  matched_dict[design] = num_solutions
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
#print(f'Available patterns: {available_patterns}')
#print(f'Desired designs: {desired_designs}')

if available_patterns is None:
  raise Exception('Could not find patterns')
pattern_dict = dict[int, list[str]]()
for pattern in available_patterns:
  length = len(pattern)
  matches = pattern_dict.get(length, [])
  matches.append(pattern)
  pattern_dict[length] = matches
count = 0

available_patterns.sort(key=lambda x: len(x), reverse=True)
#desired_designs = ['rugbgbwwbbgrwrbubgugrgbrrbgwrbbgbwurwgrbr']
unmatched = set[str]()
solution_exists = list[str]()
for design in desired_designs:
  solution, fails = find_patterns(available_patterns, unmatched, design)
  unmatched.union(fails)
  #print(f'Solution: {solution} for {design}')
  if len(solution) > 0:
    count += 1
    solution_exists.append(design)
  else:
    pass
    #print(f'No solution for {design}')
    #break
num_exists = len(solution_exists)
print(f'Solution count: {num_exists}')

AVAILABLE_PATTERNS = available_patterns
UNMATCHED = unmatched
total = 0
count_exists = 0
for design in desired_designs:
  print(f'Design: {design}')
  matched_dict = dict[str, int]()
  num = find_all_matches(design)
  print(f'+Solution: {design} with {num} matches')
  if num > 0:
    count_exists += 1
  total += num
print(f'Total: {total}, Exists: {count_exists}')
