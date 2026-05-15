# -- VALIDATION AND HELPER FUNCTIONS --
def isKeyword(word):
    """Check if a word is a reserved keyword"""
    keywords = {"PRINT", "BEG", "EXIT"}
    return word.upper() in keywords

def isValidVariableName(name):
    """Check if name follows: letter{letter|digit}"""
    if not name:
        return False
    if isKeyword(name):
        return False
    if not name[0].isalpha():
        return False
    for char in name[1:]:
        if not char.isalnum():
            return False
    return True

def isIntegerLiteral(s):
    """Check if string matches integer format: [-]digit{digit}"""
    if not s:
        return False
    if s[0] == '-':
        s = s[1:]
    if not s:
        return False
    return s.isdigit()

def isFloatLiteral(s):
    """Check if string matches float format: [-]digit{digit}.{digit}"""
    if not s:
        return False
    if s[0] == '-':
        s = s[1:]
    if '.' not in s:
        return False
    parts = s.split('.')
    if len(parts) != 2:
        return False
    if not (parts[0].isdigit() and parts[1].isdigit()):
        return False
    return True

def getValueType(value):
    """Determine type of a literal value"""
    if isIntegerLiteral(value):
        return "int", int(value)
    elif isFloatLiteral(value):
        return "float", float(value)
    else:
        return None, None

def isDefined(variable_name, variables):
    """Check if variable is defined"""
    return variable_name in variables

# -- TOKENIZATION --
def tokenize(command):
    operators = {'=', '+', '-', '*', '/', '%', '(', ')'}
    tokens = []
    current_token = ""
    i = 0
    while i < len(command):
        char = command[i]
        if char.isspace():
            if current_token:
                tokens.append(current_token)
                current_token = ""
            i += 1
            continue
        if char in operators:
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(char)
            i += 1
            continue
        current_token += char
        i += 1
    if current_token:
        tokens.append(current_token)
    return tokens

# -- PARSING & EXPRESSION EVALUATION --
def parseExpression(tokens, start_index, variables):
    result, result_type, index = parseAdditionSubtraction(tokens, start_index, variables)
    return result, result_type, index

def parseAdditionSubtraction(tokens, index, variables):
    left_val, left_type, index = parseMultiplicationDivision(tokens, index, variables)
    while index < len(tokens) and tokens[index] in ('+', '-'):
        operator = tokens[index]
        index += 1
        right_val, right_type, index = parseMultiplicationDivision(tokens, index, variables)
        if left_type != right_type:
            raise Exception("Operands must be of the same type in an arithmetic operation!")
        if operator == '+':
            left_val = left_val + right_val
        elif operator == '-':
            left_val = left_val - right_val
        left_type = "float" if isinstance(left_val, float) else "int"
    return left_val, left_type, index

def parseMultiplicationDivision(tokens, index, variables):
    left_val, left_type, index = parsePrimary(tokens, index, variables)
    while index < len(tokens) and tokens[index] in ('*', '/', '%'):
        operator = tokens[index]
        index += 1
        right_val, right_type, index = parsePrimary(tokens, index, variables)
        if left_type != right_type:
            raise Exception("Operands must be of the same type in an arithmetic operation!")
        if operator == '%':
            if left_type != "int" or right_type != "int":
                raise Exception("Modulo operation requires integer operands!")
            if right_val == 0:
                raise Exception("Modulo by zero error!")
            left_val = int(left_val) % int(right_val)
        elif operator == '*':
            left_val = left_val * right_val
        elif operator == '/':
            if right_val == 0:
                raise Exception("Division by zero error!")
            left_val = left_val / right_val
            left_type = "float"
        left_type = "float" if isinstance(left_val, float) else "int"
    return left_val, left_type, index

