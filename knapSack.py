from collections import namedtuple


def insertItems():
    # Este es el ejemplo del fichero ks_4
    Item = namedtuple("Item", ['index', 'value', 'weight'])
    items = []
    # Index, value, weight
    items.append(Item(0, 8, 4))
    items.append(Item(1, 10, 5))
    items.append(Item(2, 15, 8))
    items.append(Item(3, 4, 3))
    return items


class Node:

    def __init__(self, root, eValue, eWeight, bound):
        self.father = root
        self.right = None
        self.left = None
        self.value = eValue
        self.weight = eWeight
        self.estimate = bound

    def insert(self, newValue, newRoom, newEstimate):
        newNode = Node(self, newValue, newRoom, newEstimate)
        if newNode.estimate < self.estimate:
            self.right = newNode
        elif newNode.estimate == self.estimate:
            self.left = newNode

    def printTree(self):
        if self.left:
            self.left.printTree()
        print([self.value, self.weight, self.estimate]),
        if self.right:
            self.right.printTree()

if __name__ == "__main__":
    # Inserta los items y crea el taken
    items = insertItems()
    taken = [0]*11
    estimate = 0
    for i in items:
        estimate += i.value

    root = Node(None, 0, 11, estimate)
    act = root
    i = 0

    newEstimate = 0
    while root.left is None or root.right is None or act.father is not None:
        if act.left is None and act.weight - items[i].weight >= 0:
            act.insert(act.value + items[i].value, act.weight - items[i].weight, act.estimate)
            ant = act
            act = act.left
        else:
            act.insert(act.value, act.weight, act.estimate - items[i].value)
            ant = act
            act = act.right
        i += 1

        if act.estimate < newEstimate or i == len(items):
            if act.estimate > newEstimate:
                newEstimate = act.estimate
            i -= 1
            while ant.right is not None and ant.father is not None:
                act = ant
                ant = act.father
                i -= 1
            act = ant
            ant = act.father

    print(root.printTree())
    print(newEstimate)

