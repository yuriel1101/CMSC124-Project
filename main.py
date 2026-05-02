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

def handle_input(tokens, table):
    """Logic for 'BEG <var>'"""
    if len(tokens) < 2:
        print("Error: Missing variable name.")
        return
    
    var_name = tokens[1]
    user_val = input("In: ").strip()
    
    # TODO: Add logic to check if user_val is an INT or FLOAT.
    # Store it in 'table' with its value and type.
    # If it's not a number, print "Invalid number format".

def handle_output(tokens, table):
    """Logic for 'PRINT <var>' or 'PRINT <literal>'"""
    # TODO: Check if the token is in the table or is a raw number.
    # If it's a variable not in the table, print "Undefined variable".
    pass

def handle_assignment(tokens, table):
    """Logic for '<var> = <expression>'"""
    target_var = tokens[0]
    expression = tokens[2:]

    # TODO: If expression is one token (x = 10), save it.
    # TODO: If expression is three tokens (x = 10 + 5), check types.
    # CRITICAL: If type(op1) != type(op2), print "Incompatible types".
    pass

if __name__ == "__main__":
    main()
