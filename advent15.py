####
# Box
####
class Box:

  def __init__(self, left_x: int, left_y: int, right_x, right_y):
    self.left = (left_x, left_y)
    self.right = (right_x, right_y)
    if left_y != right_y:
      raise ValueError(f'Box must be horizontal, {self.left} -> {self.right}')

  def __repr__(self) -> str:
    return f'Box[{self.left}, {self.right}]'

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, Box):
      return False
    return (self.left == other.left and self.right == other.right)

  def __hash__(self) -> int:
    return hash((self.left, self.right))

  def contains_point(self, x: int, y: int) -> bool:
    if x < self.left[0] or x > self.right[0]:
      return False
    return y == self.left[1]


####
# Warehouse
####
class Warehouse:

  def __init__(self, original: list[str]):
    self.original = original
    self.walls, self.boxes, self.robot = self.parse_map(original)

  ####
  # Break the map into the locations of walls, boxes, and the robot
  ####
  def parse_map(
      self, original: list[str]
  ) -> tuple[set[tuple[int, int]], set[Box], tuple[int, int]]:
    walls = set[tuple[int, int]]()
    boxes = set[Box]()
    robot = tuple[int, int]()
    for y, line in enumerate(original):
      box_left = None
      for x, char in enumerate(line):
        if char == '#':
          walls.add((x, y))
        elif char == '[':
          box_left = (x, y)
        elif char == ']':
          if box_left is None:
            raise ValueError(
                f'Invalid map: ({x}, {y}) contains ] but no [ position set')
          boxes.add(Box(box_left[0], box_left[1], x, y))
          box_left = None
        elif char == '@':
          robot = (x, y)
    return walls, boxes, robot

  ####
  # Draw the map
  ####
  def draw(self):
    #print(f'Robot expected location: {self.robot}')
    for y in range(0, len(self.original)):
      row = ''
      for x in range(0, len(self.original[y])):
        if self.original[y][0] != '#':
          continue
        b = self.find_box(x, y)
        if b is not None:
          if b.left[0] == x and b.left[1] == y:
            row += '[]'
            x += 1
        elif (x, y) in self.walls:
          row += '#'
        elif (x, y) == self.robot:
          row += '@'
        else:
          row += '.'
      print(row)

  ####
  # Simulate the robot moving
  ####
  def move_robot(self, direction: tuple[int, int]):
    new_x = self.robot[0] + direction[0]
    new_y = self.robot[1] + direction[1]
    #print(f'Moving robot to ({new_x}, {new_y})')

    # Try to move the closest box to an empty space in the same
    # direction as the robot is supposed to move, freeing space
    # for the robot to move
    b = self.find_box(new_x, new_y)
    if b is not None:
      self.move_box(b, direction)

    if (new_x, new_y) in self.walls:
      #print('..Location in walls')
      return
    if b in self.boxes:
      #print('..Location still in boxes')
      return
    self.robot = (new_x, new_y)
    #print(f'...Moved robot to ({self.robot[0]}, {self.robot[1]})')

  ####
  # Find a box containing the point if it exists
  ####
  def find_box(self, x: int, y: int) -> Box | None:
    for box in self.boxes:
      if box.contains_point(x, y):
        return box
    return None

  ####
  # Attempt to move a box in the direction specified, recursively calling all adjacent
  # blocking boxs until the box is free (if possible)
  ####
  def move_box(self, b: Box, direction: tuple[int, int]):
    next_x = b.left.x + direction[0]
    next_y = b.left.y + direction[1]
    r_x = next_x + 1
    r_y = next_y + 1
    next_b = Box(next_x, next_y, r_x, r_y)

    # Can't move box
    if (next_x, next_y) in self.walls:
      return
    if next_b in self.boxes:
      self.move_box(next_b, direction)
    # The adjacent moves must have been unsuccessful, so we cannot move this box
    if next_b in self.boxes:
      return
    # Move box
    self.boxes.remove(b)
    self.boxes.add(next_b)

  ####
  # Compute the sum of all box Goods Positioning System coordiante
  def sum_box_coordinates(self) -> int:
    sum = 0
    for b in self.boxes:
      # TODO(sgaw): change to using the distance from the closest edge
      sum += b.left[0] + b.left[1] * 100
    return sum


####
# readlines: reads input from file into lines of strings
####
def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


####
# Translate a move into a vector representing the direction of movement
####
def get_direction(move: str) -> tuple[int, int]:
  if move == '<':
    return (-1, 0)
  elif move == '>':
    return (1, 0)
  elif move == '^':
    return (0, -1)
  elif move == 'v':
    return (0, 1)
  raise ValueError(f'Invalid move: {move}')


####
# Main
####
input = readlines('sample.txt')
wmap = list[str]()
for line in input:

  if line.startswith('#'):
    transformed_line = ''
    for char in line:
      if char == '#':
        transformed_line += '##'
      elif char == 'O':
        transformed_line += '[]'
      elif char == '.':
        transformed_line += '..'
      elif char == '@':
        transformed_line += '@.'
      else:
        raise ValueError(f'Invalid character: {char}')
    print(transformed_line)
    wmap.append(transformed_line)

warehouse = Warehouse(wmap)

instructions = list[str]()
for line in input:
  if line.startswith('#'):
    continue
  if len(line) == 0:
    continue
  instructions.append(line)
warehouse.draw()

instructions.clear()

for line in instructions:
  for move in line:
    direction = get_direction(move)
    warehouse.move_robot(direction)
#warehouse.draw()
sum = warehouse.sum_box_coordinates()
print(f'Sum of box coordinates: {sum}')
