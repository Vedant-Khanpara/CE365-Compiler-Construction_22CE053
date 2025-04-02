grammar = {
    'S': [['A', 'B', 'C'], ['D']],
    'A': [['a'], ['ε']],
    'B': [['b'], ['ε']],
    'C': [['(', 'S', ')'], ['c']],
    'D': [['A', 'C']]
}

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


nonterminals = list(grammar.keys())
terminals = {'a', 'b', '(', 'c', ')', '$'}

table = {}
for nt in nonterminals:
    table[nt] = {}
    for t in terminals:
        table[nt][t] = None
def first_of_production(prod):
    result = set()
    for symbol in prod:
        if symbol in first:  
            result.update(first[symbol] - {'ε'})
            if 'ε' not in first[symbol]:
                break
        else:
             
            if symbol != 'ε':
                result.add(symbol)
            break
    else:
        result.add('ε')
    return result

 
LL1 = True   
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

print("Predictive Parsing Table:")
for nt in sorted(nonterminals):
    print(nt, ":", end=" ")
    for t in sorted(terminals):
        prod = table[nt][t]
        if prod is not None:
           
            print(f"{t}: {''.join(prod)}", end="  ")
    print()

if LL1:
    print("\nGrammar is LL(1)")
else:
    print("\nGrammar is NOT LL(1)")

 
def parse_input(input_str):
     
    input_str = input_str + '$'
    stack = ['$', 'S']  
    index = 0 

    while stack:
        top = stack.pop()
        current = input_str[index]
        if top in terminals:
            if top == current:
                index += 1
            else:
                return False
        else:
             
            prod = table[top].get(current)
            if prod is None:
                return False
            if prod != ['ε']:
                
                for symbol in reversed(prod):
                    stack.append(symbol)
    return index == len(input_str)

 
while True:
    test_str = input("\nEnter string to validate (or 'exit' to quit): ")
    if test_str.lower() == "exit":
        break
    if parse_input(test_str):
        print("Valid string")
    else:
        print("Invalid string")
