# NS - Needless Script
Needless Script is a simple language and interpreter for it in python

# Description
NS consist of 3 main parts:
* Lexer
  * For analyzing sintaksis of program. 
  * Lexer generate list of tokens from program code.
* Parser
  * For analyze the program on the rules of the language.
  * Parser generate inversion polish notation from list of tokens.
* Stack machine
  * for finally executing a code.
  * Stack machine takes the inversion polish notation and execute it

# Features
* NS has a minimal standard set of operators, cycles and conditions. 
* NS supports two classes:
  * Linked list.
  * Hash set. 
* NS supports inputting and printing in console
  
All rules and definition describe into txt file:
> grammar.txt

# Launch
To run some NS program from the console, you must enter the following command:
> python ns.py program.ns
