"""
Modelacion y Simulacion
Proyecto Final

Simulacion de transito en una grilla con incorporacion de algoritmo genetico 
para la determinacion de la mejor configuracion para los semaforos

Autores:
- Maria Jose Gil Herrera
- Roberto Francisco Rios Morales
"""


import random
import numpy as np
import prettytable


def defineStreet(n, stMap):
    """
    genera una grilla de tamano n
    """
    stMap[0][0] = 2
    stMap[0][len(stMap)-1] = 2
    stMap[len(stMap)-1][0] = 2
    stMap[len(stMap)-1][len(stMap)-1] = 2

    for a in range(1, len(stMap[n])):
        h = random.random()
        if stMap[n][a-1] == 0:
            stMap[n][a] = 2
            stMap[a][n] = 2
        elif stMap[n][a-1] == 2:
            if h < 0.2:
                stMap[n][a] = 2
                stMap[a][n] = 2

    return stMap



def trafficLight(stMap):
    """
    coloca semaforos en una grilla generada
    """
    stMap = stMap.tolist()
    for a in range(1, len(stMap)-1):
        for i in range(1, len(stMap[0])-1):
            if ((stMap[a-1][i] == 0 and stMap[a+1][i] == 0 and stMap[a][i-1]==0 and stMap[a][i+1]==0) or (stMap[a-1][i] == 0 and stMap[a+1][i] == 0 and stMap[a][i-1]==0) or (stMap[a+1][i] == 0 and stMap[a][i-1]==0 and stMap[a][i+1]==0) or (stMap[a-1][i] == 0 and stMap[a+1][i] == 0 and stMap[a][i+1]==0) or (stMap[a-1][i] == 0 and stMap[a][i-1]==0 and stMap[a][i+1]==0)) and stMap[a][i]== 0:
                stMap[a][i] = (random.randint(0,10), random.randint(0,10))

    return stMap


def gengrid():
    """
    genera una grilla predefinida con los semaforos ya colocados
    """
    stgrid = [
        [2, 2, 0, 2, 2, 2, 0, 2, 2, 2], 
        [2, 2, 0, 2, 2, 2, 0, 2, 2, 2], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [2, 2, 0, 2, 0, 2, 0, 2, 2, 2], 
        [2, 2, 0, 2, 0, 2, 0, 2, 2, 2], 
        [2, 2, 0, 2, 0, 2, 0, 2, 2, 2], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [2, 2, 0, 2, 0, 2, 0, 2, 2, 2], 
        [2, 2, 0, 2, 0, 2, 0, 2, 2, 2]
    ]

    return trafficLight(np.array(stgrid))



def spawncars(grid):
    """
    genera una cantidad aleatoria de carros en los ingresos a la grilla, 
    es decir, las primeras y ultimas filas y columnas
    """
    # generar carros arriba
    for i in range(1, len(grid) - 1):
        # se genera con una probabilidad del 0.5, en la columna superior, si es que hay via
        if random.random() > 0.5 and grid[0][i] == 0 and i % 2 == 0:
            grid[0][i] = 1

    # generar carros izquierda
    for i in range(1, len(grid) - 1):
        # se genera con una probabilidad del 0.5, en la columna exterior izquierda, si es que hay via
        if random.random() > 0.5 and grid[i][0] == 0 and i % 2 == 0:
            grid[i][0] = 1
    
    # generar carros abajo
    for i in range(1, len(grid) - 1):
        # se genera con una probabilidad del 0.5, en la fila inferior, si es que hay via
        if random.random() > 0.5 and grid[-1][i] == 0 and i % 2 != 0:
            grid[-1][i] = 1
    
    # generar carros derecha
    for i in range(1, len(grid) - 1):
        # se genera con una probabilidad del 0.5, en la columna exterior derecha, si es que hay via
        if random.random() > 0.5 and grid[i][-1] == 0 and i % 2 != 0:
            grid[i][-1] = 1
    
    return grid



def genpaths(grid):
    """
    organiza en un diccionario los paths que se le deben 
    asignar a cada carro que se va a simular
    """
    paths = {}
    # se itera en cada carro que entra para asignarle un 
    # camino predefinido a seguir a traves del grid
    # carros de arriba
    for i in range(1, len(grid) - 1):
        if grid[0][i] == 1:
            paths[(0,i)] = []

    # carros izquierda
    for i in range(1, len(grid) - 1):
        if grid[i][0] == 1:
            paths[(i,0)] = []
    
    # carros abajo
    for i in range(1, len(grid) - 1):
        if grid[-1][i] == 1:
            paths[(len(grid) - 1,i)] = []
    
    # carros derecha
    for i in range(1, len(grid) - 1):
        if grid[i][-1] == 1:
            paths[(i,len(grid) - 1)] = []

    return paths



