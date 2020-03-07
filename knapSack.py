from collections import namedtuple
import os
import time
import gc

Item = namedtuple("Item", ['index', 'value', 'weight'])


# El método te devuelve la lista de items rellena, item_count y capacity
def insertItems():
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


def values(it):
    return it.value


def weights(it):
    return it.weight


def valuesWeight(it):
    return it.value / it.weight


def greedy(items, capacity):
    itemsVW = items.copy()
    itemsVW.sort(reverse=True, key=valuesWeight)
    itemsW = items.copy()
    itemsW.sort(key=weights)
    items.sort(reverse=True, key=values)

    valueGreedyV = valueGreedyVW = valueGreedyW = 0
    weightV = weightVW = weightW = 0
    takenGreedyV = [0] * len(items)
    takenGreedyVW = [0] * len(items)
    takenGreedyW = [0] * len(items)

    def checkWeights(_takenGreedy, _weight, _item, _valueGreedy):
        if _weight + _item.weight <= capacity:
            _takenGreedy[_item.index] = 1
            _valueGreedy += _item.value
            _weight += _item.weight
        return _takenGreedy, _weight, _valueGreedy

    for itemV, itemVW, itemW in zip(items, itemsVW, itemsW):
        if weightV == capacity and weightVW == capacity and weightW == capacity:
            break
        takenGreedyV, weightV, valueGreedyV = checkWeights(takenGreedyV, weightV, itemV, valueGreedyV)
        takenGreedyVW, weightVW, valueGreedyVW = checkWeights(takenGreedyVW, weightVW, itemVW, valueGreedyVW)
        takenGreedyW, weightW, valueGreedyW = checkWeights(takenGreedyW, weightW, itemW, valueGreedyW)

    del (itemsW)
    del (itemsVW)
    gc.collect()
    valueGreedy = max(valueGreedyV, valueGreedyVW, valueGreedyW)

    if valueGreedy == valueGreedyV:
        del (takenGreedyVW)
        del (takenGreedyW)
        gc.collect()
        return valueGreedy, takenGreedyV
    elif valueGreedy == valueGreedyVW:
        del (takenGreedyV)
        del (takenGreedyW)
        gc.collect()
        return valueGreedy, takenGreedyVW
    else:
        del (takenGreedyV)
        del (takenGreedyVW)
        gc.collect()
        return valueGreedy, takenGreedyW


def process(sortedItems, capacityI):
    items1 = sortedItems.copy()
    items1.sort(reverse=True, key=valuesWeight)

    sortedItems.sort(reverse=True, key=valuesWeight)
    taken = [0] * len(sortedItems)

    estimate = 0
    weights = 0

    for x in sortedItems:
        if weights + x.weight <= capacityI:
            estimate += x.value
            weights += x.weight
        else:
            res = capacityI - weights
            estimate += (res * x.value) / x.weight
            break
    root = Node(None, 0, capacityI, estimate)
    act = root
    i = 0

    result = Node(None, 0, 0, 0)

    start = time.time()
    while root.right is None or act.father is not None:
        if act.left is None and act.weight - items1[i].weight >= 0:
            act.insert(act.value + items1[i].value, act.weight - items1[i].weight, act.estimate)
            ant = act
            act = act.left
        else:
            act.insert(act.value, act.weight, act.estimate - items1[i].value)
            ant = act
            act = ant.right
        i += 1
        end = time.time()

        if end - start >= 15:
            root.left = None
            root.right = None
            gc.collect()
            valueG, takenG = greedy(sortedItems, capacity)
            print("GREDDY", item_count)
            print(valueG)
            break

        if act.estimate < result.estimate and act.weight < items1[i-1].weight or i == len(items):
            i -= 1

            if act.value > result.value:
                result = act

            while ant.right is not None and ant.father is not None:
                act = ant
                ant = act.father
                i -= 1
            act = act.father

    if root.right is not None and root.left is not None:
        print("BAB", item_count)
        print(result.value)
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


if __name__ == "__main__":
    # Imprime el/los ficheros de la carpeta
    for dirname, _, filenames in os.walk('data'):
        for filename in filenames:
            print(os.path.join(dirname, filename))

    # Abre el primer fichero (debe haber una carpeta llamada "data" en el cual puede poner el fichero que quiere leer)
    # la carpeta data debe estar en el mismo directorio en el cual se encuentra este proyecto
    for dirname, _, filenames in os.walk('data'):
        for filename in filenames:
            items = []
            item_count = 0
            capacity = 0
            bound = 0
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
                    if int(parts[1]) <= capacity and int(parts[0]) > 0:
                        items.append(Item(j - 1, int(parts[0]), int(parts[1])))
                        bound += int(parts[0])
                        j = j + 1
                process(items, capacity)
