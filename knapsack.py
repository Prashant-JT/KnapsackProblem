import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import time
import gc
import os
import csv
from collections import namedtuple
from IPython.display import FileLink

Item = namedtuple("Item", ['index', 'value', 'weight'])

def submission_generation(filename, str_output):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for item in str_output:
            writer.writerow(item)
    return FileLink(filename)

def check_solution(capacity, items, taken):
    weight = 0
    value = 0
    for item in items:
        if taken[item.index] == 1:
            weight += item.weight
            value += item.value
    if weight > capacity:
        print("solución incorrecta, se supera la capacidad de la mochila (capacity, weight):", capacity, weight)
        return 0
    return value

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


def solve_it(input_data):
    """"
    The program first tries to run with Branch and Bound, if it is not posible
    or takes a lot of time, it changes to a greedy algorithm
    """

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    """"
    Created a list to only add the items 
    which are less or equal in weight than the total capacity of the knapsack
    """
    items = []
    j = 1
    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        if int(parts[1]) <= capacity and int(parts[0]) > 0:
            items.append(Item(j - 1, int(parts[0]), int(parts[1])))
            j = j + 1

    def values(it):
        return it.value

    def weights(it):
        return it.weight

    def valuesWeight(it):
        return it.value / it.weight

    item_count = len(items)
    sortedItems = items.copy()
    sortedItems.sort(reverse=True, key=valuesWeight)

    """
        Created two same lists as "items", one list is sorted by decreasing values, 
        other by decreasing value/weight and other by increasing weights
        Created to new knapsacks and taken list for the new lists created before

        Greedy algorithm
        1. Start from the first item of all three lists (they are iterated simultaneously)
        2. If the weight of the item is lower or equal than the current capacity, the item is taken,
        the weight is subtracted from the capacity of the respected knapsack and the value of the item taken 
        is added to the current value of the knapsack (is done for each sorted list)
        3. Once all of the respected 3 knapsacks cannot be filled by any more items
           we choose the knapsack with the maximum value and delete the other lists
        4. Return the profit and the respected taken list
        """

    def greedy():
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

        """
            Branch and Bound algorithm
            1. Calculte factionary bound and create a dummy node with value = 0, room = capacity and bound calculated
            2. While the tree has not reached to a leaf node, insert the items than not exceed the capacity (like a greedy)
            3. Store the leaf node and start backtracking comparing the value of the leaf node with the estimate
            4. If a leaf node with a better node value is found, it is replaced by the stored leaf node in 3.
            5. Explore the right side of the node for a better solution
            Exceptions: if the algorithm takes more than 30 seconds or any exception ocurrs
            the algorithm is changed to a greedy
            """

    def brABound():
        takenB = [0] * len(sortedItems)
        estimate = 0
        weights = 0

        for x in sortedItems:
            if weights + x.weight <= capacity:
                estimate += x.value
                weights += x.weight
            else:
                res = capacity - weights
                estimate += (res * x.value) / x.weight
                break
        root = Node(None, 0, capacity, estimate)
        act = root
        i = 0
        result = Node(None, 0, 0, 0)

        start = time.time()
        while root.right is None or act.father is not None:
            if act.left is None and act.weight - sortedItems[i].weight >= 0:
                act.insert(act.value + sortedItems[i].value, act.weight - sortedItems[i].weight, act.estimate)
                ant = act
                act = act.left
            else:
                act.insert(act.value, act.weight, act.estimate - sortedItems[i].value)
                ant = act
                act = ant.right
            i += 1
            end = time.time()

            if end - start >= 15:
                root.right = None
                root.left = None
                gc.collect()
                return greedy()

            if act.value > result.value:
                result = act

            if i == len(items) or ant.estimate > result.estimate:
                i -= 1

                while ant.right is not None and ant.father is not None:
                    act = ant
                    ant = act.father
                    i -= 1
                act = act.father

        def searchNode(resultado, anterior):
            valor = resultado.value - anterior.value
            peso = anterior.weight - resultado.weight

            if valor != 0 and peso != 0:
                for it in sortedItems:
                    if peso == it.weight and valor == it.value:
                        return it.index

        # Taken of BAB
        res = result.value
        aux = result.father
        while aux is not None:
            if result is not None and result.value > aux.value:
                ind = searchNode(result, aux)
                takenB[ind] = 1
            result = result.father
            aux = aux.father
        return res, takenB

    value, taken = brABound()

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data, check_solution(capacity, sortedItems, taken)

if __name__ == '__main__':
    for dirname, _, filenames in os.walk('data'):
        for filename in filenames:
            print(os.path.join(dirname, filename))
    str_output = [["Filename", "Max_value"]]
    for dirname, _, filenames in os.walk('data'):
        for filename in filenames:
            full_name = dirname + '/' + filename
            with open(full_name, 'r') as input_data_file:
                input_data = input_data_file.read()
                output, value = solve_it(input_data)
                str_output.append([filename, str(value)])
    submission_generation('greedy&BB.csv', str_output)
