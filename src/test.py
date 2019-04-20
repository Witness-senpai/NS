import sys
from lexer import do_lex
import nsparser as p

filename = "./tests/program.ns"
file = open(filename)
characters = file.read()
tokens = do_lex(characters)
file.close()
for token in tokens:
    print(token)

file = open("poliz.txt", "w")
file.write(p.do_parse(tokens))
file.close()