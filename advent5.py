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
    
####
# Main
####
inputs = readlines('sample.txt')

increasing_rules, decreasing_rules, updates = extract_rules_and_updates(inputs)

print('Increasing Rules:')
debug_rules(increasing_rules)
print('Decreasing Rules:')
debug_rules(decreasing_rules, is_increasing=False)

#debug_updates(updates)

#print(has_match(23, 42, {23: [5]}, is_increasing=False))
#print(has_match(23, 4, {23: [51]}, is_increasing=True))

#print(has_match(23, 6, {23: [5]}, is_increasing=False))
#print(has_match(23, 5, {23: [5]}, is_increasing=False))
#print(has_match(23, 3, {23: [5]}, is_increasing=False))
#print(has_match(23, 3, {23: [10, 7, 5]}, is_increasing=False))

#print(has_match(23, 41, {23: [5]}, is_increasing=True))
#print(has_match(23, 51, {23: [5]}, is_increasing=True))
#print(has_match(23, 99, {23: [5]}, is_increasing=True))
#print(has_match(23, 99, {23: [5, 50, 75]}, is_increasing=True))

#print(has_match(75, 47, increasing_rules, is_increasing=True))
#print(has_match(75, 47, decreasing_rules, is_increasing=False))

#print(has_match(47, 75, increasing_rules, is_increasing=True))
#print(has_match(47, 75, decreasing_rules, is_increasing=False))

updates = [
          [75,47,61,53,29],
          [47, 53],
          [53, 47], # Rule violation 47 before 53
          [75, 47],
          [75, 97]  # Rule violation 75 before 97
         ]
for update in updates:
  print(update)
  for i in range(0, len(update)):
    for j in range(i+1, len(update)):
      if has_incr_match(update[j], update[i], increasing_rules):
        print(f' Rule violation: {update[i]} -> {update[j]}')
      if has_decr_match(update[j], update[i], decreasing_rules):
        print(f' Rule decr violation: {update[i]} -> {update[j]}')
total = 0
print(f'Total: {total}')
