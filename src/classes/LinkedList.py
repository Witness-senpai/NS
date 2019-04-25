class LinkedList:
    def __init__(self, value=None):
        self.__size = 0
        self.__first = Node()
        self.__last  = Node()

    def append(self, value):
        #Если введён самый первый элемент списка
        if (self.__first.value == None):
            self.__first = Node(value, value, value)
            self.__last = self.__first
        else:
            #Запоминаем редыдущий последний элемент
            oldEndNode = self.__last
            #Добавялем новый последний элемент
            self.__last = Node(value, self.__first, oldEndNode)
            #Предыдущий последний теперь будет ссылаться на новый послений элемент
            oldEndNode.setNext(self.__last)
            #Самый первый элемент должен ссылаться на новый последний
            self.__first.setPrev(self.__last)
        self.__size += 1
    
    def delete(self, node):
        node.prev.setNext(node.next)
        node.next.setPrev(node.prev)
        self.__size -= 1

    def getLast(self):
        return self.__last

    def getFirst(self):
        return self.__first
    
    def getSize(self):
        return self.__size
    
    def print(self):
        head = self.getFirst()
        for i in range(0, self.getSize()):      
            print(str(head.value), end=" ")
            head = head.next


class Node:
    def __init__(self, value=None, next=None, prev=None):
        self.value = value
        self.next = next
        self.prev = prev
    
    def delete(self):
        self.next.setPrev(self.prev)
        self.prev.setNext(self.next)
        


    def getValue(self):
        return self.value
    
    def setNext(self, next):
        self.next = next
    
    def setPrev(self, prev):
        self.prev = prev
    

