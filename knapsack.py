import numpy
from collections import namedtuple

def insertItems():
    # Este es el ejemplo del fichero ks_4
    Item = namedtuple("Item", ['index', 'value', 'weight'])
    items = []
    bound = 0
    items.append(Item(0, 8, 4))
    items.append(Item(1, 10, 5))
    items.append(Item(2, 15, 8))
    items.append(Item(3, 4, 3))
    capacity = 11
    for i in items:
        bound += i.value
    return items, len(items), capacity, bound

class Node:

    def __init__(self, root, value, capacity, bound):
        self.root = root
        self.left = None
        self.right = None
        self.value = value
        self.room = capacity
        self.estimate = bound

    def insert(self, newValue, newRoom, newEstimate):
        newNode = Node(self, newValue, newRoom, newEstimate)
        if newNode.estimate < self.estimate:
            self.right = newNode
        elif newNode.estimate == self.estimate:
            self.left = newNode

# Print tree
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print([self.value, self.room, self.estimate]),
        if self.right:
            self.right.PrintTree()

def greedy(items, capacity, estimate):
    total = 0
    taken = []
    for item in items: 
        if capacity - item.weight >= 0:
            total += item.value
            capacity -= item.weight
            taken.append(1)
        else:
            estimate -= item.value
            taken.append(0)
    return total, capacity, estimate, taken

if __name__ == "__main__":
    items, item_count, capacity, bound = insertItems()

    # La primera busqueda sera greedy para llegar un nodo hoja
    greedyValue, room, estimate, takenGreedy = greedy(items, capacity, bound)
    result = Node(None, greedyValue, room, estimate)
    print("result: ", "value: " + str(result.value), "room: " + str(result.room), "estimate: " + str(result.estimate), sep=" --- ")
    print("taken of result", takenGreedy)

    # Empezar a expandir el arbol comparando con el estimate de result
    ## Asi habra algunas veces que ni tendra que ir hasta el nodo hoja
    ### Con la lista abierta primero meter un nodo (None, 0, 11, 37)
    """for item in items:
        check = O.pop()
        if item.value + check.value > result.estimate:"""