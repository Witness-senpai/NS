import lexer

token_exprs = [
    (r'[ \t\n]+',               None),
    (r'!![^\n]*',               None),
    (r'!=*[^\n]=!*',            None),

    (r'\+\+',                   "INCREMENT"),
    (r'\+=',                    "PLUS_ASSIGN"),
    (r'\+',                     "PLUS"),       
    (r'--',                     "DECREMENT"),
    (r'-=',                     "MINUS_ASSIGN"), 
    (r'-',                      "MINUS"),
    (r'=',                      "ASSIGN"),
    (r'/',                      "DIVISION"),
    (r'/=',                     "DIVISION_ASSIGN"),
    (r'//',                     "DIV_MOD"),
    (r'//=',                    "DIV_MOD_ASSIGN"),
    (r'\*',                     "MULT"),
    (r'\*=',                    "MULT_ASSIGN"),

    (r'not',                    "NOT"),
    (r'and',                    "AND"),  
    (r'or',                     "OR"),
    (r'xor',                    "XOR"),
    (r'>',                      "GRATER"),
    (r'>=',                     "GRATER_EQ"),
    (r'<',                      "LESS"), 
    (r'<=',                     "LESS_EQ"),
    (r'==',                     "EQUAL"),
    (r'!=',                     "NOT_EQUAL"),

    (r'\(',                     "BRACKET_OPEN"),
    (r'\)',                     "BRACKET_CLOSE"),        
    (r'\{',                     "BRACE_OPEN"),
    (r'\}',                     "BRACE_CLOSE"),
    (r';',                      "SEMICOLON"),

    (r'if',                     "IF"),
    (r'else',                   "ELSE"),
    (r'while',                  "WHILE"),
    (r'end',                    "END"),

    (r'[0-9]+\.[0-9]+',         "DIGIT_FLOAT"),   
    (r'[0-9]+',                 "DIGIT_INT"),      
    (r'"[^"]*"',                "STRING"),
    (r'[A-Za-z_][A-Za-z0-9_]*', "ID")

    #(r'', RESERVED),
    #(r'', RESERVED),
    #(r'', RESERVED),
    #(r'', RESERVED),
    #(r'', RESERVED),
    #(r'', RESERVED)                    
]

def do_lex(string):
    return lexer.lex(string, token_exprs)