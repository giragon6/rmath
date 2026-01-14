from bitstring_graph import BitstringGraph

constraints = ["001"]
bsgraph = BitstringGraph(constraints)

def as_equation(a, s, xn_a, xn_s):
  eq = f"x(n) = {' + '.join([f"{k[0]}(n-{k[1]})" for k in xn_a])}"
  if len(xn_s) > 0:
    if len(eq) > 7:
      eq += ' - ' 
    eq += ' - '.join([f"{k[0]}(n-{k[1]})" for k in xn_s])
  if len(a) > 0:
    if len(eq) > 7:
      eq += ' + ' 
    eq += ' + '.join([f"{k[0]}(n-{k[1]})" for k in a])
  if len(s) > 0:
    if len(eq) > 7:
      eq += ' - ' 
    eq += ' - '.join([f"{k[0]}(n-{k[1]})" for k in s])
  return eq

def try_get_xn(s, xn, init, depth=1):
  new_s = s
  new_xn = xn
  for d in range(depth):
    can_get_xd = True
    while can_get_xd: # continue for multiple x(n-k)
      # check if addends of x(n) are present at depth d+1 
      # (e.g., 01(n-1) where d is 0)
      for r in init:
        if (r[0],d+1) not in s:
          can_get_xd = False
      # if all addends are present, remove them and replace with x(n-d-1)
      if can_get_xd:
        for r in init:
          s.remove((r[0],d+1))
        new_xn.append(('x',d+1))
  return new_s, new_xn
      
recs = bsgraph.recs
print(recs)
recs_no_depths = {s[0]: [t[0] for t in recs[s]] for s in recs}
print(recs_no_depths)

add = []
subtract = []
xn_add = []
xn_sub = []

def collapse(a, s, xn_a, xn_s, init):
  new_add, new_sub, new_xn_add, new_xn_sub = a, s, xn_a, xn_s
  if len(a) > 0:
    new_add, new_xn_add = try_get_xn(a, xn_a, init, depth=max([k[1] for k in a]))
  if len(s) > 0:
    new_sub, new_xn_sub = try_get_xn(s, xn_s, init, depth=max([k[1] for k in s]))
  return new_add, new_sub, new_xn_add, new_xn_sub

def expand(add, sub, recs):
  new_add = sum([[(r, s[1] + 1) for r in recs_no_depths[s[0]]] for s in add],[])
  new_sub = sum([[(r, s[1] + 1) for r in recs_no_depths[s[0]]] for s in sub],[])
  return new_add, new_sub

init = list(recs.keys())
print("Initial state: " + as_equation(init, subtract, xn_add, xn_sub))
add = sum([recs[s] for s in init],[])
print("Expanded: " + as_equation(add, subtract, xn_add, xn_sub))

while True:
  print("e = attempt expand, c = attempt collapse, as = attempt add & subtract")
  inp = input()
  match inp: 
    case "e":
      add, subtract = expand(add, subtract, recs)
    case "c":
      add, subtract, xn_add, xn_sub = collapse(add, subtract, xn_add, xn_sub, init)
    case "as":
      print("combo to add")
      combo = input()
      print("depth @ which to add")
      depth = input()
      add.append((combo, int(depth)))
      subtract.append((combo, int(depth)))
    case "exit": 
      break
  print()
  print(as_equation(add, subtract, xn_add, xn_sub))
  print()