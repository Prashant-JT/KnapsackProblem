from collections import namedtuple
import os
import gc

Item = namedtuple("Item", ['index', 'value', 'weight'])


# El método te devuelve la lista de items rellena, item_count y capacity
def insertItems():
    items = []
    item_count = 0
    capacity = 0
    bound = 0

    # Imprime el/los ficheros de la carpeta
    for dirname, _, filenames in os.walk('data'):
        for filename in filenames:
            print(os.path.join(dirname, filename))

    # Abre el primer fichero (debe haber una carpeta llamada "data" en el cual puede poner el fichero que quiere leer)
    # la carpeta data debe estar en el mismo directorio en el cual se encuentra este proyecto
    for dirname, _, filenames in os.walk('data'):
        for filename in filenames:
            full_name = dirname + '/' + filename
            with open(full_name, 'r') as input_data_file:
                input_data = input_data_file.read()

                lines = input_data.split('\n')

                firstLine = lines[0].split()
                item_count = int(firstLine[0])
                capacity = int(firstLine[1])

                j = 1
                for i in range(1, item_count + 1):
                    line = lines[i]
                    parts = line.split()
                    if int(parts[1]) <= capacity:
                        items.append(Item(j - 1, int(parts[0]), int(parts[1])))
                        bound += int(parts[0])
                        j = j + 1
                item_count = len(items)
                break
    return items, item_count, capacity


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


def valueWeight(it):
    return it.value / it.weight


if __name__ == "__main__":
    items, item_count, capacity = insertItems()
    sortedItems = items.copy()
    sortedItems.sort(reverse=True, key=valueWeight)
    taken = [0] * len(items)

    estimate = 0
    weights = 0

    for i in sortedItems:
        if weights == capacity:
            break
        if weights + i.weight <= capacity:
            estimate += i.value
            weights += i.weight
        else:
            res = capacity - weights
            weights = capacity
            estimate += (res * i.value) / i.weight

    root = Node(None, 0, capacity, estimate)
    act = root
    i = 0

    result = Node(None, 0, 0, 0)

    while root.left is None or root.right is None or act.father is not None:
        if act.left is None and act.weight - items[i].weight >= 0:
            act.insert(act.value + items[i].value, act.weight - items[i].weight, act.estimate)
            ant = act
            act = ant.left
        else:
            act.insert(act.value, act.weight, act.estimate - items[i].value)
            ant = act
            act = ant.right
        i += 1

        if act.estimate < result.estimate or i == len(items):
            if act.estimate > result.estimate:
                result = act
            i -= 1
            while ant.right is not None and ant.father is not None:
                act = ant
                ant = act.father
                i -= 1
            act = ant
            ant = act.father

    print(result.estimate)

    i = len(items) - 1
    aux = result.father
    while aux is not None:
        if aux.value != result.value:
            taken[i] = 1
        else:
            taken[i] = 0
        result = result.father
        aux = aux.father
        i -= 1

    print("taken vector: ", taken)
