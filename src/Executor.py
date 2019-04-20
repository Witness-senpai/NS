
#Стек-машина, которая выполняет сам код
class StackMachine:
    def __init__(self):
        self.stack  = [] #основной стек для выполнения операций в ПОЛИЗ
        self.buffer = [] #промежуточный стек для упорядочивания приоритетов
        self.variables = {} #cловарь varID -> getValue

    #Если входной токен число, переменная или ключ.слова ветвлений\циклов,
    #то добавляем его в общий стек. Иначе, добавляем токен в промежуточный стек(buffer)
    #buffer хранит операции, чтобы в правильном порядке формировать ПОЛИЗ в основном стеке
    def push(self, el): #el -> token(velue, lexem, priority)
        print(str(self.stack) + "\n")
        print(str(self.buffer) + "\n")
        print(str(self.variables) + "\n=====\n")
        if (el[1] in ["INT", "FLOAT", "ID", "IF", "ELSE", "WHILE"]):
            self.stack.append(el)
        else:  
            if (el[0] == ")"): #выталкиваем всё в основной буфер до первой (
                while (self.endEl(self.buffer)[0] != "("):
                    self.stack.append(self.buffer.pop())
                    self.calculate() 
                self.buffer.pop()
            elif (el[0] == "}"): #выталкиваем всё в основной буфер до первой }
                while (self.endEl(self.buffer)[0] != "{"):
                    self.stack.append(self.buffer.pop())
                    self.calculate() 
                self.buffer.pop()  
            elif (el[0] != "(" and el[0] != "{" and len(self.buffer) != 0):
                #Если новый токен имеет меньший приоритет, чем последний в буффере, то
                #последний из буффера добавялется в основной стек, а новый заносится в буффер  
                if (el[2] < self.endEl(self.buffer)[2]):                 
                    if (el[1] == "SEMICOLON"):
                        #если встретился конец вырадения, то выполняем весь стек до конца(до эл. присвоения)
                        while (not self.endEl(self.buffer)[0] in
                        ["=", "-=", "+=", "*=", "/=", "//=", "++", "--"]):
                            self.stack.append(self.buffer.pop())
                            self.calculate()  
                    self.stack.append(self.buffer.pop())
                    self.calculate()  

            if (not el[0] in [";", ")", "}"] ):
                self.buffer.append(el)

            try:
                if (not self.endEl(self.stack)[1] in 
                ["INT", "FLOAT", "ID", "IF", "ELSE", "WHILE"]):
                    self.calculate()
            except:
                pass

    def endEl(self, stack):
        try:
            return stack[len(stack) - 1]
        except:
            return 0

    def checkDef(self, var):
        if (type(var) is tuple):
            if (self.variables.get(var[0]) == None and var[1] == "ID"):
                print("Error: variable '" + var[0] + "' is not defined")
                exit()

    def getValue(self, var):
        return int(var[0]) if var[1] == "INT" else float(var[0])

    def calculate(self):
        op = self.stack.pop()[0]

        #для унарных операторов берём только 1 значение из стека
        if (not op in ["++", "--"]):
            b = self.stack.pop()
            a = self.stack.pop()
        else:
            a = self.stack.pop()
            b = (0, "INT") #костыль

        #сначала проверяем, если это оператор присвоения,
        #то переменная будет перезаписана или проинициализирована
        if (op == "="):
            a = a[0]
            #Это либо значение переменной либо непосредственно число
            b = b[0] if b[1] == "ID" else self.getValue(b)
            self.assign(a, b)
        #В противном случае, в других операциях будут использоваться уже сущ. переменные или числа
        else:
            #проверяем, если использована необъявленная переменная
            self.checkDef(a)
            self.checkDef(b)

            #для операторов которые меняют значение переменной, нужно имя переменной для обращения и второе число
            b = self.variables.get(b[0]) if self.variables.get(b[0]) != None else self.getValue(b)
            if (op == "++"):
                self.inc(a[0])
            elif (op == "--"):
                self.dec(a[0])    
            elif (op == "-="):
                self.minusAssign(a[0], b)
            elif (op == "+="):
                self.plusAssign(a[0],  b)
            elif (op == "*="):
                self.multAssign(a[0],  b)
            elif (op == "/="):
                self.divAssign(a[0],   b)
            elif (op == "//="):
                self.modAssign(a[0],   b)
            
            a = self.variables.get(a[0]) if self.variables.get(a[0]) != None else self.getValue(a)

            if (op == "+"):
                self.stack.append(self.plus(a, b))
            elif (op == "-"):
                self.stack.append(self.minus(a, b))
            elif (op == "*"):
                self.stack.append(self.mult(a,b))
            elif (op == "**"):
                self.stack.append(self.pow(a,b))
            elif (op == "/"):
                self.stack.append(self.div(a,b))
            elif (op == "//"):
                self.stack.append(self.mod(a,b))

    def inc(self, var):
        self.variables[var] = self.variables.get(var) + 1

    def dec(self, var):
        self.variables[var] = self.variables.get(var) - 1

    def assign(self, num1, num2):
        self.variables[num1] = self.variables[num2] if self.variables.get(num2) != None else num2

    def plus(self, num1, num2):
        if (type(num1) == float or type(num2) == float):
            return num1 + num2, "FLOAT"
        else:
            return num1 + num2, "INT" 

    def minus(self, num1, num2):
        if (type(num1) == float or type(num2) == float):
            return (num1 - num2, "FLOAT")
        else:
            return (num1 - num2, "INT") 

    def mult(self, num1, num2):
        if (type(num1) == float or type(num2) == float):
            return num1 * num2, "FLOAT"
        else:
            return num1 * num2, "INT" 

    def pow(self, num1, num2):
        if (type(num1) == float or type(num2) == float):
            return num1 ** num2, "FLOAT"
        else:
            return num1 ** num2, "INT"  

    def div(self, num1, num2):
        if num2 == 0:
            print("Error: division by zero")
            exit() 
        return float(num1) / float(num2), "FLOAT"
    
    def mod(self, num1, num2):
        if (type(num1) != float and type(num2) != float):
            print("Error: modulus from float")
            exit()
        elif num2 == 0:
            print("Error: modulus by zero")
            exit()
        return num1 % num2, "INT"

    def minusAssign(self, var, num):
        self.variables[var] = self.variables.get(var) - num
    
    def plusAssign(self, var, num):
        self.variables[var] = self.variables.get(var) + num
    
    def multAssign(self, var, num):
        self.variables[var] = self.variables.get(var) * num

    def divAssign(self, var, num):
        if num != 0:
            self.variables[var] = self.variables.get(var) / float(num)
        else:
            print("Error: division by zero")
            exit() 

    def modAssign(self, var, num):
        if (type(self.variables.get(var)) != float and type(num) != float):
            print("Error: modulus from float")
            exit()
        elif num == 0:
            print("Error: modulus by zero")
            exit()
        else:
            self.variables[var] = self.variables.get(var) % num 







