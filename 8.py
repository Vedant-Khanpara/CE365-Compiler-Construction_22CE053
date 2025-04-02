# Predictive Parsing Table Construction and LL(1) Grammar Validation
#
# Grammar:
#   S → A B C | D
#   A → a | ε
#   B → b | ε
#   C → ( S ) | c
#   D → A C
#
# Given FIRST sets:
#   FIRST(S) = {a, b, (, c}
#   FIRST(A) = {a, ε}
#   FIRST(B) = {b, ε}
#   FIRST(C) = {(, c}
#   FIRST(D) = {a, (, c}
#
# Given FOLLOW sets:
#   FOLLOW(S) = {), $}
#   FOLLOW(A) = {b, (, c}
#   FOLLOW(B) = {(, c}
#   FOLLOW(C) = {), $}
#   FOLLOW(D) = {), $}
#
# Terminals (we consider): a, b, (, c, ), $
#
# This script constructs the predictive parsing table, reports if the grammar is LL(1),
# prints the table, and then validates test strings provided by the user.

# Define the grammar as a dictionary:
grammar = {
    'S': [['A', 'B', 'C'], ['D']],
    'A': [['a'], ['ε']],
    'B': [['b'], ['ε']],
    'C': [['(', 'S', ')'], ['c']],
    'D': [['A', 'C']]
}

# Provided FIRST and FOLLOW sets
first = {
    'S': {'a', 'b', '(', 'c'},
    'A': {'a', 'ε'},
    'B': {'b', 'ε'},
    'C': {'(', 'c'},
    'D': {'a', '(', 'c'}
}

follow = {
    'S': {')', '$'},
    'A': {'b', '(', 'c'},
    'B': {'(', 'c'},
    'C': {')', '$'},
    'D': {')', '$'}
}

# Nonterminals and terminals:
nonterminals = list(grammar.keys())
terminals = {'a', 'b', '(', 'c', ')', '$'}

# Initialize predictive parsing table as a nested dictionary.
# table[nonterminal][terminal] will hold a production (list of symbols) or None.
table = {}
for nt in nonterminals:
    table[nt] = {}
    for t in terminals:
        table[nt][t] = None

# Helper function: Compute FIRST of a production (list of symbols)
def first_of_production(prod):
    result = set()
    for symbol in prod:
        if symbol in first:  # symbol is a nonterminal
            result.update(first[symbol] - {'ε'})
            if 'ε' not in first[symbol]:
                break
        else:
            # symbol is terminal (or ε)
            if symbol != 'ε':
                result.add(symbol)
            break
    else:
        result.add('ε')
    return result

# Fill in the parsing table:
LL1 = True  # Flag to check if grammar is LL(1)
for nt in nonterminals:
    for production in grammar[nt]:
        prod_first = first_of_production(production)
        for t in prod_first:
            if t != 'ε':
                if table[nt][t] is not None:
                    print("Conflict in table at", nt, t, ". Grammar is not LL(1).")
                    LL1 = False
                table[nt][t] = production
        if 'ε' in prod_first:
            for t in follow[nt]:
                if table[nt][t] is not None:
                    print("Conflict in table at", nt, t, ". Grammar is not LL(1).")
                    LL1 = False
                table[nt][t] = production

# Print the predictive parsing table
print("Predictive Parsing Table:")
for nt in sorted(nonterminals):
    print(nt, ":", end=" ")
    for t in sorted(terminals):
        prod = table[nt][t]
        if prod is not None:
            # Join production symbols into a string for display.
            print(f"{t}: {''.join(prod)}", end="  ")
    print()

if LL1:
    print("\nGrammar is LL(1)")
else:
    print("\nGrammar is NOT LL(1)")

# Parsing function using the predictive parsing table
def parse_input(input_str):
    # Append end-marker '$' to the input
    input_str = input_str + '$'
    stack = ['$', 'S']  # Initialize stack with end-marker and start symbol S
    index = 0  # Current index in input_str

    while stack:
        top = stack.pop()
        current = input_str[index]
        if top in terminals:
            if top == current:
                index += 1
            else:
                return False
        else:
            # top is a nonterminal; lookup the production in the table
            prod = table[top].get(current)
            if prod is None:
                return False
            if prod != ['ε']:
                # Push production symbols in reverse order onto the stack
                for symbol in reversed(prod):
                    stack.append(symbol)
    return index == len(input_str)

# Allow the user to test multiple input strings.
while True:
    test_str = input("\nEnter string to validate (or 'exit' to quit): ")
    if test_str.lower() == "exit":
        break
    if parse_input(test_str):
        print("Valid string")
    else:
        print("Invalid string")
