import re
class Node:
    def __init__(self, kind, value=None, left=None, right=None):
        self.kind = kind    
        self.value = value   
        self.left = left
        self.right = right
def tokenize(expr):
 
    token_pattern = r'\d+\.\d+|\d+|[A-Za-z_]\w*|[+\-*/^()]'
    return re.findall(token_pattern, expr)
tokens = []
pos = 0

def parse_E():
    global pos
    node = parse_T()
    if node is None:
        return None
    return parse_Eprime(node)

def parse_Eprime(inherited):
    global pos
    while pos < len(tokens) and tokens[pos] in ['+', '-']:
        op = tokens[pos]
        pos += 1
        right = parse_T()
        if right is None:
            return None
        inherited = Node('op', op, inherited, right)
    return inherited

def parse_T():
    global pos
    node = parse_F()
    if node is None:
        return None
    return parse_Tprime(node)

def parse_Tprime(inherited):
    global pos
    while pos < len(tokens) and tokens[pos] in ['*', '/']:
        op = tokens[pos]
        pos += 1
        right = parse_F()
        if right is None:
            return None
        inherited = Node('op', op, inherited, right)
    return inherited

def parse_F():
    global pos
    if pos >= len(tokens):
        return None
    token = tokens[pos]
    if token == '(':
        pos += 1  
        node = parse_E()
        if node is None:
            return None
        if pos >= len(tokens) or tokens[pos] != ')':
            return None  
        pos += 1   
        return node
    else:
      
        if re.fullmatch(r'\d+(\.\d+)?', token):
            pos += 1
            
            if '.' in token:
                return Node('num', float(token))
            else:
                return Node('num', int(token))
        elif re.fullmatch(r'[A-Za-z_]\w*', token):
            pos += 1
            return Node('var', token)
        else:
            return None

def parse_expression(expr):
    global tokens, pos
    tokens = tokenize(expr)
    pos = 0
    ast = parse_E()
    if ast is None or pos != len(tokens):
        return None
    return ast
def fold_constants(node):
    if node is None:
        return None
    if node.kind == 'op':
        node.left = fold_constants(node.left)
        node.right = fold_constants(node.right)

        if node.left and node.left.kind == 'num' and node.right and node.right.kind == 'num':
            a = node.left.value
            b = node.right.value
            try:
                if node.value == '+':
                    res = a + b
                elif node.value == '-':
                    res = a - b
                elif node.value == '*':
                    res = a * b
                elif node.value == '/':
                   
                    res = a / b if b != 0 else float('inf')
                elif node.value == '^':
                    res = a ** b
                else:
                    return node
                return Node('num', res)
            except Exception as e:
                return node
        else:
            return node
    else:
        
        return node
precedence = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '^': 3
}

def ast_to_string(node, parent_prec=0):
    if node is None:
        return ""
    if node.kind in ['num', 'var']:
        return str(node.value)
    elif node.kind == 'op':
        op = node.value
        prec = precedence.get(op, 0)
        left_str = ast_to_string(node.left, prec)
        right_str = ast_to_string(node.right, prec + 1 if op in ['-', '/'] else prec)
        s = f"{left_str} {op} {right_str}"
        if prec < parent_prec:
            return f"({s})"
        return s
    return ""
if __name__ == "__main__":
    print("Constant Folding Code Optimization")
    print("Enter an arithmetic expression (operands: integers/decimals/variables, operators: +, -, *, /, ^, and parentheses)")
    print("Type 'exit' to quit.\n")
    while True:
        expr = input("Expression: ")
        if expr.lower() == "exit":
            break
        expr = expr.strip()
        ast = parse_expression(expr)
        if ast is None:
            print("Invalid expression\n")
            continue
        optimized_ast = fold_constants(ast)
        optimized_expr = ast_to_string(optimized_ast)
        print("Optimized Expression:", optimized_expr, "\n")
