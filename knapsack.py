import numpy
from collections import namedtuple

def insertItems():
    # Este es el ejemplo del fichero ks_4
    Item = namedtuple("Item", ['index', 'value', 'weight'])
    items = []
    items.append(Item(0, 8, 4))
    items.append(Item(1, 10, 5))
    items.append(Item(2, 15, 8))
    items.append(Item(3, 4, 3))
    return items

class Node:

    def __init__(self, value, capacity, bound):
        self.root = None
        self.left = None
        self.right = None
        self.value = value
        self.room = capacity
        self.estimate = bound

    def insert(self, newValue, newRoom, newEstimate):
        newNode = Node(newValue, newRoom, newEstimate)
        newNode.root = self
        if newNode.estimate < self.estimate:
            if self.right is None:
                self.right = newNode
            else:
                self.right.insert(newNode.value, newNode.room, newNode.estimate)
        elif newNode.estimate == self.estimate:
            if self.left is None:
                self.left = newNode
            else:
                self.left.insert(newNode.value, newNode.room, newNode.estimate)  

# Print tree
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print([self.value, self.room, self.estimate]),
        if self.right:
            self.right.PrintTree()

if __name__ == "__main__":
    #Inserta los items y crea el taken
    items = insertItems()
    taken = [0]*11
    
    #Calcula la informacion del nodo raiz y la crea: VALUE ROOM ESTIMATE
    estimate = 0
    for i in items:
        estimate += i.value
    act = Node(0, 11, estimate)
    ant = None
    res = None
    root = act
    
    def searchChild(act, ant, pos):
        if res == None:
            for item in items:
                if act.room - item.weight >= 0:
                    act.insert(act.value + item.value, act.room - item.weight, act.estimate)
                    ant = act
                    act = ant.left
                else:
                    act.insert(act.value, act.room, act.estimate - item.value)
                    ant = act
                    act = ant.right
            return ant, act, root
        else:
            if res.value < ant.estimate - items[pos].value:
                ant.insert(ant.value, ant.room, ant.estimate - items[pos].value)
                act = ant.right
                ant = act.root
            for i in range(pos + 1, len(items)):
                if res.value < ant.estimate - items[i].value:
                    if ant.room - items[i].weight >= 0:
                        ant.insert(act.value + items[i].value, act.room - items[i].weight, act.estimate)
                        act = ant.left
                        ant = act.root
                    else:
                        ant.insert(act.value, act.room, act.estimate - items[i].value)
                        act = ant.right
                        ant = act.root
            return ant, act, root
    
    def reverseTree(ant, act):
        i = len(items) - 1
        while (True):
            if ant == root: break
            if ant.right == None:
                ant1, act1, root1 = searchChild(act, ant, i)
                res2 = act1
                i = len(items) - 1
            ant = ant.root
            act = act.root
            i -= 1
        return ant, act

    ant, act, root = searchChild(act, ant, 0)
    res = act
    
    a, s = reverseTree(ant, act)
    
    """ant = ant.root
    act = act.root
    del(root)
    i = len(items) - 1

    while (act.right != None):
        ant = ant.root
        act = act.root
        i -= 1
    
    res2 = completeTree(res, act, i)
    print(ant.value, ant.estimate)
    print(act.value, act.estimate)
    print(i)"""

    print(root.PrintTree())