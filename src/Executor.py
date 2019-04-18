#Класс переменной, которой будет опперировать стек-машина
#
class Var:
    def __init__(self, ID, value):
        self.ID = ID
        self.velue = value


#Стек-машина, которая выполняет сам код
class StackMachine:
    def __init__(self):
        self.stack  = [] #основной стек для выполнения операций в ПОЛИЗ
        self.buffer = [] #промежуточный стек для упорядочивания приоритетов
        self.variables = {}

    #Если входной токен число, переменная или ключ.слова ветвлений\циклов,
    #то добавляем его в общий стек. Иначе, добавляем токен в промежуточный стек(buffer)
    #buffer хранит операции, чтобы в правильном порядке формировать ПОЛИЗ в основном стеке
    def push(self, el): #el -> token(velue, lexem, priority)
        if (el[1] in ["NUMBER", "FLOAT_NUMBER", "ID", "IF", "ELSE", "WHILE"]):
            self.stack.append(el)
        else:
            self.buffer.append(el)


