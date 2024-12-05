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
    increasing_rules[key] = compact_rule(values)
  for key, values in decreasing_rules.items():
    decreasing_rules[key] = compact_rule(values, is_increasing=False)
    
  return increasing_rules, decreasing_rules, updates


def debug_rules(rules, is_increasing=True):
  for key in rules:
    print(f'Rule: {key}: {rules[key]}')

def debug_updates(updates):
  for update in updates:
    print(f'Update: {update}')

def compact_rule(values, is_increasing=True):
  values.sort()
  if not is_increasing:
    values.reverse()
  value = values.pop()
  return value

def has_match(page1, page2, rules, is_increasing=True):
  if is_increasing and page2 < page1:
    print(f' Increasing wrong order: {page1} < {page2}')
    return False
  if not is_increasing and page2 > page1:
    print(f' Decreasing wrong order: {page1} > {page2}')
    return False
  if page1 not in rules:
    print(f' No rule for {page1}')
    return False
  rule_value = rules[page1]
  print(f' Rule: {page1} -> {rule_value}, {page2}')
  if is_increasing:
    return page2 <= rule_value
  else:
    return page2 >= rule_value

####
# Main
####
inputs = readlines('sample.txt')

increasing_rules, decreasing_rules, updates = extract_rules_and_updates(inputs)

#print('Increasing Rules:')
#debug_rules(increasing_rules)
#print('Decreasing Rules:')
#debug_rules(decreasing_rules, is_increasing=False)

#debug_updates(updates)

#print(has_match(23, 42, {23: 5}, is_increasing=False))
#print(has_match(23, 4, {23: 51}, is_increasing=True))

#print(has_match(23, 6, {23: 5}, is_increasing=False))
#print(has_match(23, 3, {23: 5}, is_increasing=False))
#print(has_match(23, 5, {23: 5}, is_increasing=False))

#print(has_match(23, 41, {23: 51}, is_increasing=True))
#print(has_match(23, 99, {23: 51}, is_increasing=True))
#print(has_match(23, 51, {23: 51}, is_increasing=True))
total = 0
print(f'Total: {total}')
