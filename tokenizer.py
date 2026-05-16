import re

def tokenize(line):
    """
    Converts a single line of SNOL code into a list of tokens.
    Handles identifiers, literals (integers/floats), operators, and keywords.
    """
    tokens = []
    i = 0
    while i < len(line):
        if line[i].isspace():
            i += 1
            continue
        
        # Check for the exit command specifically
        if line[i:].startswith('EXIT!'):
            tokens.append(('EXIT', 'EXIT!'))
            i += 5
            continue
        
        # Check for common operators (except hyphen which needs context)
        if line[i] in '+*/%=':
            tokens.append(('OP', line[i]))
            i += 1
            continue
        
        # Handle the hyphen: either a binary operator or a sign for a numeric literal
        if line[i] == '-':
            # If it's at the start or follows another operator, it's a negative sign
            if not tokens or (tokens[-1][0] == 'OP'):
                match = re.match(r'-\d+(\.\d+)?', line[i:])
                if match:
                    val = match.group()
                    if '.' in val:
                        tokens.append(('FLOAT', val))
                    else:
                        tokens.append(('INTEGER', val))
                    i += len(val)
                    continue
            # Otherwise, it's the subtraction operator
            tokens.append(('OP', '-'))
            i += 1
            continue
        
        # Match floating point literals
        match = re.match(r'\d+\.\d+', line[i:])
        if match:
            tokens.append(('FLOAT', match.group()))
            i += len(match.group())
            continue
        
        # Match integer literals
        match = re.match(r'\d+', line[i:])
        if match:
            tokens.append(('INTEGER', match.group()))
            i += len(match.group())
            continue
        
        # Match valid identifiers (start with letter, followed by letters/digits)
        match = re.match(r'[a-zA-Z][a-zA-Z0-9]*', line[i:])
        if match:
            tokens.append(('ID', match.group()))
            i += len(match.group())
            continue
        
        # Record any unknown characters for error reporting
        tokens.append(('UNKNOWN', line[i]))
        i += 1
    return tokens
