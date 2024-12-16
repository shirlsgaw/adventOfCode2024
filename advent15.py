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
    #print(f'..Moving box {b} in direction {direction}')
    targets = set[Box]()
    to_move = list[Box]()
    to_move.append(b)

    while len(to_move) > 0:
      b = to_move.pop(0)
      #print(f'Considering {b}')
      targets.add(b)

      left_side = (b.left[0] + direction[0], b.left[1] + direction[1])
      right_side = (left_side[0] + 1, left_side[1])

      # Blocked from moving
      if (left_side[0], left_side[1]) in self.walls:
        return
      if (right_side[0], right_side[1]) in self.walls:
        return

      tmp1 = self.find_box(left_side[0], left_side[1])
      #print(f'..Adding left side of box {tmp1}')
      if tmp1 and tmp1 not in targets:
        to_move.append(tmp1)
      tmp2 = self.find_box(right_side[0], right_side[1])
      #print(f'..Adding right side of box {tmp2}')
      if tmp2 and tmp2 not in targets:
        to_move.append(tmp2)
      #print(f'..to_move: {to_move}')

    boxes_to_add = set[Box]()
    for b in targets:
      #print(f'..Removing {b}')
      self.boxes.remove(b)
      left = (b.left[0] + direction[0], b.left[1] + direction[1])
      right = (left[0] + 1, left[1])
      to_add = Box(left[0], left[1], right[0], right[1])
      boxes_to_add.add(to_add)
    #print(f'..Adding {boxes_to_add}')
    self.boxes.update(boxes_to_add)

  ####
  # Compute the sum of all box Goods Positioning System coordiante
  def sum_box_coordinates(self) -> int:
    sum = 0
    for b in self.boxes:
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
input = readlines('input15.txt')
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
    wmap.append(transformed_line)

warehouse = Warehouse(wmap)

instructions = list[str]()
for line in input:
  if line.startswith('#'):
    continue
  if len(line) == 0:
    continue
  instructions.append(line)
#warehouse.draw()

for line in instructions:
  for move in line:
    #print(f'Moving robot in direction {move}')
    direction = get_direction(move)
    warehouse.move_robot(direction)
    #warehouse.draw()

#warehouse.draw()

sum = warehouse.sum_box_coordinates()
print(f'Sum of box coordinates: {sum}')
