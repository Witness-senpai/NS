import sys
from lexer import do_lex
from nsparser import do_parse
from Executor import do_calculate

fileProgram = open("./tests/program.ns")
characters = fileProgram.read()
fileProgram.close()

tokens = do_lex(characters)
poliz = do_parse(tokens)
do_calculate(poliz)

file1 = open("./logs/tokens.txt", "w")
file1.write(str(tokens))
file1.close()

file1 = open("./logs/poliz.txt", "w")
file1.write(str(poliz))
file1.close()
