#guard = GuardLocation(0, 0, Direction.EAST).move(['..'])
#print(f'New guard: {guard}') # expect (1,0) EAST
test = is_outside(guard.x, guard.y, ['..#'])
print(f'  Is outside: {test}')
test = is_outside(guard.x, guard.y, ['.'])
print(f'  Is outside: {test}')

guard = guard.move(['..#']) # Expect (1,1) SOUTH
print(f'New guard: {guard}')
test = is_outside(guard.x, guard.y, ['.'])
print(f'  Is outside: {test}')

guard = GuardLocation(1, 0, Direction.WEST).move(['..'])
print(f'New guard: {guard}') # Expect (0,0) WEST

# Expect (1, -1) NORTH
guard = GuardLocation(1, 0, Direction.WEST).move(['#.'])   
print(f'New guard: {guard}')
