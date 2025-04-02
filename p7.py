grammar = {
    'S': [['A', 'B', 'C'], ['D']],
    'A': [['a'], ['ε']],
    'B': [['b'], ['ε']],
    'C': [['(', 'S', ')'], ['c']],
    'D': [['A', 'C']]
}

nonterminals = set(grammar.keys())

 
def is_terminal(symbol):
  
    return symbol not in nonterminals or symbol == 'ε'

 
first = { nt: set() for nt in nonterminals }
 
changed = True
while changed:
    changed = False
    for nt in nonterminals:
        for production in grammar[nt]:
            added_epsilon = True  
            for symbol in production:
                if is_terminal(symbol):
                    
                    if symbol != 'ε':
                        if symbol not in first[nt]:
                            first[nt].add(symbol)
                            changed = True
                    else:
                        if 'ε' not in first[nt]:
                            first[nt].add('ε')
                            changed = True
                    added_epsilon = (symbol == 'ε')
                    if not added_epsilon:
                        break
                else:
                    
                    before = len(first[nt])
                    first[nt].update(first[symbol] - {'ε'})
                    if len(first[nt]) > before:
                        changed = True
                    if 'ε' in first[symbol]:
                        added_epsilon = True
                    else:
                        added_epsilon = False
                        break
            if added_epsilon:
                if 'ε' not in first[nt]:
                    first[nt].add('ε')
                    changed = True

follow = { nt: set() for nt in nonterminals }
 
start_symbol = 'S'
follow[start_symbol].add('$')

changed = True
while changed:
    changed = False
    for nt in nonterminals:
        for production in grammar[nt]:
             for i, symbol in enumerate(production):
                if symbol in nonterminals:  # only nonterminals get follow set updates.
   
                    rest_first = set()
                    all_epsilon = True
                    for next_sym in production[i+1:]:
                        if is_terminal(next_sym):
                            if next_sym != 'ε':
                                rest_first.add(next_sym)
                            all_epsilon = (next_sym == 'ε')
                            if not all_epsilon:
                                break
                        else:
                            rest_first.update(first[next_sym] - {'ε'})
                            if 'ε' in first[next_sym]:
                                all_epsilon = True
                            else:
                                all_epsilon = False
                                break
                    before = len(follow[symbol])
                    follow[symbol].update(rest_first)
                    if all_epsilon:
                        follow[symbol].update(follow[nt])
                    if len(follow[symbol]) > before:
                        changed = True
def format_set(s):
    return "{" + ", ".join(sorted(s)) + "}"

print("FIRST Sets:")
for nt in sorted(nonterminals):
    print(f"First({nt}) = {format_set(first[nt])}")

print("\nFOLLOW Sets:")
for nt in sorted(nonterminals):
    print(f"Follow({nt}) = {format_set(follow[nt])}")
