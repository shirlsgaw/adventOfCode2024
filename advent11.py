from functools import lru_cache


def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


@lru_cache(maxsize=2048)
def blink(stone: str, iteration: int, target_iterations: int) -> int:
  #print(f'Blinking {stone} {iteration} of {target_iterations}, stored_results={stored_results}')
  if iteration == target_iterations:
    #print()
    return 1

  next_iter = iteration + 1

  if stone == '0':
    result = blink('1', next_iter, target_iterations)
    return result
  if len(stone) % 2 == 0:
    new_len = int(len(stone) / 2)
    stone1 = str(int(stone[:new_len]))
    stone2 = str(int(stone[new_len:]))
    result1 = blink(stone1, next_iter, target_iterations)
    result2 = blink(stone2, next_iter, target_iterations)
    return result1 + result2
  else:
    value = int(stone)
    result = blink(str(value * 2024), next_iter, target_iterations)
    return result


####
# Main
####
input = readlines('input11.txt')
stones = input[0].split(' ')
print(stones)

total = 0
for stone in stones:
  count = blink(stone, 0, 75)
  #print(stored_results)
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
