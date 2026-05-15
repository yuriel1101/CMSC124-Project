import re
import sys

# Constants for Regex
IDENTIFIER_REGEX = r'[a-zA-Z][a-zA-Z0-9]*'
FLOAT_REGEX = r'[-]?\d+\.\d+'
INTEGER_REGEX = r'[-]?\d+'
OPERATORS = ['+', '-', '*', '/', '%', '=']
KEYWORDS = ['BEG', 'PRINT', 'EXIT!']

class SNOLInterpreter:
    def __init__(self):
        self.symbol_table = {}
        self.running = True

    def tokenize(self, line):
        tokens = []
        i = 0
        while i < len(line):
            if line[i].isspace():
                i += 1
                continue
            
            # Check for EXIT!
            if line[i:].startswith('EXIT!'):
                tokens.append(('EXIT', 'EXIT!'))
                i += 5
                continue
            
            # Check for operators (other than -)
            if line[i] in '+*/%=':
                tokens.append(('OP', line[i]))
                i += 1
                continue
            
            # Check for - (could be binary operator or part of a literal)
            if line[i] == '-':
                # It's a negative sign if it's the start of the line or follows an operator
                if not tokens or (tokens[-1][0] == 'OP'):
                    # Look ahead for digits (literal)
                    match = re.match(r'-\d+(\.\d+)?', line[i:])
                    if match:
                        val = match.group()
                        if '.' in val:
                            tokens.append(('FLOAT', val))
                        else:
                            tokens.append(('INTEGER', val))
                        i += len(val)
                        continue
                # Otherwise it's a binary subtraction operator
                tokens.append(('OP', '-'))
                i += 1
                continue
            
            # Check for FLOAT literal
            match = re.match(r'\d+\.\d+', line[i:])
            if match:
                tokens.append(('FLOAT', match.group()))
                i += len(match.group())
                continue
            
            # Check for INTEGER literal
            match = re.match(r'\d+', line[i:])
            if match:
                tokens.append(('INTEGER', match.group()))
                i += len(match.group())
                continue
            
            # Check for IDENTIFIER
            match = re.match(r'[a-zA-Z][a-zA-Z0-9]*', line[i:])
            if match:
                tokens.append(('ID', match.group()))
                i += len(match.group())
                continue
            
            # Unknown character
            tokens.append(('UNKNOWN', line[i]))
            i += 1
        return tokens

    def get_precedence(self, op):
        if op in ('*', '/', '%'):
            return 2
        if op in ('+', '-'):
            return 1
        return 0

    def apply_op(self, left, op, right):
        if type(left) != type(right):
            raise TypeError("Operands must be of the same type in an arithmetic operation!")
        
        if op == '+': return left + right
        if op == '-': return left - right
        if op == '*': return left * right
        if op == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero!")
            if isinstance(left, int):
                return left // right
            return left / right
        if op == '%':
            if not isinstance(left, int) or not isinstance(right, int):
                 raise TypeError("Modulo operation is only allowed for integer type!")
            if right == 0:
                raise ZeroDivisionError("Modulo by zero!")
            return left % right
        return None

    def evaluate_expression(self, tokens):
        if not tokens:
            raise SyntaxError("Empty expression")
        
        def get_term_value(kind, val):
            if kind == 'INTEGER': return int(val)
            if kind == 'FLOAT': return float(val)
            if kind == 'ID':
                if val in ['BEG', 'PRINT']:
                    raise SyntaxError("Keyword in expression")
                if val in self.symbol_table:
                    return self.symbol_table[val]
                raise NameError(f"Undefined variable [{val}]")
            raise SyntaxError("Invalid term")

        values = []
        ops = []
        expect_term = True
        
        for kind, val in tokens:
            if expect_term:
                if kind in ('INTEGER', 'FLOAT', 'ID'):
                    values.append(get_term_value(kind, val))
                    expect_term = False
                else:
                    raise SyntaxError("Expected term")
            else:
                if kind == 'OP' and val != '=':
                    while (ops and self.get_precedence(ops[-1]) >= self.get_precedence(val)):
                        r = values.pop()
                        l = values.pop()
                        o = ops.pop()
                        values.append(self.apply_op(l, o, r))
                    ops.append(val)
                    expect_term = True
                else:
                    raise SyntaxError("Expected operator")
        
        if expect_term:
            raise SyntaxError("Trailing operator")
            
        while ops:
            r = values.pop()
            l = values.pop()
            o = ops.pop()
            values.append(self.apply_op(l, o, r))
            
        return values[0]

    def is_valid_expression_syntax(self, tokens):
        if not tokens:
            return False
        expect_term = True
        for kind, val in tokens:
            if expect_term:
                if kind in ('INTEGER', 'FLOAT', 'ID'):
                    if val in ['BEG', 'PRINT']:
                        return False
                    expect_term = False
                else:
                    return False
            else:
                if kind == 'OP' and val != '=':
                    expect_term = True
                else:
                    return False
        return not expect_term

    def run_command(self, line):
        # Check for Unknown Words based on whitespace-separated chunks
        words = line.split()
        for word in words:
            # Tokenize the individual word to see if it contains any unknown characters
            word_tokens = self.tokenize(word)
            if any(t[0] == 'UNKNOWN' for t in word_tokens):
                print(f"SNOL> Unknown word [{word}]")
                return

        tokens = self.tokenize(line)
        if not tokens:
            return

        first_kind, first_val = tokens[0]

        # EXIT!
        if first_kind == 'EXIT':
            print("\nInterpreter is now terminated...")
            self.running = False
            return

        # BEG var
        if first_kind == 'ID' and first_val == 'BEG':
            if len(tokens) == 2 and tokens[1][0] == 'ID':
                var_name = tokens[1][1]
                if var_name in ['BEG', 'PRINT']:
                    print("SNOL> Unknown command!")
                    return
                print(f"SNOL> Please enter value for [{var_name}]:")
                val_str = input("Input: ").strip()
                try:
                    if re.fullmatch(r'[-]?\d+\.\d+', val_str):
                        self.symbol_table[var_name] = float(val_str)
                    elif re.fullmatch(r'[-]?\d+', val_str):
                        self.symbol_table[var_name] = int(val_str)
                    else:
                        raise ValueError()
                except ValueError:
                    print(f"SNOL> Unknown word [{val_str}]")
                return
            else:
                print("SNOL> Unknown command!")
                return

        # PRINT out
        if first_kind == 'ID' and first_val == 'PRINT':
            if len(tokens) == 2:
                kind, val = tokens[1]
                if kind == 'ID':
                    if val in self.symbol_table:
                        result = self.symbol_table[val]
                        print(f"SNOL> [{val}] = {result}")
                    else:
                        print(f"SNOL> Undefined variable [{val}]")
                elif kind == 'INTEGER' or kind == 'FLOAT':
                    print(f"SNOL> [{val}] = {val}")
                else:
                    print("SNOL> Unknown command!")
                return
            else:
                 print("SNOL> Unknown command!")
                 return

        # Assignment: var = expr
        if first_kind == 'ID' and len(tokens) >= 3 and tokens[1] == ('OP', '='):
            var_name = first_val
            if var_name in ['BEG', 'PRINT']:
                print("SNOL> Unknown command!")
                return
            
            expr_tokens = tokens[2:]
            if self.is_valid_expression_syntax(expr_tokens):
                try:
                    result = self.evaluate_expression(expr_tokens)
                    self.symbol_table[var_name] = result
                except NameError as e:
                    print(f"SNOL> {str(e)}")
                except TypeError as e:
                    print(f"SNOL> Error! {str(e)}")
                except (SyntaxError, ZeroDivisionError):
                    print("SNOL> Unknown command!")
            else:
                print("SNOL> Unknown command!")
            return

        # Operation / Standalone expression
        if self.is_valid_expression_syntax(tokens):
            # Special check for standalone undefined identifier
            if len(tokens) == 1 and first_kind == 'ID':
                if first_val not in self.symbol_table and first_val not in ['BEG', 'PRINT']:
                    print(f"SNOL> Unknown word [{first_val}]")
                    return
            
            try:
                self.evaluate_expression(tokens)
            except NameError as e:
                print(f"SNOL> {str(e)}")
            except TypeError as e:
                print(f"SNOL> Error! {str(e)}")
            except (SyntaxError, ZeroDivisionError, IndexError):
                print("SNOL> Unknown command!")
            return

        # If not a recognized command or valid expression structure
        # Check if the first word is an unknown word
        if first_kind == 'ID':
            if first_val not in self.symbol_table and first_val not in ['BEG', 'PRINT']:
                print(f"SNOL> Unknown word [{first_val}]")
                return
        
        print("SNOL> Unknown command!")



    def start(self):
        print("The SNOL environment is now active, you may proceed with giving your commands.\n")
        while self.running:
            try:
                line = input("Command: ").strip()
                if not line:
                    continue
                self.run_command(line)
            except (EOFError, KeyboardInterrupt):
                print("\nInterpreter is now terminated...")
                break

if __name__ == "__main__":
    interpreter = SNOLInterpreter()
    interpreter.start()
