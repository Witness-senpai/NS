#Стек-машина, которая выполняет сам код
class StackMachine:
    def __init__(self, poliz):
        self.poliz = poliz #ПОльская ИНверсная запись, полученная после парсера
        self.stack = [] #основной стек для выполнения операций
        self.variables = {} #cловарь c переменными: varID -> varValue
        self.pos = 0 #номер текущего элемента полиза

    def stackEnd(self):
        if (len(self.stack) >= 1):
            return self.stack[len(self.stack) - 1]
        else:
            return (None, None)

    #выполняет вычисление на стек машине, пока не дошли до конца ПОЛИЗа
    def process(self):
        while (self.pos < len(self.poliz)):
            self.stack.append(self.poliz[self.pos])
            self.pos += 1

            if (self.stackEnd()[1] == "!"):
                self.pos = self.stack.pop()[0]
            elif(self.stackEnd()[1] == "!F"):
                adr = self.stack.pop()[0]
                if (not self.stackEnd()[0]):
                    self.pos = adr
                self.stack.pop() #выталкиваем оставшийся ненужный bool-результат
            elif (self.stackEnd()[1] == "PRINT"):
                self.stack.pop() #убираем из стека print
                self.printing(self.stack.pop()[0])
            elif (self.stackEnd()[1] == "INPUT"):
                self.stack.pop() #убираем из стека read
                self.inputting(self.stack.pop()[0])
            elif (self.stackEnd() != None):
                #если на вершине стека какая-то операция над операндами, то выполняем
                if (not self.stackEnd()[1] in 
                ["INT", "FLOAT", "BOOL", "ID", "STRING"]):
                    self.calculate()
            
    def printing(self, value):
        if (self.variables.get(value) != None):
            print("> " + str(self.variables.get(value)))
        else:
            print("> " + str(value))

    def inputting(self, var):
        if (self.variables.get(var) != None):
            v = str(input(">>"))
            self.variables[var] = self.convertType(v)
        else:
            print("Error: variable '" + var + "' is not defined")
            exit()

    def convertType(self, value):
        try:
            if (value.find('"') != -1):
                return str(value)
            elif (value.find('.') != -1):
                return float(value)
            else:
                return int(value)
        except:
            print("Error: unknown type of value '" + value + "'")
            exit()

    def checkDef(self, var):
        if (type(var) is tuple):
            if (self.variables.get(var[0]) == None and var[1] == "ID"):
                print("Error: variable '" + var[0] + "' is not defined")
                exit()

    def getValue(self, var):
        if var[1] == "INT":
            return int(var[0])
        elif (var[1] == "FLOAT"):
            return float(var[0])
        elif (var[1] == "BOOL"):
            return bool(var[0])
        else:
            return str(var[0])

    def calculate(self):
        op = self.stack.pop()[0]

        #для унарных операторов берём только 1 значение из стека
        if (not op in ["++", "--", "not"]):
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
            else:
                #для других операторов нужно только значение двух операндов, получаем значение вторго и выполняем
                a = self.variables.get(a[0]) if self.variables.get(a[0]) != None else self.getValue(a)
                
                if (op == "."):
                    self.stack.append(self.concat(a, b))
                elif (op == "+"):
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
                elif (op == "and"):
                    self.stack.append(self.l_and(a,b))
                elif (op == "or"):
                    self.stack.append(self.l_or(a,b))
                elif (op == "xor"):
                    self.stack.append(self.l_xor(a,b))
                elif (op == ">"):
                    self.stack.append(self.l_greater(a,b))
                elif (op == ">="):
                    self.stack.append(self.l_greaterEq(a,b))
                elif (op == "<"):
                    self.stack.append(self.l_less(a,b))
                elif (op == "<="):
                    self.stack.append(self.l_lessEq(a,b))
                elif (op == "!="):
                    self.stack.append(self.l_notEq(a,b))
                elif (op == "=="):
                    self.stack.append(self.l_equal(a,b))
                elif (op == "not"):
                    self.stack.append(self.l_not(a))

    def concat(self, val1, val2):
        return str(val1) + str(val2), "STRING"

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
        res = num1 ** num2
        if (type(res) == float):
            return res, "FLOAT"
        else:
            return res, "INT"  

    def div(self, num1, num2):
        if num2 == 0:
            print("Error: division by zero")
            exit() 
        return float(num1) / float(num2), "FLOAT"
    
    def mod(self, num1, num2):
        if (type(num1) == float or type(num2) == float):
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
    
    def l_greater(self, num1, num2):
        try:
            return num1 > num2, "BOOL"
        except:
            self.compareException(num1, num2)
    
    def l_greaterEq(self, num1, num2):
        try:
            return num1 >= num2, "BOOL"
        except:
            self.compareException(num1, num2)

    def l_less(self, num1, num2):
        try:
            return num1 < num2, "BOOL"
        except:
            self.compareException(num1, num2)

    def l_lessEq(self, num1, num2):
        try:
            return num1 <= num2, "BOOL"
        except:
            self.compareException(num1, num2)
  
    def l_notEq(self, num1, num2):
        try:
            return num1 != num2, "BOOL"
        except:
            self.compareException(num1, num2)

    def l_equal(self, num1, num2):
        try:
            return num1 == num2, "BOOL"
        except:
            self.compareException(num1, num2)

    def l_not(self, num):
        if (type(num) == bool):
            return not num, "BOOL"
        else:
            self.pushError("Error: using LOGICAL NOT for non-logical expression")

    def l_or(self, num1, num2):
        if (type(num1) == bool and type(num2) == bool):
            return num1 or num2, "BOOL"
        else:
           self.pushError("Error: using LOGICAL OR for non-logical expression")

    def l_and(self, num1, num2):
        if (type(num1) == bool and type(num2) == bool):
            return num1 and num2, "BOOL"
        else:
            self.pushError("Error: using LOGICAL AND for non-logical expression")
    
    def l_xor(self, num1, num2):
        if (type(num1) == bool and type(num2) == bool):
            return ((not num1) and num2) or ((num1 and (not num2))), "BOOL"
        else:
            self.pushError("Error: using LOGICAL XOR for non-logical expression")

    def pushError(self, error):
        print(error)
        exit()

    def compareException(self, n1, n2):
        self.pushError("Error: impossible to compare '" +
        str(n1) + "' and '" + str(n2) + "' values")

def do_calculate(poliz):
    machine = StackMachine(poliz)
    machine.process()