def add_semaphore_wait(semaphore:list[int], semaphorepos:tuple[int], lastpos:tuple[int]):
    """
    suma el tiempo perdido en esperar semaforos para cada carro que se tope con uno
    """
    # ver de que lado hace esperar el semaforo 
    # retornar la posicion en la que esta el carro la cantidad de veces que indica el semaforo
    if semaphorepos[0] == lastpos[0]: # si hace esperar filas
        return [lastpos for _ in range(semaphore[0])] 
    else: # si hace esperar columnas
        return [lastpos for _ in range(semaphore[1])]


def simulatepaths(paths, grid):
    """
    esta funcion simula el movimiento de los carros como tal 
    a traves del grid, tomando en cuenta que deben esperar 
    en los semaforos el tiempo indicado en los mismos
    """
    # asignar el camino a su destino para salir de la grilla a cada carro
    for k,v in paths.items():
        # si empieza arriba deberia terminar en los lados o abajo
        if k[0] == 0:
            x, y = k[0], k[1] # x es fila, ye es columna
            while (y != 0) or (y != len(grid) - 1) or (x != len(grid) - 1):
                # revisar que no haya pared para avanzar
                try:
                    if grid[x+1][y] == 0:
                        x += 1
                        v.append((x,y))
                    # revisar si se llego a un semaforo, se tiene la opcion de seguir recto o cruzar si es que se puede
                    elif type(grid[x+1][y]) is tuple:
                        v.extend(add_semaphore_wait(grid[x+1][y],(x+1,y),(x,y)))
                        # si se puede seguir hacia abajo, se sigue recto
                        if grid[x+2][y] == 0:
                            x += 1
                            v.append((x,y))
                            x += 1
                            v.append((x,y))
                        # si no se puede entonces se ve hacia que lado cruzar
                        else:
                            # si se puede cruzar a la derecha
                            if grid[x+1][y+1] == 0:
                                x += 1
                                v.append((x,y))
                                y += 1
                                v.append((x,y))
                            # si se puede cruzar a la izquierda
                            elif grid[x+1][y-1] == 0:
                                x += 1
                                v.append((x,y))
                                y -= 1
                                v.append((x,y))
                    # hay pared y no se puede avanzar recto
                    else:
                        # si se puede cruzar a la derecha:
                        if grid[x][y+1] == 0:
                            y += 1
                            v.append((x,y))
                        elif grid[x][y-1] == 0:
                            y += 1
                            v.append((x,y))
                except IndexError as ie:
                    print(f"{ie}, el carro salio del grid")
                    break

        # si empieza abajo deberia terminar en los lados o arriba
        elif k[0] == len(grid) - 1:
            x, y = k[0], k[1] # x is row, y is column
            while (y != 0) or (y != len(grid) - 1) or (x != 0):
                # revisar que no haya pared para avanzar
                try:
                    if grid[x-1][y] == 0:
                        x += 1
                        v.append((x,y))
                    # revisar si se llego a un semaforo, se tiene la opcion de seguir recto o cruzar si es que se puede
                    elif type(grid[x-1][y]) is tuple:
                        v.extend(add_semaphore_wait(grid[x-1][y],(x-1,y),(x,y)))
                        # si se puede seguir hacia abajo, se sigue recto
                        if grid[x+2][y] == 0:
                            x += 1
                            v.append((x,y))
                            x += 1
                            v.append((x,y))
                        # si no se puede entonces se ve hacia que lado cruzar
                        else:
                            # si se puede cruzar a la derecha
                            if grid[x-1][y+1] == 0:
                                x -= 1
                                v.append((x,y))
                                y += 1
                                v.append((x,y))
                            # si se puede cruzar a la izquierda
                            elif grid[x-1][y-1] == 0:
                                x -= 1
                                v.append((x,y))
                                y -= 1
                                v.append((x,y))
                    # hay pared y no se puede avanzar recto
                    else:
                        # si se puede cruzar a la derecha:
                        if grid[x][y+1] == 0:
                            y += 1
                            v.append((x,y))
                        elif grid[x][y-1] == 0:
                            y += 1
                            v.append((x,y))
                except IndexError as ie:
                    print(f"{ie}, el carro salio del grid")
                    break

        # si empieza derecha deberia terminar arriba, abajo o izquierda
        elif k[1] == 0:
            x, y = k[0], k[1] # x is row, y is column
            while (y != len(grid) - 1) or (x != len(grid) - 1) or (x != 0):
                try:
                    # check if there's no wall to move forward
                    if grid[x][y+1] == 0:
                        y += 1
                        v.append((x,y))
                    # check if there's a semaphore, you have the option to go straight or cross if possible
                    elif type(grid[x][y+1]) is tuple:
                        v.extend(add_semaphore_wait(grid[x][y+1],(x,y+1),(x,y)))
                        # if you can continue to the right, go straight
                        if grid[x][y+2] == 0:
                            y += 1
                            v.append((x,y))
                            y += 1
                            v.append((x,y))
                        # if not, then look to which side to cross
                        else:
                            # if you can cross upwards
                            if grid[x-1][y+1] == 0:
                                y += 1
                                v.append((x,y))
                                x -= 1
                                v.append((x,y))
                            # if you can cross downwards
                            elif grid[x+1][y+1] == 0:
                                y += 1
                                v.append((x,y))
                                x += 1
                                v.append((x,y))
                    # there's a wall and you can't move forward
                    else:
                        # if you can cross upwards
                        if grid[x-1][y] == 0:
                            x -= 1
                            v.append((x,y))
                        # if you can cross downwards
                        elif grid[x+1][y] == 0:
                            x += 1
                            v.append((x,y))
                        else:
                            break
                except IndexError as ie:
                    print(f"{ie}, el carro salio del grid")
                    break

        # # if the car starts from the left and should go right
        elif k[1] == len(grid)-1:
            x, y = k[0], k[1] # x is row, y is column
            while (y > 0) or (x != len(grid) - 1) or (x != 0):
                # condicion extra ya que python acepta indices negativos
                if y > 0:
                    try:
                        # check if there's no wall to move forward
                        if grid[x][y-1] == 0:
                            y -= 1
                            v.append((x,y))
                        # check if there's a semaphore, you have the option to go straight or cross if possible
                        elif type(grid[x][y-1]) is tuple:
                            v.extend(add_semaphore_wait(grid[x][y-1],(x,y-1),(x,y)))
                            # if you can continue to the left, go straight
                            if grid[x][y-2] == 0:
                                y -= 1
                                v.append((x,y))
                                y -= 1
                                v.append((x,y))
                            # if not, then look to which side to cross
                            else:
                                # if you can cross upwards
                                if grid[x-1][y-1] == 0:
                                    y -= 1
                                    v.append((x,y))
                                    x -= 1
                                    v.append((x,y))
                                # if you can cross downwards
                                elif grid[x+1][y-1] == 0:
                                    y -= 1
                                    v.append((x,y))
                                    x += 1
                                    v.append((x,y))
                        # there's a wall and you can't move forward
                        else:
                            # if you can cross upwards
                            if grid[x-1][y] == 0:
                                x -= 1
                                v.append((x,y))
                            # if you can cross downwards
                            elif grid[x+1][y] == 0:
                                x += 1
                                v.append((x,y))
                            else:
                                break
                    except IndexError as ie:
                        print(f"{ie}, el carro salio del grid")
                        break
                else:
                    print(f"el carro salio del grid")        
                    break
    return paths



