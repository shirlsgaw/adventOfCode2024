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
    self.output = ''

  ####
  # execute_program
  ####
  def execute_program(self):
    pc = 0
    while pc < len(self.program):
      instruction = self.program[pc]
      if instruction == 0:  # adv
        self.div('A', self.program[pc + 1])
        pc += 2
      elif instruction == 1:  # bxl
        literal = self.program[pc + 1]
        self.bxl(literal)
        pc += 2
      elif instruction == 2:  # bst
        self.bst(self.program[pc + 1])
        pc += 2
      elif instruction == 3:  # jnz
        pc = self.jnz(pc)
      elif instruction == 4:  # bxc
        self.bxc(self.program[pc + 1])
        pc += 2
      elif instruction == 5:  # out
        self.out(self.program[pc + 1])
        pc += 2
      elif instruction == 6:  # bdv
        self.div('B', self.program[pc + 1])
        pc += 2
      elif instruction == 7:  # cdv
        self.div('C', self.program[pc + 1])
        pc += 2
    print(f'Output: {self.output}')

  ####
  # bxc: XOR on registers B and C
  ####
  def bxc(self, _: int):
    self.registers['B'] = self.registers['B'] ^ self.registers['C']

  ####
  # out: outputs combo operand modulo 8
  ####
  def out(self, combo_operand: int):
    value = self.combo_operand(combo_operand) % 8
    if len(self.output) == 0:
      self.output = str(value)
    else:
      self.output += ',' + str(value)

  ####
  # div: shift right for register
  ####
  def div(self, register: str, combo_operand: int):
    value = self.registers[register]
    shift = self.combo_operand(combo_operand)
    self.registers[register] = value >> shift

  ####
  # bxl: XOR register B
  ####
  def bxl(self, literal: int):
    operand = self.registers['B']
    self.registers['B'] = operand ^ literal

  ####
  # bst: shift register B
  ####
  def bst(self, combo_operand: int):
    value = self.combo_operand(combo_operand)
    self.registers['B'] = value % 8

  ####
  # jnz: jump command
  ####
  def jnz(self, curr_pc) -> int:
    value = self.registers['A']
    if value == 0:
      return curr_pc + 2
    else:
      return self.program[curr_pc + 1]

  ####
  # operand: translate combo operand to its value
  ####
  def combo_operand(self, combo_operand: int) -> int:
    if combo_operand in [0, 1, 2, 3]:
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
computer = Computer(registers={
    'A': 2024,
    'B': 2024,
    'C': 43690
},
                    program=[0, 1, 5, 4, 3, 0])  #parse_input(input)
print(f'Registers: {computer.registers}')
print(f'Program: {computer.program}')

computer.execute_program()
print(f'Registers: {computer.registers}')
