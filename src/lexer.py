import re
import sys
from lexer_def import token_exprs

def lex(characters, token_exprs):
    tokens = []
    pos = 0
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                lexem = match.group(0)
                if tag:
                    token = (lexem, tag)
                    tokens.append(token)
                break
        if not match:
            print("Wrong character '" + str(characters[pos]) + "'")
            return(tokens)
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens          

def do_lex(chars):
    return lex(chars, token_exprs)