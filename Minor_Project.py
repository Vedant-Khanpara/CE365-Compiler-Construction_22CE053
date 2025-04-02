import re

def is_valid_expression(expression):
    """
    Checks whether the arithmetic expression is syntactically valid.
    Supports digits, basic operators (+, -, *, /), exponentiation (^), 
    square root ($ as a unary operator), and parentheses.
    """
    # Remove all whitespaces
    expression = expression.replace(" ", "")
    
    # Check for invalid characters
    # Allowed characters: digits, +, -, *, /, (, ), ^, and $
    if not re.fullmatch(r"[0-9+\-*/()^$]+", expression):
        return False, "Expression contains invalid characters"

    # Check that the parentheses are balanced
    if not check_balanced_parentheses(expression):
        return False, "Parentheses are not balanced"

    # Tokenize the expression into numbers, operators, and parentheses
    tokens = tokenize(expression)
    
    # Check the token sequence for proper syntax
    if not check_syntax(tokens):
        return False, "Invalid syntax in token sequence"
    
    return True, "Expression has valid syntax"

def check_balanced_parentheses(expression):
    """
    Validates that all opening parentheses have a matching closing one.
    """
    stack = []
    for char in expression:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0

def tokenize(expression):
    """
    Splits the expression into tokens (numbers, operators, and parentheses).
    Updated to include exponentiation '^' and square root '$'.
    """
    # \d+ matches multi-digit numbers; the character class now includes ^ and $.
    return re.findall(r'\d+|[+\-*/()^$]', expression)

def check_syntax(tokens):
    """
    Checks the sequence of tokens to ensure valid syntax:
      - Numbers and operators are placed correctly.
      - Unary operators (+, -, or $) are allowed at the start or after an operator or '('.
      - Binary operators (+, -, *, /, ^) must be placed between valid operands.
    """
    prev_token = ""
    for i, token in enumerate(tokens):
        if token in "+-":
            # Determine if + or - is used as a unary operator.
            if i == 0 or prev_token in "+-*/(^$":
                # As a unary operator, it must be followed by a digit, an opening parenthesis, or a unary $.
                if i + 1 < len(tokens) and (tokens[i+1].isdigit() or tokens[i+1] == '(' or tokens[i+1] == '$'):
                    pass  # Valid unary usage.
                else:
                    return False
            else:
                # In binary context, the previous token must be an operand (a number or a closing parenthesis).
                if prev_token in "+-*/(^$":
                    return False
        elif token == "$":
            # The square root operator ($) is always unary.
            if i == 0 or prev_token in "+-*/(^$":
                if i + 1 < len(tokens) and (tokens[i+1].isdigit() or tokens[i+1] == '(' or tokens[i+1] == '$'):
                    pass
                else:
                    return False
            else:
                return False
        elif token in "*/^":
            # Binary operators: cannot be first or last and must be preceded by a valid operand.
            if i == 0 or i == len(tokens) - 1:
                return False
            if prev_token in "+-*/(^$":
                return False
        elif token == ")":
            # A closing parenthesis should not directly follow an operator or an opening parenthesis.
            if prev_token in "+-*/(^$(":
                return False
        elif token == "(":
            # An opening parenthesis should either be at the start or follow an operator.
            if prev_token and prev_token not in "+-*/(^$(":
                return False
        # No additional checks are needed for digit tokens.
        prev_token = token
    return True

# Example usage
if __name__ == "__main__":
    while True:
        test_expr = input("Enter an arithmetic expression (or 'quit' to exit): ")
        if test_expr.lower() == "quit":
            break
        valid, message = is_valid_expression(test_expr)
        print(message)