def parsePrimary(tokens, index, variables):
    if index >= len(tokens):
        raise Exception("Incomplete expression")
    token = tokens[index]
    if isIntegerLiteral(token):
        return int(token), "int", index + 1
    elif isFloatLiteral(token):
        return float(token), "float", index + 1
    if isValidVariableName(token):
        if not isDefined(token, variables):
            raise Exception(f"Undefined variable [{token}]!")
        var_info = variables[token]
        return var_info["value"], var_info["type"], index + 1
    if token == '(':
        val, val_type, index = parseExpression(tokens, index + 1, variables)
        if index >= len(tokens) or tokens[index] != ')':
            raise Exception("Missing closing parenthesis")
        return val, val_type, index + 1
    raise Exception(f"Unknown word [{token}]!")

# -- COMMAND PROCESSING --
def processCommand(command, variables):
    tokens = tokenize(command)
    if not tokens:
        return
    if '=' in tokens and tokens[0] != '=':
        processAssignment(tokens, variables)
    elif tokens[0].upper() == "PRINT":
        processPrint(tokens, variables)
    elif tokens[0].upper() == "BEG":
        processBeg(tokens, variables)
    elif len(tokens) == 1:
        processSingleExpression(tokens, variables)
    elif any(op in tokens for op in ['+', '-', '*', '/', '%']):
        processArithmeticExpression(tokens, variables)
    else:
        print("Unknown command! Does not match any valid command of the language.")

# -- COMMAND HANDLERS --
def processAssignment(tokens, variables):
    try:
        eq_index = tokens.index('=')
    except ValueError:
        print("Invalid assignment format!")
        return
    if eq_index != 1:
        print("Invalid assignment format!")
        return
    var_name = tokens[0]
    if not isValidVariableName(var_name):
        print(f"Unknown word [{var_name}]!")
        return
    expr_tokens = tokens[eq_index + 1:]
    try:
        value, value_type, _ = parseExpression(expr_tokens, 0, variables)
        variables[var_name] = {"value": value, "type": value_type}
    except Exception as e:
        print(f"SNOL> Error! {str(e)}")

def processPrint(tokens, variables):
    if len(tokens) != 2:
        print("Unknown command! Does not match any valid command of the language.")
        return
    operand = tokens[1]
    if isIntegerLiteral(operand) or isFloatLiteral(operand):
        print(f"SNOL> [{operand}] = {operand}")
        return
    if isValidVariableName(operand):
        if not isDefined(operand, variables):
            print(f"SNOL> Error! Undefined variable [{operand}]!")
            return
        var_info = variables[operand]
        print(f"SNOL> [{operand}] = {var_info['value']}")
        return
    print(f"Unknown word [{operand}]!")

def processBeg(tokens, variables):
    if len(tokens) != 2:
        print("Unknown command! Does not match any valid command of the language.")
        return
    var_name = tokens[1]
    if not isValidVariableName(var_name):
        print(f"Unknown word [{var_name}]!")
        return
    print(f"SNOL> Please enter value for [{var_name}]:")
    user_input = input("Input: ").strip()
    value = None
    value_type = None
    if isIntegerLiteral(user_input):
        value = int(user_input)
        value_type = "int"
    elif isFloatLiteral(user_input):
        value = float(user_input)
        value_type = "float"
    else:
        print(f"SNOL> Error! Invalid number format!")
        return
    variables[var_name] = {"value": value, "type": value_type}

def processSingleExpression(tokens, variables):
    token = tokens[0]
    if isValidVariableName(token):
        if isDefined(token, variables):
            pass  # Evaluate silently as per spec
        else:
            print(f"SNOL> Error! Undefined variable [{token}]!")
        return
    if isIntegerLiteral(token) or isFloatLiteral(token):
        return  # Evaluate silently as per spec
    print(f"Unknown word [{token}]!")

def processArithmeticExpression(tokens, variables):
    try:
        result, result_type, _ = parseExpression(tokens, 0, variables)
    except Exception as e:
        print(f"SNOL> Error! {str(e)}")

# MAIN FUNCTION
def main():
    print("The SNOL environment is now active, you may proceed with giving your commands.")
    variables = {}
    while True:
        try:
            command = input(">>> ").strip()
            if not command:
                continue
            if command.strip().upper() == "EXIT":
                print("Exiting SNOL environment. Goodbye!")
                break
            processCommand(command, variables)
        except KeyboardInterrupt:
            print("\nExiting SNOL environment. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()