"""
Usage: python main.py dfa.txt
"""
import sys
import pdb
from itertools import product

def print_and_exit():
    sys.stderr.write(__doc__ + "\n")
    sys.exit(1)

if len(sys.argv) != 2:
    print_and_exit()

final_states = set()
states = set()
delta = dict()
with open(sys.argv[1], "r") as r:
    lines = r.readlines()
    alphabet = set( lines[0].strip().split() )
    final_states = set( lines[1].strip().split() )
    states |= final_states
    for l in lines[2:]:
        l = l.strip()
        toks = l.split()
        assert len(toks) == 3
        assert toks[1] in alphabet
        delta[toks[0],toks[1]] = toks[2]
        states.add(toks[0])
        states.add(toks[2])

marked = dict()
# For convenience do redundant work
for (Q, R) in product(states, states):
    if Q == R:
        marked[Q,R] = False
    else:
        marked[Q,R] = (Q in final_states and R not in final_states) or (R in final_states and Q not in final_states)

made_mark = True
while made_mark:
    made_mark = False
    for (Q, R) in product(states, states): # Again, for convenience do redundant work
        for c in alphabet:
            if Q == R: continue
            if marked[ delta[Q,c], delta[R,c] ] and not marked[Q,R]:
                made_mark = True
                marked[Q,R] = True

memberships = {state: {state} for state in states}
for (Q,R) in filter(lambda k: not marked[k], marked.keys()):
    memberships[Q].add(R)
    memberships[R].add(Q)

new_states = set()
for (_, v) in memberships.items():
    new_states.add(tuple(sorted(list(v))))
new_states = list(new_states)

print(marked)
print(new_states)
