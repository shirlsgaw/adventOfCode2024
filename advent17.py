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

  ####
  # execute_program
  ####
  def execute_program(self):
    pc = 0
    while pc < len(self.program):
      instruction = self.program[pc]
      if instruction == 0:
        value = self.registers['A']
        shift = self.combo_operand(self.program[pc + 1])
        result = value >> shift
        self.registers['A'] = result
        pc += 2
      elif instruction == 1:
        operand = self.registers['B']
        literal = self.program[pc + 1]
        self.registers['B'] = operand ^ literal
        pc += 2

  ####
  # operand: translate combo operand to its value
  ####
  def combo_operand(self, combo_operand: int) -> int:
    if combo_operand in [0, 1, 2, 3, 7]:
      return combo_operand
    elif combo_operand == 4:
      return self.registers['A']
    elif combo_operand == 5:
      return self.registers['B']
    elif combo_operand == 6:
      return self.registers['C']
    else:
      raise ValueError(f'Invalid operand: {combo_operand}')


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
computer = Computer(registers={'A': 12}, program=[0, 2])  #parse_input(input)
print(f'Registers: {computer.registers}')
print(f'Program: {computer.program}')

computer.execute_program()
print(f'Registers: {computer.registers}')
result = 12 >> 2
print(result)
