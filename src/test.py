import sys
from lexer import do_lex
import nsparser as p
import Executor as ex

filename = "./tests/program.ns"
file = open(filename)
characters = file.read()
tokens = do_lex(characters)
file.close()
for token in tokens:
    print(token)

poliz = p.do_parse(tokens)

ex = ex.StackMachine(poliz)
ex.process()

file = open("poliz.txt", "w")
file.write(str(poliz))
file.close()