def getcountsemaphores(grid):
    """
    esta funcion solo es para obtener la cantidad de semaforos
    que hay en un grid
    """
    count = 0
    for i in range(1, len(grid) - 1):
        for j in range(len(grid[i]) -1):
            if type(grid[i][j]) is tuple:
                count += 1
    return count



def fitness(childpath:dict, childgrid):
    """
    Aptitud: minimiza la cantidad de iteraciones que cada 
    carro debe dar para llegar a su destino
    """
    score = 0
    # iterar el grid en busca de los semaforos
    for row in range(1, len(childgrid) - 1):
        for cell in range(len(childgrid[row]) -1):
            # si encontramos un semaforo
            if type(childgrid[row][cell]) is tuple:
                # rowtime,celltime = cell[0],cell[1]
                # iterar los paths de cada carro para encontrar su relacion con los semaforos
                for k,v in childpath.items():
                    if len(v) > 20:
                        score += 1
                    elif len(v) in range(15,20):
                        score += 3
                    elif len(v) in range(10, 15):
                        score += 5
                    elif len(v) in range(5, 10):
                        score += 8
    return score



def mutate(childgrid):
    """
    otorga una probabilidad del 10% de mejora a cada hijo
    """
    # iterar el grid en busca de los semaforos
    for row in range(1, len(childgrid) - 1):
        for cell in range(1, len(childgrid) - 1):
            # si encontramos un semaforo tenemos probabilidad de mutar su tiempo
            if type(cell) is tuple:
                if random.random < 0.1:
                    childgrid[row][cell] -= 1
    
    return childgrid



