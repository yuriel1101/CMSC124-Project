def is_valid_expression_syntax(tokens):
    """
    Checks if a list of tokens follows the valid syntactic structure for an expression.
    Validates the alternating pattern of terms and operators.
    """
    if not tokens:
        return False
        
    expect_term = True
    for kind, val in tokens:
        if expect_term:
            # Must be a number or a variable name (not a keyword)
            if kind in ('INTEGER', 'FLOAT', 'ID'):
                if val in ['BEG', 'PRINT']:
                    return False
                expect_term = False
            else:
                return False
        else:
            # Must be an arithmetic operator (not an assignment operator)
            if kind == 'OP' and val != '=':
                expect_term = True
            else:
                return False
                
    # A valid expression must not end with an operator
    return not expect_term
