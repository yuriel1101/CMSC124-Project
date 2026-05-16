from operations import get_precedence, apply_op

def evaluate_expression(tokens, symbol_table):
    """
    Evaluates a list of tokens as a mathematical expression using the Shunting-yard algorithm.
    Retrieves variable values from the provided symbol table.
    """
    if not tokens:
        raise SyntaxError("Empty expression")
    
    def get_term_value(kind, val):
        """Helper to convert tokens to their actual numeric values or look up variables."""
        if kind == 'INTEGER': return int(val)
        if kind == 'FLOAT': return float(val)
        if kind == 'ID':
            # Keywords are not allowed as variable names in expressions
            if val in ['BEG', 'PRINT']:
                raise SyntaxError("Keyword in expression")
            if val in symbol_table:
                return symbol_table[val]
            raise NameError(f"Undefined variable [{val}]")
        raise SyntaxError("Invalid term")

    values = []
    ops = []
    expect_term = True # State tracker for infix notation validation
    
    for kind, val in tokens:
        if expect_term:
            if kind in ('INTEGER', 'FLOAT', 'ID'):
                values.append(get_term_value(kind, val))
                expect_term = False
            else:
                raise SyntaxError("Expected term")
        else:
            if kind == 'OP' and val != '=':
                # Apply operators with higher or equal precedence before pushing the new one
                while (ops and get_precedence(ops[-1]) >= get_precedence(val)):
                    r = values.pop()
                    l = values.pop()
                    o = ops.pop()
                    values.append(apply_op(l, o, r))
                ops.append(val)
                expect_term = True
            else:
                raise SyntaxError("Expected operator")
    
    if expect_term:
        raise SyntaxError("Trailing operator")
        
    # Process remaining operators in the stack
    while ops:
        r = values.pop()
        l = values.pop()
        o = ops.pop()
        values.append(apply_op(l, o, r))
        
    return values[0]
