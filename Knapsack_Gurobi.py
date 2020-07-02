from collections import namedtuple
from gurobipy import *
from IPython.display import FileLink
import csv

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
            value += item.value+0.5
    if weight > capacity:
        print("solución incorrecta, se supera la capacidad de la mochila (capacity, weight):", capacity, weight)
        return 0
    return int(value)


def auxiliar(sortedItems, capacityI):
    taken = [0]*len(sortedItems)

    indices = [x[0] for x in sortedItems]
    valores = [x[1] for x in sortedItems]
    pesos = [x[2] for x in sortedItems]

    valoresDict = dict(zip(indices, valores))
    pesosDict = dict(zip(indices, pesos))

    m = Model("mochila")

    x1 = m.addVars(indices, vtype=GRB.BINARY, name="x")

    m.addConstr(x1.prod(pesosDict) <= capacityI)

    m.setObjective(x1.prod(valoresDict), GRB.MAXIMIZE)

    m.setParam(GRB.Param.PoolSolutions, 2048)
    m.setParam(GRB.Param.PoolGap, 0.01)
    m.setParam(GRB.Param.PoolSearchMode, 1)
    m.setParam(GRB.Param.TimeLimit, 10.0)

    m.optimize()

    for e in indices:
        if x1[e].x > 0.9:
            taken[e] = 1

    return taken


def process(sortedItems, capacityI):

    sortedItems.sort(key=lambda x: x.value/x.weight)

    taken = auxiliar(sortedItems, capacityI)

    maximo = check_solution(capacityI, sortedItems, taken)

    if maximo == 0:
        exit(1)

    # prepare the solution in the specified output format
    output_data = '%.2f' % maximo + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))

    return output_data, maximo


if __name__ == "__main__":
    # Imprime el/los ficheros de la carpeta
    for dirname, _, filenames in os.walk('data'):
        for filename in filenames:
            print(os.path.join(dirname, filename))
    str_output = [["Filename", "Max_value"]]
    # Abre el primer fichero (debe haber una carpeta llamada "data" en el cual puede poner el fichero que quiere leer)
    # la carpeta data debe estar en el mismo directorio en el cual se encuentra este proyecto
    for dirname, _, filenames in os.walk('data'):
        for filename in filenames:
            items = []
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
                        items.append(Item(j - 1, int(parts[0])-0.5, int(parts[1])))
                        j = j + 1
                output, value = process(items, capacity)
                print(filename, "-------------", value, "----------------")
                str_output.append([filename, str(value)])

    submission_generation('MOCHILA.csv', str_output)
