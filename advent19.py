from typing import Self
from enum import Enum
from heapq import heappush
from heapq import heappop
from dataclasses import dataclass, field
import re


####
# Find patterns that can combine to match this design
####
def find_patterns(pattern_dict: dict[int, list[str]], unmatched: list[str],
                  design: str) -> tuple[list[str], list[str]]:
  # print('Finding patterns for design: ' + design)
  # Early terminate if we know there's no matches due to previous iterations
  if design in unmatched:
    #print(f'. Early terminate {design}')
    return ([], unmatched)

  prefix_lengths = [key for key in pattern_dict.keys()]
  prefix_lengths.sort(reverse=True)

  for prefix_length in prefix_lengths:
    #print(f'prefix_length: {prefix_length}')
    prefix = design[0:prefix_length]
    suffix = design[prefix_length:]
    for pattern in pattern_dict[prefix_length]:
      #print(f'.   pattern: {pattern}')
      if pattern == design:
        print(f'. Found exact match {pattern} for {design}')
        return [pattern], []
      if prefix == pattern:
        #print(f'.  Found prefix {pattern} for {design}')
        # Recursive case:
        matches, fails = find_patterns(pattern_dict, unmatched, suffix)
        if len(matches) > 0:
          #print(f'.  Found match [\'{pattern}\'] + {matches} = {design}')
          return [pattern] + matches, []
        else:
          #print(f'.  Failed to find match for {design}')
          unmatched.append(design)
          unmatched.extend(fails)
  #print(f'. No match found for *{design}*')
  unmatched.append(design)
  return [], unmatched


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

unmatched = list[str]()
for design in desired_designs:
  solution, fails = find_patterns(pattern_dict, unmatched, design)
  print(f'Solution: {solution} for {design}')
  if len(solution) > 0:
    count += 1
  else:
    print(f'No solution for {design}')
    unmatched.extend(fails)
    #break
print(f'Solution count: {count}')
