import sys
from lexer import do_lex

filename = "./tests/program.ns"
file = open(filename)
characters = file.read()
tokens = do_lex(characters)
file.close()
for token in tokens:
    print(token)