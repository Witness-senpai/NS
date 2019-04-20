from sys import exit
import Executor as ex

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens #набор кокенов после лексера
        self.pos = 0 #показывает текущий номер токена(позицию) в наборе токенов
        self.stack = ex.StackMachine() #cтек-машина, которая будет выполнять код в ПОЛИЗ

    def parseExeption(self, expected, detected):
        print("\nParse error: detected " + "'" + detected +
             "', but " + "'" + expected + "' are expected!")
        exit()     

    def endScript(self):
        return self.pos == len(self.tokens)

    def parse(self):
        return self.lang()

    #lang -> expr* KW_END
    def lang(self):
        while(not self.endScript()):
            if (not self.expr(self.pos)):
                if (not self.tokens[self.pos][1] == "END"):
                    return False 
                self.pos += 1
        print("============\n" + str(self.stack.variables))
        return True    

    #expr -> assign | while_stmt | if_stmt
    def expr(self, pos):
        if not(
            self.assign(self.pos) or
            self.while_stmt(self.pos) or
            self.if_stmt(self.pos)
            ):
            return False
        return True  

    #assign -> var ((assign_op arif_stmt) | inc_dec) semicolon
    def assign(self, pos):
        if (not self.var(self.pos)):
            return False
        if (self.assign_op(self.pos)):
            if (not self.arif_stmt(self.pos)):
                self.parseExeption("arithmetic expression", self.tokens[self.pos][0])
                return False
        elif (not self.inc_dec(self.pos)):
            self.parseExeption("=, ++ or --", self.tokens[self.pos][0])
            return False       
        if (not self.semicolon(self.pos)):
            self.parseExeption(";", self.tokens[self.pos][0])
            return False
        return True

    def var(self, pos):
        if self.tokens[self.pos][1] == "ID":
            self.stack.push(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False  

    def assign_op(self, pos):
        if (
            self.tokens[self.pos][1] == "ASSIGN" or
            self.tokens[self.pos][1] == "PLUS_ASSIGN" or
            self.tokens[self.pos][1] == "MINUS_ASSIGN" or
            self.tokens[self.pos][1] == "MULT_ASSIGN" or
            self.tokens[self.pos][1] == "DIVISION_ASSIGN" or
            self.tokens[self.pos][1] == "MOD_ASSIGN"
            ): 
            self.stack.push(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    #arif_stmt -> value (arif_op value)*
    def arif_stmt(self, pos):
        if (not self.value(self.pos)):
            return False
        while(True): #эквивалентно (arif_op value)*
            if (not self.arif_op(self.pos) and not self.value(self.pos)):
                break   
        return True

    #value -> var | number | bkt_expr
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
            self.stack.push(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    #bkt_expr -> bkt_open arif_stmt bkt_close
    def bkt_expr(self, pos):
        if (not self.bkt_open(self.pos)):
            return False
        elif(not self.arif_stmt(self.pos)):
            self.parseExeption("arithmetic expression", self.tokens[self.pos][0])
            return False
        elif(not self.bkt_close(self.pos)):
            self.parseExeption(")", self.tokens[self.pos][0])
            return False
        return True

    #log_stmt -> log_value (log_op log_value)*
    def log_stmt(self, pos):
        if (not self.log_value(self.pos)):
            return False
        while(True): #эквивалентно (log_op log_value)*
            if (not self.log_op(self.pos) and not self.log_value(self.pos)):
                break 
        return True

    #log_value -> var | number | log_bkt_expr
    def log_value(self, pos):
        if not(
            self.var(self.pos)    or
            self.number(self.pos) or
            self.log_bkt_expr(self.pos)
            ):
            return False
        return True

    #log_bkt_expr -> bkt_open log_stmt bkt_close
    def log_bkt_expr(self, pos):
        if (not self.bkt_open(self.pos)):
            return False
        elif(not self.log_stmt(self.pos)):
            self.parseExeption("logical expression", self.tokens[self.pos][0])
            return False
        elif(not self.bkt_close(self.pos)):
            self.parseExeption(")", self.tokens[self.pos][0])
            return False
        return True    

    #if_stmt -> KW_IF bkt_open log_stmt bkt_close brace_open expr* brace_close [else_stmt]
    def if_stmt(self, pos):
        if (not self.KW_IF(self.pos)):
            return False
        elif(not self.bkt_open(self.pos)):
            self.parseExeption("(", self.tokens[self.pos][0])
            return False
        elif(not self.log_stmt(self.pos)):
            self.parseExeption("logical expression", self.tokens[self.pos][0])
            return False
        elif(not self.bkt_close(self.pos)):
            self.parseExeption(")", self.tokens[self.pos][0])
            return False
        elif(not self.brace_open(self.pos)):
            self.parseExeption("{", self.tokens[self.pos][0])
            return False
        while(True): #эквивалентно expr* - выполняется 0 или более раз
            if (not self.expr(self.pos)):
                break     
        if(not self.brace_close(self.pos)):
            self.parseExeption("}", self.tokens[self.pos][0])
            return False
        #Выполнение else_stmt не обязательно и не повлияет на выполнение if_stmt
        if (self.tokens[self.pos][1] == "ELSE"):
            if (not self.else_stmt(self.pos)):
                return False
        return True

    #else_stmt -> KW_ELSE brace_open expr* brace_close
    def else_stmt(self, pos):
        if (not self.KW_ELSE(self.pos)):
            return False
        elif(not self.brace_open(self.pos)):
            self.parseExeption("{", self.tokens[self.pos][0])
            return False
        while(True): #эквивалентно expr* - выполняется 0 или более раз
            if (not self.expr(self.pos)):
                break   
        if(not self.brace_close(self.pos)):
            self.parseExeption("}", self.tokens[self.pos][0])
            return False
        return True    

    def KW_IF(self, pos):
        if (self.tokens[self.pos][1] == "IF"):
            self.stack.push(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    def KW_ELSE(self, pos):
        if (self.tokens[self.pos][1] == "ELSE"):
            self.stack.push(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False    

    #while_stmt -> KW_WHILE bkt_open log_stmt bkt_close brace_open expr* brace_close        
    def while_stmt(self, pos):
        if (not self.KW_WHILE(self.pos)):
            return False
        elif(not self.bkt_open(self.pos)):
            self.parseExeption("(", self.tokens[self.pos][0])
            return False
        elif(not self.log_stmt(self.pos)):
            self.parseExeption("logical expression", self.tokens[self.pos][0])
            return False
        elif(not self.bkt_close(self.pos)):
            self.parseExeption(")", self.tokens[self.pos][0])
            return False
        elif(not self.brace_open(self.pos)):
            self.parseExeption("{", self.tokens[self.pos][0])
            return False
        while(True): #эквивалентно expr* - выполняется 0 или более раз
            if (not self.expr(self.pos)):
                break 
        if(not self.brace_close(self.pos)):
            self.parseExeption("}", self.tokens[self.pos][0])
            return False      
        return True 

    def KW_WHILE(self, pos):
        if (self.tokens[self.pos][1] == "WHILE"):
            self.stack.push(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False    

    def brace_open(self, pos):
        if (self.tokens[self.pos][1] == "BRACE_OPEN"):
            self.stack.push(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False 

    def brace_close(self, pos):
        if (self.tokens[self.pos][1] == "BRACE_CLOSE"):
            self.stack.push(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False     

    def bkt_open(self, pos):
        if (self.tokens[self.pos][1] == "BRACKET_OPEN"):
            self.stack.push(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    def bkt_close(self, pos):
        if (self.tokens[self.pos][1] == "BRACKET_CLOSE"):
            self.stack.push(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False         
    
    #Не обязателен, поэтому всегда возвращает True, чтобы не прерывать программу, главное
    #что он запишется в список токенов если есть
    def inc_dec(self, pos):
        if (
            self.tokens[self.pos][1] == "INC" or
            self.tokens[self.pos][1] == "DEC" 
        ):
            self.stack.push(self.tokens[self.pos])
            self.pos += 1
        return True

    def arif_op(self, pos):
        if (
            self.tokens[self.pos][1] == "MULT"        or
            self.tokens[self.pos][1] == "PLUS"        or
            self.tokens[self.pos][1] == "MINUS"       or
            self.tokens[self.pos][1] == "DIVISION"    or
            self.tokens[self.pos][1] == "MOD"         or
            self.tokens[self.pos][1] == "POW"
        ):
            self.stack.push(self.tokens[self.pos])
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
            self.stack.push(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    def semicolon(self, pos):
        if (self.tokens[pos][1] == "SEMICOLON"):
            self.stack.push(self.tokens[self.pos])
            self.pos += 1
            return True        
        else:
            return False      

def do_parse(tokens):
    p = Parser(tokens)
    return p.parse()            