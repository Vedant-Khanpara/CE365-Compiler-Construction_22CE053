# Define the grammar as a dictionary.
# Each nonterminal maps to a list of productions.
# Each production is represented as a list of symbols.
grammar = {
    'S': [['A', 'B', 'C'], ['D']],
    'A': [['a'], ['ε']],
    'B': [['b'], ['ε']],
    'C': [['(', 'S', ')'], ['c']],
    'D': [['A', 'C']]
}

nonterminals = set(grammar.keys())

# Helper function: Check if a symbol is terminal.
def is_terminal(symbol):
    # ε is treated as a special terminal representing epsilon.
    return symbol not in nonterminals or symbol == 'ε'

# Initialize FIRST sets.
first = { nt: set() for nt in nonterminals }
# Also for terminals, first(symbol) = { symbol }.
# (We don't really need to store these for the algorithm.)

# Iteratively compute FIRST sets.
changed = True
while changed:
    changed = False
    for nt in nonterminals:
        for production in grammar[nt]:
            # For each production A -> X1 X2 ... Xn,
            # add FIRST(X1) minus epsilon, then if X1 derives ε, add FIRST(X2), etc.
            added_epsilon = True  # assume all symbols so far derive ε.
            for symbol in production:
                if is_terminal(symbol):
                    # If symbol is terminal:
                    if symbol != 'ε':
                        if symbol not in first[nt]:
                            first[nt].add(symbol)
                            changed = True
                    else:
                        # symbol is ε
                        if 'ε' not in first[nt]:
                            first[nt].add('ε')
                            changed = True
                    added_epsilon = (symbol == 'ε')
                    if not added_epsilon:
                        break
                else:
                    # symbol is nonterminal: add first(symbol) except ε.
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

# Initialize FOLLOW sets.
follow = { nt: set() for nt in nonterminals }
# For the start symbol, add '$'
start_symbol = 'S'
follow[start_symbol].add('$')

changed = True
while changed:
    changed = False
    for nt in nonterminals:
        for production in grammar[nt]:
            # For each production A -> X1 X2 ... Xn,
            # for every nonterminal Xi, add FIRST(Xi+1...Xn) minus ε to FOLLOW(Xi)
            # If Xi+1...Xn derives ε, then add FOLLOW(A) to FOLLOW(Xi)
            for i, symbol in enumerate(production):
                if symbol in nonterminals:  # only nonterminals get follow set updates.
                    # Compute FIRST of the rest of production.
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

# For neat printing, sort the sets.
def format_set(s):
    return "{" + ", ".join(sorted(s)) + "}"

print("FIRST Sets:")
for nt in sorted(nonterminals):
    print(f"First({nt}) = {format_set(first[nt])}")

print("\nFOLLOW Sets:")
for nt in sorted(nonterminals):
    print(f"Follow({nt}) = {format_set(follow[nt])}")
