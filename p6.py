# Global variables for the input string and current position.
input_str = ""
pos = 0

def parse_S():
    global pos, input_str
    # S  → ( L ) | a
    if pos >= len(input_str):
        return False
    if input_str[pos] == 'a':
        pos += 1  # consume 'a'
        return True
    elif input_str[pos] == '(':
        pos += 1  # consume '('
        if not parse_L():
            return False
        if pos < len(input_str) and input_str[pos] == ')':
            pos += 1  # consume ')'
            return True
        else:
            return False
    else:
        return False

def parse_L():
    global pos, input_str
    # L → S L’
    if not parse_S():
        return False
    return parse_Lprime()

def parse_Lprime():
    global pos, input_str
    # L’ → , S L’ | ε
    if pos < len(input_str) and input_str[pos] == ',':
        pos += 1  # consume comma
        if not parse_S():
            return False
        return parse_Lprime()
    # ε production
    return True

while True:
    # Get input from the user (type "exit" to quit)
    input_str = input("Enter the string (or type 'exit' to quit): ")
    if input_str.lower() == "exit":
        break

    # Remove spaces for simplicity
    input_str = input_str.replace(" ", "")
    pos = 0  # Reset position

    # Start parsing with the start symbol S and check if all input is consumed.
    if parse_S() and pos == len(input_str):
        print("Valid string")
    else:
        print("Invalid string")