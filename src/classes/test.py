from LinkedList import LinkedList

a = LinkedList()

for i in range(0,10):
    a.append(i)

a.print()
a.delete(a.getFirst().next)
print("")
a.print()