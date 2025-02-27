input_str = ""
pos = 0

def parse_S():
    global pos, input_str
     
    if pos >= len(input_str):
        return False
    if input_str[pos] == 'a':
        pos += 1   
        return True
    elif input_str[pos] == '(':
        pos += 1   
        if not parse_L():
            return False
        if pos < len(input_str) and input_str[pos] == ')':
            pos += 1   
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
        pos += 1 
        if not parse_S():
            return False
        return parse_Lprime()
     
    return True

while True:
     
    input_str = input("Enter the string (or type 'exit' to quit): ")
    if input_str.lower() == "exit":
        break
        
    input_str = input_str.replace(" ", "")
    pos = 0  

    if parse_S() and pos == len(input_str):
        print("Valid string")
    else:
        print("Invalid string")
