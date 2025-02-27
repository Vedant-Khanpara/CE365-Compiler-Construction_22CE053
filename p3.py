import re

file_path = input("Enter the C source file path: ")

with open(file_path, 'r') as f:
    code = f.read()


code = re.sub(r'//.*', '', code)
code = re.sub(r'/\*[\s\S]*?\*/', '', code)
keywords = {"int", "char", "return", "void", "struct", "float", "long"}


multi_char_ops = {"++", "--", "==", "!=", "<=", ">="}
single_char_ops = {"+", "-", "*", "/", "=", "%", "<", ">", "!"}
punctuations = {"(", ")", "{", "}", "[", "]", ";", ",", "."}

tokens = []    
symbol_table = []  
lexical_errors = []  

i = 0
n = len(code)

while i < n:
     
    if code[i].isspace():
        i += 1
        continue
        
    if code[i] == '"':
        j = i + 1
        while j < n and code[j] != '"':
            j += 1
        if j < n:   
            token = code[i:j+1]
            tokens.append(("Constant", token))
            i = j + 1
            continue
        else:
            lexical_errors.append("Unterminated string literal")
            break

    if code[i] == "'":
        j = i + 1
        while j < n and code[j] != "'":
            j += 1
        if j < n:   
            token = code[i:j+1]
            tokens.append(("Constant", token))
            i = j + 1
            continue
        else:
            lexical_errors.append("Unterminated character literal")
            break

    if code[i].isalpha() or code[i] == '_':
        j = i
        while j < n and (code[j].isalnum() or code[j] == '_'):
            j += 1
        token = code[i:j]
        if token in keywords:
            tokens.append(("Keyword", token))
        else:
            tokens.append(("Identifier", token))
            if token not in symbol_table:
                symbol_table.append(token)
        i = j
        continue

    if code[i].isdigit():
        j = i
        while j < n and code[j].isdigit():
            j += 1
    
        if j < n and code[j].isalpha():
            k = j
            while k < n and (code[k].isalnum() or code[k] == '_'):
                k += 1
            token = code[i:k]
            tokens.append(("Invalid", token))
            lexical_errors.append(f"Line ? : {token} invalid lexeme")
            i = k
            continue
        token = code[i:j]
        tokens.append(("Constant", token))
        i = j
        continue

    if i + 1 < n:
        two_char = code[i:i+2]
        if two_char in multi_char_ops:
            tokens.append(("Operator", two_char))
            i += 2
            continue

    if code[i] in single_char_ops:
        tokens.append(("Operator", code[i]))
        i += 1
        continue

    if code[i] in punctuations:
        tokens.append(("Punctuation", code[i]))
        i += 1
        continue

    tokens.append(("Invalid", code[i]))
    lexical_errors.append(f"Line ? : {code[i]} invalid lexeme")
    i += 1

print("\nTOKENS")
for token_type, lexeme in tokens:
    if token_type == "Invalid":
        continue 
    print(f"{token_type}: {lexeme}")

if lexical_errors:
    print("\nLEXICAL ERRORS")
    for error in lexical_errors:
        print(error)

print("\nSYMBOL TABLE ENTRIES")
for idx, ident in enumerate(symbol_table, 1):
    print(f"{idx}) {ident}")
