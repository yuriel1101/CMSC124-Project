def get_precedence(op):
    """
    Returns the precedence level of a given SNOL operator.
    Higher values indicate higher priority.
    """
    if op in ('*', '/', '%'):
        return 2
    if op in ('+', '-'):
        return 1
    return 0

def apply_op(left, op, right):
    """
    Performs the arithmetic operation specified by 'op' on 'left' and 'right'.
    Enforces type consistency and handles division/modulo by zero errors.
    """
    # SNOL requires operands to have the same type
    if type(left) != type(right):
        raise TypeError("Incompatible types")
    
    if op == '+': return left + right
    if op == '-': return left - right
    if op == '*': return left * right
    
    if op == '/':
        if right == 0:
            raise ZeroDivisionError("Division by zero!")
        # Integer division for integers, floating point division for floats
        if isinstance(left, int):
            return left // right
        return left / right
        
    if op == '%':
        # Modulo is strictly for integers in SNOL
        if not isinstance(left, int) or not isinstance(right, int):
             raise TypeError("Modulo operation is only allowed for integer type!")
        if right == 0:
            raise ZeroDivisionError("Modulo by zero!")
        return left % right
        
    return None
