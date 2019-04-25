from sys import exit

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens #набор токенов после лексера
        self.pos = 0 #показывает текущий номер токена(позицию) в наборе токенов
        self.poliz = [] #итоговая польская инверсная запись
        self.buffer = [] #буферный стек для операций
        self.addrsForFilling  = [] #хранит адреса ПОЛИЗa, куда потом нужно будет записать адрес перехода
        self.addrsJumps  = [] #хранит адреса перехода(только для while)
        self.calls = [] #стек вызовов операций while, if, else

    def parseExeption(self, expected, detected):
        print("\nParse error: detected " + "'" + detected +
             "', but " + "'" + expected + "' are expected!")
        exit(0)

    def endScript(self):
        return self.pos == len(self.tokens)

    def parse(self):
        return self.lang()

    #lang -> expr*
    def lang(self):
        while(not self.endScript()):
            if (not self.expr(self.pos)):
                self.parseExeption("expression", self.tokens[self.pos][0])
        return True    

    #expr -> assign | while_stmt | if_stmt
    def expr(self, pos):
        if not(
            self.assign(self.pos) or
            self.while_stmt(self.pos) or
            self.if_stmt(self.pos) or
            self.printing(self.pos) or
            self.inputting(self.pos)
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
       
    #number -> int | float | bool 
    def number(self, pos):
        if (
            self.tokens[self.pos][1] == "INT"   or
            self.tokens[self.pos][1] == "FLOAT" or
            self.tokens[self.pos][1] == "BOOL"
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

    #log_stmt -> comp_expr (log_op comp_expr)*
    def log_stmt(self, pos):
        if (not self.comp_expr(self.pos)):
            return False
        while(True): 
            if (self.log_op(self.pos)):
                if (not self.comp_expr(self.pos)):
                    self.parseExeption("compare expression", self.tokens[self.pos][0])
                    break
            else:
                break
        return True

    #comp_expr -> [log_not] (arif_stmt comp_op arif_stmt)
    def comp_expr(self, pos):
        if(self.log_not(self.pos)):
            pass
        if (self.arif_stmt(self.pos)):
            if(not self.comp_op(self.pos)):
                self.parseExeption("compare expression", self.tokens[self.pos][0])
                return False
            elif (not self.arif_stmt(self.pos)):
                self.parseExeption("arithmetic expression", self.tokens[self.pos][0])
                return False
        else:
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

    #printing -> KW_PRINT bkt_open arif_stmt bkt_close semicolon
    def printing(self, pos):
        if (not self.KW_PRINT(self.pos)):
            return False
        elif (not self.bkt_open(self.pos)):
            self.parseExeption("(", self.tokens[self.pos][0])
            return False
        elif (not self.str_stmt(self.pos)):
            self.parseExeption("string or arithmetic expression", self.tokens[self.pos][0])
            return False
        elif (not self.bkt_close(self.pos)):
            self.parseExeption(")", self.tokens[self.pos][0])
            return False
        elif (not self.semicolon(self.pos)):
            self.parseExeption(";", self.tokens[self.pos][0])
            return False
        else:
            return True
    
    def KW_PRINT(self, pos):
        if (self.tokens[self.pos][1] == "PRINT"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    #str_stmt -> substr (concat substr)*
    def str_stmt(self, pos):
        if (not self.substr(self.pos)):
            return False
        while(True): #эквивалентно (concat substr)*
            if (not self.concat(self.pos) and not self.substr(self.pos)):
                break   
        return True

    #substr -> string | arif_stmt
    def substr(self, pos):
        if (
            self.string(self.pos) or
            self.arif_stmt(self.pos)
        ):
            return True
        else:
            return False

    def string(self, pos):
        if (self.tokens[self.pos][1] == "STRING"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False  

    def concat(self, pos):
        if (self.tokens[self.pos][1] == "CONCAT"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    #inputting -> KW_INPUT bkt_open var bkt_close semicolon
    def inputting(self, pos):
        if (not self.KW_INPUT(self.pos)):
            return False
        elif (not self.bkt_open(self.pos)):
            self.parseExeption("(", self.tokens[self.pos][0])
            return False
        elif (not self.var(self.pos)):
            self.parseExeption("variable", self.tokens[self.pos][0])
            return False
        elif (not self.bkt_close(self.pos)):
            self.parseExeption(")", self.tokens[self.pos][0])
            return False
        elif (not self.semicolon(self.pos)):
            self.parseExeption(";", self.tokens[self.pos][0])
            return False
        else:
            return True

    def KW_INPUT(self, pos):
        if (self.tokens[self.pos][1] == "INPUT"):
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
            self.tokens[self.pos][1] == "AND" or
            self.tokens[self.pos][1] == "OR"  or
            self.tokens[self.pos][1] == "XOR"       
        ):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    def comp_op(self, pos):
        if (
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
            self.pushInStack(self.tokens[self.pos])
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
        #print(self.poliz)
        #print(str(self.buffer) + "\n====")
        if (el[1] in 
        ["INT", "FLOAT", "BOOL", "ID", "STRING"]):
            self.poliz.append( (el[0], el[1]) )
        elif (el[1] in ["WHILE", "IF", "ELSE"]):
            self.calls.append(el[1])
            self.buffer.append(el)
            if (el[1] in  ["ELSE"]):
                self.buffer.pop()
                self.addrsForFilling.append( len(self.poliz) )
                self.poliz.append ( 0 ) #Добавляем любой элемент, потом он заменится на переход
            elif (el[1] == "WHILE"):
                self.addrsJumps.append( len(self.poliz) )
        else:  
            if (el[0] == ")"):#выталкиваем всё в основной буфер до первой (
                while (self.endEl(self.buffer)[0] != "("):
                    value = self.buffer.pop()
                    self.poliz.append( (value[0], value[1]))
                self.buffer.pop()#убрали саму "("
                #если в буффере были оператторы ветвления, что фиксируем адрес для заполнения далее
                if (self.endEl(self.buffer)[1] in ["IF", "WHILE"]):
                        self.buffer.pop()
                        self.addrsForFilling.append( len(self.poliz) )
                        self.poliz.append ( 0 ) #Добавляем любой элемент, потом он заменится на переход
            elif (el[0] == "}"): #выталкиваем всё в основной буфер до первой {
                while (self.endEl(self.buffer)[0] != "{"):
                    value = self.buffer.pop()
                    self.poliz.append( (value[0], value[1]))
                self.buffer.pop()#убрали саму "{"
                lastCall = self.calls.pop()
                if (lastCall == "WHILE"):
                    self.poliz.append( (self.addrsJumps.pop(), "!") )
                    self.poliz[self.addrsForFilling.pop()] = (len(self.poliz), "!F")
                elif (lastCall == "IF"):
                    self.poliz[self.addrsForFilling.pop()] = (len(self.poliz) + 1, "!F") 
                elif (lastCall == "ELSE"):
                    self.poliz[self.addrsForFilling.pop()] = (len(self.poliz), "!")
                else:
                    #выполнится только если было IF без ELSE и для нормального ветвления,
                    #нужная заглушка. Если ELSE был, то на этот адрес будет записан адрес безусловного перехода
                    self.poliz.append( (None, None) )           
            elif (el[0] != "(" and el[0] != "{" and len(self.buffer) != 0):
                #Если новый токен имеет меньший приоритет, чем последний в буффере, то
                #последний из буффера добавялется в основной стек, а новый заносится в буффер  
                if (el[2] < self.endEl(self.buffer)[2]):                 
                    if (el[1] == "SEMICOLON"):
                        #если встретился конец выражения, то переносим всё из буфера в основнйо стек
                        while (not self.endEl(self.buffer)[0] in
                        ["=", "-=", "+=", "*=", "/=", "//=", "++", "--", "print", ".", "input"]):
                            val = self.buffer.pop()
                            self.poliz.append( (val[0], val[1]) )
                    val = self.buffer.pop() 
                    self.poliz.append( (val[0], val[1]) )

            if (not el[0] in [";", ")", "}"]):
                self.buffer.append(el)   
    
    def endEl(self, n):
        try:
            return n[len(n) - 1]
        except:
            return (None, None)

def do_parse(tokens):
    p = Parser(tokens)
    if (p.parse()):
        return p.poliz