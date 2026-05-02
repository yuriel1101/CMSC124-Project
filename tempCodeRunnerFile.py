import sys

def main():
    # SYMBOL TABLE: Stores variable names, their values, and types.
    # Passing this as an argument avoids global variables.
    symbol_table = {} 

    print("SNOL Interpreter [Version 1.0]")
    print("Type 'EXIT!' to quit.")

    while True:
        try:
            line = input("Command: ").strip()
            
            if line == "EXIT!":
                break
            if not line:
                continue

            # STEP 1: TOKENIZE
            tokens = line.split()

            # STEP 2: EVALUATE
            # We pass the symbol_table into the evaluator
            evaluate(tokens, symbol_table)

        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")

def evaluate(tokens, table):
    """Identifies the command type and routes to the correct logic."""
    first_token = tokens[0]

    # Case 1: BEG command (Input)
    if first_token == "BEG":
        handle_input(tokens, table)

    # Case 2: PRINT command (Output)
    elif first_token == "PRINT":
        handle_output(tokens, table)

    # Case 3: Assignment (e.g., x = 10 or x = 10 + 5)
    elif len(tokens) >= 3 and tokens[1] == "=":
        handle_assignment(tokens, table)

    else:
        print("Error: Unknown command format.")

def get_value(token, table):
    # Check if it's a variable in the table
    if token in table:
        return table[token]
    
    # Check if it's a raw number
    try:
        if "." in token:
            return float(token)
        return int(token)
    except ValueError:
        print(f"Error: Undefined variable {token}")
        return None

def handle_input(tokens, table):
    if len(tokens) < 2:
        print("Error: BEG requires a variable name.")
        return
    
    var_name = tokens[1]
    raw_value = input("In: ").strip()

    try:
        # Try to save as an integer
        if "." not in raw_value:
            table[var_name] = int(raw_value)
        else:
            # Try to save as a float
            table[var_name] = float(raw_value)
            
    except ValueError:
        # If the user types "abc" or "10-helper"
        print("Error: Invalid number format")

def handle_output(tokens, table):
    # Check if the user actually provided a variable name
    if len(tokens) < 2:
        print("Error: PRINT command requires a variable or a value.")
        return

    target = tokens[1]

    # Step 1: Check if 'target' is a variable we have saved in our table
    if target in table:
        print(table[target])
    
    # Step 2: Check if 'target' is just a raw number (like PRINT 10)
    elif target.replace('.', '', 1).isdigit():
        print(target)
        
    # Step 3: If it's not a number and not in the table, it's an error
    else:
        print(f"Error: Undefined variable {target}")

def handle_assignment(tokens, table):
    target_var = tokens[0]
    # tokens[1] is the "="
    expr = tokens[2:]

    # Scenario 1: Simple assignment (e.g., x = 10 or x = y)
    if len(expr) == 1:
        val = get_value(expr[0], table)
        if val is not None:
            table[target_var] = val

    # Scenario 2: Arithmetic (e.g., x = 10 + 5)
    elif len(expr) == 3:
        left_val = get_value(expr[0], table)
        op = expr[1]
        right_val = get_value(expr[2], table)

        if left_val is not None and right_val is not None:
            # CRITICAL PROJECT RULE: Check if types match
            if type(left_val) != type(right_val):
                print("Error: Incompatible types")
                return

            # Perform math based on the operator
            if op == "+": table[target_var] = left_val + right_val
            elif op == "-": table[target_var] = left_val - right_val
            elif op == "*": table[target_var] = left_val * right_val
            elif op == "/": table[target_var] = left_val / right_val
            elif op == "%": table[target_var] = left_val % right_val

if __name__ == "__main__":
    main()
