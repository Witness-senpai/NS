from LinkedList import LinkedList
from HashSet import HashSet
import random

a = LinkedList()

for i in range(0,10):
    a.append(i)

b = a

a.print()
a.delete(a.getFirst().getNext())
print("")
a.print()

print("\n===============")

h = HashSet()

h.add("11")
h.add(1)
h.add(1)
h.add(5333)
h.add(5)
h.add(2)
h.add(4)
h.add(555)
h.add(555)

h.print()
print(str(h.getSize()))
print(h.inSet(1))

