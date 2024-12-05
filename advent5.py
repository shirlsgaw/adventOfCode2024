from os import read


def readlines(source):
  with open(source, "r") as f:
    lines = f.readlines()
    return list(map(lambda x: x.rstrip(), lines))


def extract_rules_and_updates(lines):
  rules = list()
  increasing_rules = dict()
  decreasing_rules = dict()
  updates = list()
  for line in lines:
    if line.find('|') > -1:
      rule = list(map(lambda x: int(x), line.split('|', maxsplit=1)))
      first, second = rule
      if first < second:
        temp = increasing_rules.pop(first, list())
        temp.append(second)
        increasing_rules[first] = temp
      else:
        temp = decreasing_rules.pop(first, list())
        temp.append(second)
        decreasing_rules[first] = temp
      rules.append(rule)
    elif line.find(',') > -1:
      update = list(map(lambda x: int(x), line.split(',')))
      updates.append(update)

  # Remove overlapping rules
  
  for key, values in increasing_rules.items():
    values.sort()
  for key, values in decreasing_rules.items():
    values.sort(reverse=True)
    
  return increasing_rules, decreasing_rules, updates


def debug_rules(rules, is_increasing=True):
  for key in rules:
    print(f'Rule: {key}: {rules[key]}')

def debug_updates(updates):
  for update in updates:
    print(f'Update: {update}')

def has_decr_match(page1, page2, rules):
  if page2 > page1:
    return False
  if page1 not in rules:
    return False
  valuesl = rules[page1]
  return page2 in valuesl
  
def has_incr_match(page1, page2, rules):
  if page2 < page1:
    return False
  if page1 not in rules:
    return False
  valuesl = rules[page1]
  return page2 in valuesl

def swap(i, j, arr):
  tmp = arr[j]
  arr[j] = arr[i]
  arr[i] = tmp

####
# Main
####
inputs = readlines('input5.txt')

increasing_rules, decreasing_rules, updates = extract_rules_and_updates(inputs)

#print('Increasing Rules:')
#debug_rules(increasing_rules)
#print('Decreasing Rules:')
#debug_rules(decreasing_rules, is_increasing=False)

total = 0
for update in updates:
  has_violation = False
  orig = update.copy()
  for i in range(0, len(update)):
    for j in range(i+1, len(update)):
      if has_incr_match(update[j], update[i], increasing_rules):
        #print(f' Rule violation: {update[i]} -> {update[j]}')
        has_violation = True
        swap(i,j, update)
      elif has_decr_match(update[j], update[i], decreasing_rules):
        #print(f' Rule decr violation: {update[i]} -> {update[j]}')
        has_violation = True
        swap(i,j,update)
  #if has_violation:
  #  print(f' {orig}: {update}')
  mid = int(len(update) / 2)
  total += update[mid]
    

print(f'Total: {total}')
