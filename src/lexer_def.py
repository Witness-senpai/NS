#token -> (reEx, tag, priority)
token_exprs = [
    (r'[ \t\n]+',               None,                0),
    (r'!![^\n]*',               None,                0),

    (r'\+\+',                   "INC",               8),
    (r'\+=',                    "PLUS_ASSIGN",       1),
    (r'\+',                     "PLUS",              6),       
    (r'--',                     "DEC",               8),
    (r'-=',                     "MINUS_ASSIGN",      1), 
    (r'-',                      "MINUS",             6),
    (r'//=',                    "MOD_ASSIGN",        1),
    (r'//',                     "MOD",               7),
    (r'/=',                     "DIVISION_ASSIGN",   1),
    (r'/',                      "DIVISION",          7),
    (r'\*\*',                   "POW",               8), 
    (r'\*=',                    "MULT_ASSIGN",       1),
    (r'\*',                     "MULT",              7),  

    (r'not',                    "NOT",               4),
    (r'and',                    "AND",               3),  
    (r'or',                     "OR",                2),
    (r'xor',                    "XOR",               2),
    (r'>=',                     "GRATER_EQ",         5),
    (r'>',                      "GRATER",            5),
    (r'<=',                     "LESS_EQ",           5),
    (r'<',                      "LESS",              5), 
    (r'==',                     "EQUAL",             4),
    (r'=',                      "ASSIGN",            1),
    (r'!=',                     "NOT_EQUAL",         4),

    (r'\(',                     "BRACKET_OPEN",      0),
    (r'\)',                     "BRACKET_CLOSE",     0),        
    (r'\{',                     "BRACE_OPEN",        0),
    (r'\}',                     "BRACE_CLOSE",       0),
    (r';',                      "SEMICOLON",         0),

    (r'end.',                   "END",               0),
    (r'if',                     "IF",                0),
    (r'else',                   "ELSE",              0),
    (r'while',                  "WHILE",             0),

    (r'[0-9]+\.[0-9]+',         "FLOAT",             0),   
    (r'[0-9]+',                 "INT",               0),      
    #(r'"[^"]*"',                "STRING"),
    (r'[A-Za-z_][A-Za-z0-9_]*', "ID",                0)                    
]