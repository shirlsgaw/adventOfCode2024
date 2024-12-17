from typing import Self
from enum import Enum
import re


####
# Computer
####
class Computer:

  def __init__(self, registers: dict[str, int], program: list[int]):
    self.registers = registers
    self.program = program

  def execute_program(self):
    pc = 0
    while pc < len(self.program):
      instruction = self.program[pc]
      if instruction in [0]:
        numerator = self.registers['A']
        power = self.program[pc + 1]
        denominator = 1 << power
        result = int(numerator / denominator)
        self.registers['A'] = result
        pc += 2
        print(f'. {pc} adv: {power}, {numerator} / {denominator} = {result}')


####
# readlines: reads input from file into lines of strings
####
def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


####
# Input to Computer
####
def parse_input(input: list[str]) -> Computer:
  registers = dict[str, int]()
  program = list[int]()
  for line in input:
    matches = re.findall(r'Register (.): (\d+)', line)
    if len(matches) > 0:
      match = matches[0]
      registers[match[0]] = int(match[1])
    matches = re.findall(r'Program: (.+)', line)
    if len(matches) > 0:
      match = matches[0]
      program = list(map(int, match.split(',')))
  return Computer(registers, program)


####
# Main
####
input = readlines('sample.txt')
computer = Computer(registers={'A': 10}, program=[0, 2])  #parse_input(input)
print(f'Registers: {computer.registers}')
print(f'Program: {computer.program}')

computer.execute_program()
