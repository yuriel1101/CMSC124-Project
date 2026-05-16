import re
from tokenizer import tokenize
from validator import is_valid_expression_syntax
from evaluator import evaluate_expression

def run_command(interpreter, line):
    """
    Parses and executes a single SNOL command.
    Handles input, printing, assignment, and general expression evaluation.
    """
    # Check for Unknown Words by validating each whitespace-separated chunk
    words = line.split()
    for word in words:
        word_tokens = tokenize(word)
        if any(t[0] == 'UNKNOWN' for t in word_tokens):
            print(f"SNOL> Unknown word [{word}]")
            return

    tokens = tokenize(line)
    if not tokens:
        return

    first_kind, first_val = tokens[0]

    # Handle Termination: EXIT!
    if first_kind == 'EXIT':
        print("\nInterpreter is now terminated...")
        interpreter.running = False
        return

    # Handle Input: BEG variable
    if first_kind == 'ID' and first_val == 'BEG':
        if len(tokens) == 2 and tokens[1][0] == 'ID':
            var_name = tokens[1][1]
            if var_name in ['BEG', 'PRINT']:
                print("SNOL> Unknown command! What follows the keyword BEG should be a variable")
                return
            
            print(f"SNOL> Please enter value for [{var_name}]:")
            val_str = input("Input: ").strip()
            try:
                # Validate input as either a float or an integer
                if re.fullmatch(r'[-]?\d+\.\d+', val_str):
                    interpreter.symbol_table[var_name] = float(val_str)
                elif re.fullmatch(r'[-]?\d+', val_str):
                    interpreter.symbol_table[var_name] = int(val_str)
                else:
                    raise ValueError()
            except ValueError:
                print(f"SNOL> Invalid number format [{val_str}]")
            return
        else:
            print("SNOL> Unknown command! What follows the keyword BEG should be a variable")
            return

    # Handle Output: PRINT identifier/literal
    if first_kind == 'ID' and first_val == 'PRINT':
        if len(tokens) == 2:
            kind, val = tokens[1]
            if kind == 'ID':
                if val in interpreter.symbol_table:
                    result = interpreter.symbol_table[val]
                    print(f"SNOL> [{val}] = {result}")
                else:
                    print(f"SNOL> Undefined variable [{val}]")
            elif kind in ('INTEGER', 'FLOAT'):
                print(f"SNOL> [{val}] = {val}")
            else:
                print("SNOL> Unknown command! Does not match any valid command of the language.")
            return
        else:
             print("SNOL> Unknown command! Does not match any valid command of the language.")
             return

    # Handle Assignment: var = expression
    if first_kind == 'ID' and len(tokens) >= 3 and tokens[1] == ('OP', '='):
        var_name = first_val
        if var_name in ['BEG', 'PRINT']:
            print("SNOL> Unknown command!")
            return
        
        expr_tokens = tokens[2:]
        if is_valid_expression_syntax(expr_tokens):
            try:
                result = evaluate_expression(expr_tokens, interpreter.symbol_table)
                interpreter.symbol_table[var_name] = result
            except NameError as e:
                print(f"SNOL> {str(e)}")
            except TypeError as e:
                print(f"SNOL> {str(e)}")
            except (SyntaxError, ZeroDivisionError):
                print("SNOL> Unknown command! Does not match any valid command of the language.")
        else:
            print("SNOL> Unknown command! Does not match any valid command of the language.")
        return

    # Handle Standalone Expression or Operation
    if is_valid_expression_syntax(tokens):
        # Specific check for undefined identifiers when used alone
        if len(tokens) == 1 and first_kind == 'ID':
            if first_val not in interpreter.symbol_table and first_val not in ['BEG', 'PRINT']:
                print(f"SNOL> Unknown word [{first_val}]")
                return
        
        try:
            evaluate_expression(tokens, interpreter.symbol_table)
        except NameError as e:
            print(f"SNOL> {str(e)}")
        except TypeError as e:
            print(f"SNOL> {str(e)}")
        except (SyntaxError, ZeroDivisionError, IndexError):
            print("SNOL> Unknown command! Does not match any valid command of the language.")
        return

    # Fallback for unrecognized syntax
    print("SNOL> Unknown command! Does not match any valid command of the language.")
