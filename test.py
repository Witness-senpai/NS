import sys
from lexer_def import *

filename = "program.ns"
file = open(filename)
characters = file.readlines()
tokens = do_lex(characters)
file.close()
for token in tokens:
    print(token)