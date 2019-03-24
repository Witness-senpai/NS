import re
import sys

def lex(characters, token_exprs):
    num_line = 0
    tokens = []
    for line in characters:
        pos = 0
        num_line += 1
        while pos < len(line):
            match = None
            for token_expr in token_exprs:
                pattern, tag = token_expr
                regex = re.compile(pattern)
                match = regex.match(line, pos)
                if match:
                    txt = match.group(0)
                    if tag:
                        token = (txt, tag)
                        tokens.append(token)
                    break
            if not match:
                print("Wrong character '" + str(line[pos]) + "' at line " + str(num_line))
                return(tokens)
                sys.exit(1)
            else:
                pos = match.end(0)
    return tokens          