def crossover(grid1:list[int], grid2:list[int], childgrid):
    """
    cruza a dos padres para obtener un hijo con 50 50 de probabilidades
    de obtener las caracteristicas de uno o el otro
    """
    # iterar el grid en busca de los semaforos
    for row in range(1, len(childgrid) - 1):
        for cell in range(len(childgrid[row]) -1):
            # si encontramos un semaforo tenemos probabilidad de mutar su tiempo
            if type(cell) is tuple:
                if random.random() <= 0.5:
                    childgrid[row][cell] = grid1[row][cell]
                else:
                    childgrid[row][cell] = grid2[row][cell]

    return childgrid



def select(population):
    """
    selecciona en base al mejor score dado por el fitness 
    a los mejores candidatos para la siguiente generacion
    """
    tested = []
    best_childs = []
    
    for i in population:
        tested.append((i, fitness(i[1], i[0]))) 
    
    sorted_population = sorted(tested, key=lambda x: x[1], reverse=True)[:5]
    
    for i in sorted_population:
        # Append the corresponding element from the population to best_childs
        best_childs.append(i[0])
    
    return best_childs


def gridtostr(best:list[list]):
    # Create a PrettyTable object
    table = prettytable.PrettyTable()

    # Add rows to the table
    for row in best:
        table.add_row(row)

    # Convert the table to a string and return
    table.header = False
    return table.get_string()
    


def main():
    """
    Implementacion de la simulacion y la ejecucion del algoritmo genetico.

    La visualizacion seria ineficiente por medio de consola, 
    por lo tanto se pueden ver en el archivo "results.txt".
    """

    # gengrid 1
    # spawncars 2
    # genpaths 3
    # simulatepaths 4


    # Configuracion inicial
    POPULATION = 5
    GENERATIONS = 500
    CROSSOVER_RATE = 0.4
    MUTATION_RATE = 0.2


    emptygrids = [gengrid() for _ in range(POPULATION)] # hacer population de 5 grids
    grids = list(map(spawncars, emptygrids))
    paths = list(map(lambda x: genpaths(x), grids))
    computed_paths = [simulatepaths(path,grid) for path,grid in zip(paths,grids)]
    population = [(grid,path) for grid,path in zip(grids, computed_paths)]
    
    best_fitness = 0
    best_chromosome = ""
    file = open("result.txt", "w", encoding="utf-8")
    
    file.write(f"\nPoblacion inicial: \n{population}\n")
    file.write(f"\nTamano de cada poblacion: {POPULATION}.")
    file.write(f"\nCantidad de generaciones: {GENERATIONS}.")
    file.write(f"\nTasa de reproduccion: {CROSSOVER_RATE}.")
    file.write(f"\nTasa de mutacion: {MUTATION_RATE}.")
    
    for gen in range(GENERATIONS):
        selected_population = select(population)
        
        children = []
        while len(children) < POPULATION:
            parent1 = random.choice(selected_population)
            parent2 = random.choice(selected_population)
            child = crossover(parent1, parent2, gengrid())
            children.append(child)
        
        # causar mutaciones en cada generacion y hacer que corran mas carros
        for i in range(len(children)):
            children[i] = mutate(children[i])
        
        for i in range(len(children)):
            # correr nuevamente la simulacion de carros pasando por la grilla
            child = spawncars(child)
            paths = genpaths(child)
            new_computed_paths = simulatepaths(paths, child)
            children[i] = (child, new_computed_paths)

            child_fitness = fitness(new_computed_paths, child)
            if child_fitness > best_fitness:
                best_fitness = child_fitness
                best_chromosome = child
        
        population = children

        # visualizacion de resultados
        file.write(f"\nGen: {gen} ")
        file.write(f"Mejor cromosoma: \n{gridtostr(best_chromosome)}\n")
        file.write(f"Mejor fitness score: {best_fitness} \n")
        
    file.close()

main()