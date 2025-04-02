import re

# Global variables used by the parser.
tokens = []
pos = 0
temp_counter = 0
quadruple_table = []  # List to hold quadruples

def new_temp():
    """Generate a new temporary variable name."""
    global temp_counter
    temp_counter += 1
    return f"t{temp_counter}"

def tokenize(expr):
    """
    Tokenizes the input expression into numbers, operators, and parentheses.
    Supports integers and decimals.
    """
    token_pattern = r'\d+\.\d+|\d+|[+\-*/()]'
    return re.findall(token_pattern, expr)

# Parsing functions based on the grammar (with left recursion eliminated):

def parse_E():
    """E → T E'"""
    left = parse_T()
    if left is None:
        return None
    return parse_Eprime(left)

def parse_Eprime(inherited):
    """E' → + T {generate '+'} | - T {generate '-'} | ε"""
    global pos
    while pos < len(tokens) and tokens[pos] in ['+', '-']:
        op = tokens[pos]
        pos += 1
        right = parse_T()
        if right is None:
            return None
        temp = new_temp()
        quadruple_table.append((op, inherited, right, temp))
        inherited = temp
    return inherited

def parse_T():
    """T → F T'"""
    left = parse_F()
    if left is None:
        return None
    return parse_Tprime(left)

def parse_Tprime(inherited):
    """T' → * F {generate '*'} | / F {generate '/'} | ε"""
    global pos
    while pos < len(tokens) and tokens[pos] in ['*', '/']:
        op = tokens[pos]
        pos += 1
        right = parse_F()
        if right is None:
            return None
        temp = new_temp()
        quadruple_table.append((op, inherited, right, temp))
        inherited = temp
    return inherited

def parse_F():
    """F → ( E ) | digit"""
    global pos
    if pos >= len(tokens):
        return None
    token = tokens[pos]
    if token == '(':
        pos += 1  # consume '('
        result = parse_E()
        if result is None:
            return None
        if pos >= len(tokens) or tokens[pos] != ')':
            return None  # Missing closing parenthesis.
        pos += 1  # consume ')'
        return result
    # Check if token is a digit (integer or decimal)
    elif re.fullmatch(r'\d+(\.\d+)?', token):
        pos += 1
        return token  # Return the number as is.
    else:
        return None

def generate_quadruple_table(expression):
    """
    Main function that tokenizes the expression, parses it,
    and returns the quadruple table if successful.
    """
    global tokens, pos, temp_counter, quadruple_table
    # Normalize the expression: remove spaces and replace Unicode minus with ASCII '-'
    expression = expression.replace(" ", "").replace("–", "-")
    tokens = tokenize(expression)
    pos = 0
    temp_counter = 0
    quadruple_table = []
    
    result = parse_E()
    # If parsing failed or not all tokens were consumed, the expression is invalid.
    if result is None or pos != len(tokens):
        return None
    return quadruple_table

# Main loop: repeatedly read input expressions until "exit" is typed.
if __name__ == "__main__":
    print("Intermediate Code Generation using Quadruple Table")
    print("Grammar:")
    print("  E  → T E'")
    print("  E' → + T | - T | ε")
    print("  T  → F T'")
    print("  T' → * F | / F | ε")
    print("  F  → (E) | digit")
    print("\nEnter an arithmetic expression (operands: integers/decimals, operators: +, -, *, /, parentheses):")
    print("Type 'exit' to quit.\n")

    while True:
        expr = input("Expression: ")
        if expr.lower() == "exit":
            break
        quad_table = generate_quadruple_table(expr)
        if quad_table is None:
            print("Invalid expression")
        else:
            print("\nQuadruple Table:")
            print("Operator  Operand1  Operand2  Result")
            for quad in quad_table:
                op, op1, op2, res = quad
                print(f"{op:<9} {op1:<9} {op2:<9} {res}")
        print()
