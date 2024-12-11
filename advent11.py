from collections.abc import Generator


def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))

def blink(stone: str, iteration: int, target_iterations: int) -> int:
  print(f'Blinking {stone} {iteration} of {target_iterations}')
  if iteration == target_iterations:
    print()
    return 1
  if stone == '0':
    return blink('1', iteration + 1, target_iterations)
  if len(stone) % 2 == 0:
    new_len = int(len(stone) / 2)
    stone1 = stone[:new_len]
    stone2 = stone[new_len:]
    return blink(str(int(stone1)), iteration + 1, target_iterations) + blink(str(int(stone2)), iteration + 1, target_iterations)
  else:
    value = int(stone)
    return blink(str(value * 2024), iteration + 1, target_iterations)

####
# Main
####
input = readlines('sample.txt')
stones = input[0].split(' ')
print(stones)

total = 0
for stone in stones:
  count = blink(stone, 0, 6)
  total += count
print(f'Part 1: {total}')

#num_stones = blink('0', 0, 0)
#print(f'Part 1: {num_stones}')
#num_stones = blink('0', 0, 1)
#print(f'Part 1: {num_stones}')
#num_stones = blink('0', 0, 2)
#print(f'Part 1: {num_stones}')
#num_stones = blink('0', 0, 3)
#print(f'Part 1: {num_stones}')
#num_stones = blink('40', 0, 3)
#print(f'Part 1: {num_stones}')
