
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        return self.lang()

    def endScript(self):
        return self.pos == len(self.tokens)

    def lang(self):
        while(True):
            if (not self.expr(self.pos)):
                return False
            if (self.endScript()):
                return True    

    def expr(self, pos):
        if not(
            self.assign(self.pos) or
            self.while_stmt(self.pos) or
            self.if_stmt(self.pos)
            ):
            return False
        return True   

    def assign(self, pos):
        if (not self.var(self.pos)):
            return False
        elif (not self.assign_op(self.pos)):
            return False
        elif (not self.arif_stmt(self.pos)):
            return False
        elif (not self.semicolon(self.pos)):
            return False
        return True

    def var(self, pos):
        if self.tokens[self.pos][1] == "ID":
            self.pos += 1
            return True
        else:
            return False  

    def assign_op(self, pos):
        if self.tokens[self.pos][1] == "ASSIGN": 
            self.pos += 1
            return True
        else:
            return False

    def arif_stmt(self, pos):
        if (not self.value(self.pos)):
            return False
        while(True): #эквивалентно (arif_op value)*
            if (not self.arif_op(self.pos) and not self.value(self.pos)):
                break   
        return True

    def value(self, pos):
        if not(
            self.var(self.pos)    or 
            self.number(self.pos) or
            self.bkt_expr(self.pos)
            ):
            return False
        return True    

    def number(self, pos):
        if self.tokens[self.pos][1] == "NUMBER":
            self.pos += 1
            return True
        else:
            return False

    def bkt_expr(self, pos):
        if (not self.bkt_open(self.pos)):
            return False
        elif(not self.arif_stmt(self.pos)):
            return False
        elif(not self.bkt_close(self.pos)):
            return False
        return True

    def log_stmt(self, pos):
        if (not self.log_value(self.pos)):
            return False
        while(True): #эквивалентно (log_op log_value)*
            if (not self.log_op(self.pos) and not self.log_value(self.pos)):
                break 
        return True

    def log_value(self, pos):
        if not(
            self.var(self.pos)    or
            self.number(self.pos) or
            self.log_bkt_expr(self.pos)
            ):
            return False
        return True

    def log_bkt_expr(self, pos):
        if (not self.bkt_open(self.pos)):
            return False
        elif(not self.log_stmt(self.pos)):
            return False
        elif(not self.bkt_close(self.pos)):
            return False
        return True    

    def if_stmt(self, pos):
        if (not self.KW_IF(self.pos)):
            return False
        elif(not self.bkt_open(self.pos)):
            return False
        elif(not self.log_stmt(self.pos)):
            return False
        elif(not self.bkt_close(self.pos)):
            return False
        elif(not self.brace_open(self.pos)):
            return False
        while(True): #эквивалентно expr* - выполняется 0 или более раз
            if (not self.expr(self.pos)):
                break     
        if(not self.brace_close(self.pos)):
            return False
        if (self.tokens[self.pos + 1][1] == "ELSE"):
            if (self.else_stmt(self.pos)):
                return True
            else:
                return False    
        return True

    def else_stmt(self, pos):
        if (not self.KW_ELSE(self.pos)):
            return False
        elif(not self.brace_open(self.pos)):
            return False
        while(True): #эквивалентно expr* - выполняется 0 или более раз
            if (not self.expr(self.pos)):
                break   
        if(not self.brace_close(self.pos)):
            return False
        return True    

    def KW_IF(self, pos):
        if (self.tokens[self.pos][1] == "IF"):
            self.pos += 1
            return True
        else:
            return False

    def KW_ELSE(self, pos):
        if (self.tokens[self.pos][1] == "ELSE"):
            self.pos += 1
            return True
        else:
            return False        
            

    def while_stmt(self, pos):
        if (not self.KW_WHILE(self.pos)):
            return False
        elif(not self.bkt_open(self.pos)):
            return False
        elif(not self.log_stmt(self.pos)):
            return False
        elif(not self.bkt_close(self.pos)):
            return False
        elif(not self.brace_open(self.pos)):
            return False
        while(True): #эквивалентно expr* - выполняется 0 или более раз
            if (not self.expr(self.pos)):
                break 
        if(not self.brace_close(self.pos)):
            return False      
        return True 

    def KW_WHILE(self, pos):
        if (self.tokens[self.pos][1] == "WHILE"):
            self.pos += 1
            return True
        else:
            return False    

    def brace_open(self, pos):
        if (self.tokens[self.pos][1] == "BRACE_OPEN"):
            self.pos += 1
            return True
        else:
            return False 

    def brace_close(self, pos):
        if (self.tokens[self.pos][1] == "BRACE_CLOSE"):
            self.pos += 1
            return True
        else:
            return False     

    def bkt_open(self, pos):
        if (self.tokens[self.pos][1] == "BRACKET_OPEN"):
            self.pos += 1
            return True
        else:
            return False

    def bkt_close(self, pos):
        if (self.tokens[self.pos][1] == "BRACKET_CLOSE"):
            self.pos += 1
            return True
        else:
            return False         
    
    def arif_op(self, pos):
        if (
            self.tokens[self.pos][1] == "MULT"        or
            self.tokens[self.pos][1] == "PLUS"        or
            self.tokens[self.pos][1] == "MINUS"       or
            self.tokens[self.pos][1] == "XDIVISIONOR"
        ):
            self.pos += 1
            return True
        else:
            return False

    def log_op(self, pos):
        if (
            self.tokens[self.pos][1] == "NOT"        or
            self.tokens[self.pos][1] == "AND"        or
            self.tokens[self.pos][1] == "OR"         or
            self.tokens[self.pos][1] == "XOR"        or
            self.tokens[self.pos][1] == "GRATER_EQ"  or
            self.tokens[self.pos][1] == "GRATER"     or
            self.tokens[self.pos][1] == "LESS_EQ"    or
            self.tokens[self.pos][1] == "LESS"       or 
            self.tokens[self.pos][1] == "EQUAL"      or
            self.tokens[self.pos][1] == "NOT_EQUAL"
        ):
            self.pos += 1
            return True
        else:
            return False

    def semicolon(self, pos):
        if (self.tokens[pos][1] == "SEMICOLON"):
            self.pos += 1
            return True        
        else:
            return False

def do_parse(tokens):
    p = Parser(tokens)
    return p.parse()            