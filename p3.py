import re

# ----------------------------
# Step 1: Read and Preprocess the File
# ----------------------------

# Ask user for the C source file path.
file_path = input("Enter the C source file path: ")

# Read the entire file.
with open(file_path, 'r') as f:
    code = f.read()

# Remove single-line comments (//...) and multi-line comments (/* ... */)
code = re.sub(r'//.*', '', code)
code = re.sub(r'/\*[\s\S]*?\*/', '', code)

# ----------------------------
# Step 2: Define Lists for Token Types
# ----------------------------

# A small set of C keywords (you can expand this list as needed)
keywords = {"int", "char", "return", "void", "struct", "float", "long"}

# Define sets for operators and punctuation
multi_char_ops = {"++", "--", "==", "!=", "<=", ">="}
single_char_ops = {"+", "-", "*", "/", "=", "%", "<", ">", "!"}
punctuations = {"(", ")", "{", "}", "[", "]", ";", ",", "."}

# ----------------------------
# Step 3: Lexical Analysis (Tokenization)
# ----------------------------

tokens = []          # List of tuples: (token_type, lexeme)
symbol_table = []    # List to store identifiers (no duplicates)
lexical_errors = []  # List of error messages

i = 0
n = len(code)

while i < n:
    # Skip white spaces.
    if code[i].isspace():
        i += 1
        continue

    # ----------------------------
    # Handle String Literals
    # ----------------------------
    if code[i] == '"':
        j = i + 1
        while j < n and code[j] != '"':
            j += 1
        if j < n:  # Found closing "
            token = code[i:j+1]
            tokens.append(("Constant", token))
            i = j + 1
            continue
        else:
            lexical_errors.append("Unterminated string literal")
            break

    # ----------------------------
    # Handle Character Literals
    # ----------------------------
    if code[i] == "'":
        j = i + 1
        while j < n and code[j] != "'":
            j += 1
        if j < n:  # Found closing '
            token = code[i:j+1]
            tokens.append(("Constant", token))
            i = j + 1
            continue
        else:
            lexical_errors.append("Unterminated character literal")
            break

    # ----------------------------
    # Handle Identifiers and Keywords (start with letter or underscore)
    # ----------------------------
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

    # ----------------------------
    # Handle Numeric Constants
    # ----------------------------
    if code[i].isdigit():
        j = i
        while j < n and code[j].isdigit():
            j += 1
        # Check for a letter immediately following the number (invalid token like 7H)
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

    # ----------------------------
    # Handle Multi-character Operators First (like ++, --, ==, etc.)
    # ----------------------------
    if i + 1 < n:
        two_char = code[i:i+2]
        if two_char in multi_char_ops:
            tokens.append(("Operator", two_char))
            i += 2
            continue

    # ----------------------------
    # Handle Single-character Operators
    # ----------------------------
    if code[i] in single_char_ops:
        tokens.append(("Operator", code[i]))
        i += 1
        continue

    # ----------------------------
    # Handle Punctuation
    # ----------------------------
    if code[i] in punctuations:
        tokens.append(("Punctuation", code[i]))
        i += 1
        continue

    # ----------------------------
    # If the character does not match any known token, flag it as a lexical error.
    # ----------------------------
    tokens.append(("Invalid", code[i]))
    lexical_errors.append(f"Line ? : {code[i]} invalid lexeme")
    i += 1

# ----------------------------
# Step 4: Output the Results
# ----------------------------

print("\nTOKENS")
for token_type, lexeme in tokens:
    if token_type == "Invalid":
        continue  # Lexical errors will be printed separately
    print(f"{token_type}: {lexeme}")

if lexical_errors:
    print("\nLEXICAL ERRORS")
    for error in lexical_errors:
        print(error)

print("\nSYMBOL TABLE ENTRIES")
for idx, ident in enumerate(symbol_table, 1):
    print(f"{idx}) {ident}")
