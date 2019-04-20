from sys import exit
import Executor as ex

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens #набор токенов после лексера
        self.pos = 0 #показывает текущий номер токена(позицию) в наборе токенов
        self.reverseNotation = [] #итоговая польская инверсная запись
        self.buffer = [] #буферный стек для операций
        self.calls  = [] #стек с адресами переходов ветвлений 

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
            self.pushInStack(self.tokens[self.pos])
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
            self.pushInStack(self.tokens[self.pos])
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
       
    #number -> int | float
    def number(self, pos):
        if (
            self.tokens[self.pos][1] == "INT"   or
            self.tokens[self.pos][1] == "FLOAT" or
            self.tokens[self.pos][1] == "TRUE"  or
            self.tokens[self.pos][1] == "FALSE"
        ):
            self.pushInStack(self.tokens[self.pos])
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

    #log_stmt -> log_value (log_op log_value)+
    def log_stmt(self, pos):
        if (not self.log_value(self.pos)):
            return False
        #эквивалентно (log_op log_value)+ -> 1 раз обязателен
        if (not self.log_op(self.pos) and not self.log_value(self.pos)):
            self.parseExeption("logical operation or logical value", self.tokens[self.pos][0])
            return False
        while(True): 
            if (not self.log_op(self.pos) and not self.log_value(self.pos)):
                break 
        return True

    #log_value -> [not_log] ( var | number | log_bkt_expr )
    def log_value(self, pos):
        self.log_not(self.pos)
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
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    def KW_ELSE(self, pos):
        if (self.tokens[self.pos][1] == "ELSE"):
            self.pushInStack(self.tokens[self.pos])
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
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False    

    def brace_open(self, pos):
        if (self.tokens[self.pos][1] == "BRACE_OPEN"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False 

    def brace_close(self, pos):
        if (self.tokens[self.pos][1] == "BRACE_CLOSE"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False     

    def bkt_open(self, pos):
        if (self.tokens[self.pos][1] == "BRACKET_OPEN"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    def bkt_close(self, pos):
        if (self.tokens[self.pos][1] == "BRACKET_CLOSE"):
            self.pushInStack(self.tokens[self.pos])
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
            self.pushInStack(self.tokens[self.pos])
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
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    def log_op(self, pos):
        if (
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
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    def log_not(self, pos):
        if (self.tokens[self.pos][1] == "NOT"):
            self.pos += 1
            return True
        else:
            return False

    def semicolon(self, pos):
        if (self.tokens[pos][1] == "SEMICOLON"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True        
        else:
            return False

    #Если входной токен число, переменная или ключ.слова ветвлений\циклов,
    #то добавляем его в общий стек. Иначе, добавляем токен в промежуточный стек(buffer)
    #buffer хранит операции, чтобы в правильном порядке формировать ПОЛИЗ в основном стеке
    def pushInStack(self, el):
        print(self.reverseNotation)
        print(str(self.buffer) + "\n====")
        #el -> token(velue, lexem, priority)ъ
        if (el[1] in ["WHILE"]):
            self.calls.append( len(self.reverseNotation) )
        elif (el[1] in 
        ["INT", "FLOAT", "FALSE", "TRUE", "ID"]):
            if (el[1] in ["IF", "ELSE", "WHILE"]):
                self.reverseNotation.append( 
                    (len(self.reverseNotation), "") )
            self.reverseNotation.append( (el[0], el[1]) )
        else:  
            if (el[0] == ")"): #выталкиваем всё в основной буфер до первой (
                while (self.endEl(self.buffer)[0] != "("):
                    self.reverseNotation.append(self.buffer.pop())
                self.buffer.pop()
            elif (el[0] == "}"): #выталкиваем всё в основной буфер до первой }
                while (self.endEl(self.buffer)[0] != "{"):
                    self.reverseNotation.append(self.buffer.pop())
                self.buffer.pop()  
            elif (el[0] != "(" and el[0] != "{" and len(self.buffer) != 0):
                #Если новый токен имеет меньший приоритет, чем последний в буффере, то
                #последний из буффера добавялется в основной стек, а новый заносится в буффер  
                if (el[2] < self.endEl(self.buffer)[2]):                 
                    if (el[1] == "SEMICOLON"):
                        #если встретился конец выражения, то переносим всё из буфера в основнйо стек
                        while (not self.endEl(self.buffer)[0] in
                        ["=", "-=", "+=", "*=", "/=", "//=", "++", "--"]):
                            val = self.buffer.pop()
                            self.reverseNotation.append( (val[0], val[1]) )
                    val = self.buffer.pop() 
                    self.reverseNotation.append( (val[0], val[1]) )

            if (not el[0] in [";", ")", "}"]):
                self.buffer.append(el)   
    
    def endEl(self, n):
        try:
            return n[len(n) - 1]
        except:
            return 0

def do_parse(tokens):
    p = Parser(tokens)
    if (p.parse()):
        return str(p.reverseNotation)       