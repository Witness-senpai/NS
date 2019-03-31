token_exprs = [
    (r'[ \t\n]+',               None),
    (r'!![^\n]*',               None),

    (r'\+\+',                   "INCREMENT"),
    (r'\+=',                    "PLUS_ASSIGN"),
    (r'\+',                     "PLUS"),       
    (r'--',                     "DECREMENT"),
    (r'-=',                     "MINUS_ASSIGN"), 
    (r'-',                      "MINUS"),
    (r'=',                      "ASSIGN"),
    (r'/=',                     "DIVISION_ASSIGN"),
    (r'/',                      "DIVISION"),
    (r'//=',                    "DIV_MOD_ASSIGN"),
    (r'//',                     "DIV_MOD"),
    (r'\*=',                    "MULT_ASSIGN"),
    (r'\*',                     "MULT"),    

    (r'not',                    "NOT"),
    (r'and',                    "AND"),  
    (r'or',                     "OR"),
    (r'xor',                    "XOR"),
    (r'>=',                     "GRATER_EQ"),
    (r'>',                      "GRATER"),
    (r'<=',                     "LESS_EQ"),
    (r'<',                      "LESS"), 
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

    (r'[0-9]+\.[0-9]+',         "DIGIT_FLOAT"),   
    (r'[0-9]+',                 "NUMBER"),      
    #(r'"[^"]*"',                "STRING"),
    (r'[A-Za-z_][A-Za-z0-9_]*', "ID")                    
]