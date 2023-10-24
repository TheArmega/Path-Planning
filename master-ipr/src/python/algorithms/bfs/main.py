#! /usr/bin/env python

"""
# Notactión

## Mapa

En mapa original:

* 0: libre
* 1: ocupado (muro/obstáculo)

Vía código incorporamos:

* 2: visitado
* 3: start
* 4: goal

## Nodo

Nós
* -2: parentId del nodo start
* -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

# Específico de implementación Python

* Índices empiezan en 0
* charMap
"""

# # Initial values are hard-coded (A nivel mapa)

######################################################################
#                           IMPORTANTE                               #
#                      CAMBIAR RUTA DEL MAPA                         #
######################################################################

#FILE_NAME = "/usr/local/share/master-ipr/map1/map1.csv" # Linux-style absolute path
#FILE_NAME = "C:\\Users\\USER_NAME\\Downloads\\master-ipr\\map1\\map1.csv" # Windows-style absolute path, note the `\\` and edit `USER_NAME`
#FILE_NAME = "../../../../map1/map1.csv" # Linux-style relative path
#FILE_NAME = "..\\..\\..\\..\\map1\\map1.csv" # Windows-style relative path, note the `\\`
import tempfile
from time import sleep
from matplotlib import pyplot as plt
import csv
import numpy as np

FILE_NAME = "/Users/jaimemas/Desktop/Master/Primer Semestre/Introduccion a la Planificacion de Robots/master-ipr/shrek_map/shrek.csv"
START_X = 0
START_Y = 0
END_X = 1
END_Y = 1

# # Define Node class (A nivel grafo/nodo)

class Node:
    def __init__(self, x, y, myId, parentId):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId))

# # Mapa

# ## Creamos estructura de datos para mapa

charMap = []

# ## Creamos función para volcar estructura de datos para mapa

def dumpMap():
    for line in charMap:
        print(line)

# ## De fichero, llenar estructura de datos de fichero (`to parse`/`parsing``) para mapa
with open(FILE_NAME) as f:
    line = f.readline()
    while line:
        charLine = line.strip().split(',')
        charMap.append(charLine)
        line = f.readline()

# ## A nivel mapa, integramos la info que teníamos de start & end

charMap[START_X][START_Y] = '3' # 3: start
charMap[END_X][END_Y] = '4' # 4: goal

# ## Volcamos mapa por consola

dumpMap()

# # Grafo búsqueda

# ## Creamos el primer nodo
init = Node(START_X, START_Y, 0, -2)
# init.dump() # comprobar que primer nodo bien

# ## `nodes` contendrá los nodos del grafo

nodes = []

# ## Añadimos el primer nodo a `nodes
nodes.append(init)

def move(direction, node, goalParentId):
    """
    Función que mueve la posición actual a una nueva posición en la dirección 
    dada.

    Args:
    - direction: La dirección en la que se va a mover el nodo ('up', 'down', 
    'right' o 'left').
    - node: El nodo actual que se va a mover.
    - goalParentId: El identificador del nodo objetivo al que estamos buscando.

    Returns:
    - Un par de valores booleanos:
        - True si se ha alcanzado el objetivo en la nueva posición.
        - False si no se ha alcanzado el objetivo en la nueva posición.

    Esta función se encarga de mover el nodo actual en una dirección específica
    ('up', 'down', 'right' o 'left'). Calcula las nuevas coordenadas en función
    de la dirección, verifica si la nueva posición contiene un nodo objetivo 
    ('4'), un nodo visitable ('0') o una posición no válida, y realiza las 
    acciones correspondientes. Si se encuentra el nodo objetivo, se marca como 
    "GOALLLL!!!" y se actualiza el identificador del nodo objetivo. Si la nueva
    posición es visitable, se marca como visitada ('2') y se crea un nuevo nodo
    en esa posición. La función devuelve True si se ha alcanzado el objetivo en
    la nueva posición y False en otros casos.
    """

    x, y = 0, 0

    match direction:
        case 'up':
            x = -1
        case 'down':
            x = 1
        case 'right':
            y = 1
        case 'left':
            y = -1

    tmpX = node.x + x
    tmpY = node.y + y

    if (charMap[tmpX][tmpY] == '4'):
            print(direction,": GOALLLL!!!")
            goalParentId = node.myId
            return True, goalParentId
    
    elif (charMap[tmpX][tmpY] == '0'):
            print(direction,": mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)
            return False, goalParentId
    else:
        return False, goalParentId
    
def BFS(done, node, goalParentId):
    """
    Función que realiza el algoritmo BFS (Breadth-First Search).
    Propaga la búsqueda en las cuatro direcciones (arriba, abajo, derecha e 
    izquierda) en secuencia.

    Args:
    - done: Un indicador de si se ha alcanzado el objetivo.
    - node: El nodo actual en el que estamos buscando.
    - goalParentId: El identificador del nodo objetivo al que estamos buscando.

    Returns:
    - done: Un indicador de si se ha alcanzado el objetivo.
    - goalParentId: El identificador del nodo objetivo (puede cambiar si se 
      encuentra un nuevo camino).
    
    Esta función implementa el algoritmo BFS, que realiza una búsqueda por 
    niveles en un grafo. Comienza desde el nodo actual y explora todos los 
    nodos adyacentes en las cuatro direcciones posibles. Si se encuentra un 
    camino hacia el objetivo, se marca como "done" y se devuelve. Se continúa
    buscando en todas las direcciones en secuencia y, si se encuentra un camino
    hacia el objetivo en alguna dirección, se devuelve. El parámetro "done" se 
    utiliza como una variable de control para determinar si se ha alcanzado el 
    objetivo en algún momento durante la búsqueda.
    """

    done, goalParentId = move('up', node, goalParentId)
    if (done): return done, goalParentId
    done, goalParentId = move('down', node, goalParentId)
    if (done): return done, goalParentId
    done, goalParentId = move('right', node, goalParentId)
    if (done): return done, goalParentId
    done, goalParentId = move('left', node, goalParentId)
    
    return done, goalParentId

def greedy(node, goalParentId):
    """
    Función que incorpora un algoritmo greedy.
    Sigue siempre la distancia más corta al objetivo.

    Args:
    - node: El nodo actual en el que estamos buscando.
    - goalParentId: El identificador del nodo objetivo al que estamos buscando.

    Returns:
    - done: Un indicador de si se ha alcanzado el objetivo.
    - goalParentId: El identificador del nodo objetivo (puede cambiar si se 
      encuentra un nuevo camino más corto).
    - atascado: Un indicador de si el agente se encuentra en un mínimo local.

    Este algoritmo utiliza una estrategia "greedy" para buscar el camino más
    corto hacia el objetivo. Calcula las distancias desde el nodo actual a las
    posibles direcciones (arriba, abajo, derecha y izquierda) y elige la 
    dirección con la distancia más corta al objetivo. Luego, verifica si esa 
    dirección es transitable en el mapa (marcada como '0' o '4') y realiza un 
    movimiento en esa dirección si es posible. El proceso se repite hasta que 
    se alcanza el objetivo o el agente se queda atascado en un mínimo local.
    """

    atascado = True # Variable de control para evitar mínimos locales
    done = False    # Variable de control para detectar el objetivo

    # Calcula las distancias a las posibles direcciones
    distances = {
        'up': ((node.x - 1 - END_X) ** 2 + (node.y - END_Y) ** 2) ** 0.5,
        'down': ((node.x + 1 - END_X) ** 2 + (node.y - END_Y) ** 2) ** 0.5,
        'right': ((node.x - END_X) ** 2 + (node.y + 1 - END_Y) ** 2) ** 0.5,
        'left': ((node.x - END_X) ** 2 + (node.y - 1 - END_Y) ** 2) ** 0.5
    }
    
    # Ordena las direcciones en función de las distancias
    sortedPaths = sorted(distances, key=distances.get)

    # Recorre las direcciones ordenadas y realiza movimientos si es posible
    for distance in sortedPaths:
        if (distance == 'up' and (charMap[node.x - 1][node.y] == '0' or charMap[node.x - 1][node.y] == '4')):
            print("UP")
            done, goalParentId = move('up', node, goalParentId)
            atascado = False
            break
        elif (distance == 'down' and (charMap[node.x + 1][node.y] == '0' or charMap[node.x + 1][node.y] == '4')):
            print("DOWN")
            done, goalParentId = move('down', node, goalParentId)
            atascado = False
            break
        elif (distance == 'right' and (charMap[node.x][node.y + 1] == '0' or charMap[node.x][node.y + 1] == '4')):
            print("RIGHT")
            done, goalParentId = move('right', node, goalParentId)
            atascado = False
            break
        elif (distance == 'left' and (charMap[node.x][node.y - 1] == '0' or charMap[node.x][node.y - 1] == '4')):
            print("LEFT")
            done, goalParentId = move('left', node, goalParentId)
            atascado = False  
            break

    return done, goalParentId, atascado
    
def drawMap(done):
    """
    Función que muestra el mapa en una interfaz gráfica.

    Args:
    - done: Un indicador de si se ha alcanzado el objetivo.

    Esta función genera una representación visual del mapa utilizando una 
    biblioteca gráfica (matplotlib) y muestra el estado de cada celda en 
    colores personalizados. Los colores representan diferentes estados, 
    como áreas sin explorar, obstáculos, nodos explorados, inicio, objetivo
    y el camino. Los estados se definen en un mapa de colores personalizado y 
    se asignan a cada celda en el mapa de acuerdo con su valor.

    La función también agrega bordes blancos a las celdas y muestra una leyenda
    que describe los estados representados por los colores. Si se alcanza el 
    objetivo (indicado por el parámetro 'done'), cierra todas las ventanas 
    gráficas.

    Nota: La función utiliza un archivo CSV temporal ('csvAux.csv') para 
    almacenar la información del mapa y cargarlo posteriormente.

    """

    # Creamos un csv temporal donde ir guardando la información que guardábamos en charMap
    tempfile.NamedTemporaryFile(mode='w', suffix='.csv', prefix='csvAux', delete=False)
    b = open('csvAux.csv', 'w')
    a = csv.writer(b)
    # Escribimos cada elemento array de charMap en el CSV
    for line in charMap:
        data = [np.array(line)]
        a.writerows(data)
    b.close()

    plt.ion()

    map_data = np.loadtxt('csvAux.csv', delimiter=',')

    cmap = plt.cm.colors.ListedColormap(['#f7eae5', '#352346', '#d9a0ab', '#61C9A8', '#5DA9E9', 'yellow'])
    bounds = [0, 1, 2, 3, 4, 5, 6]  
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N, clip=True)

    plt.xticks([])
    plt.yticks([])

    plt.imshow(map_data, cmap=cmap, norm=norm)

    # Agrega bordes blancos a las celdas
    for i in range(map_data.shape[0]):
        for j in range(map_data.shape[1]):
            if map_data[i, j] != 1:
                plt.plot([j - 0.5, j + 0.5, j + 0.5, j - 0.5, j - 0.5],
                        [i - 0.5, i - 0.5, i + 0.5, i + 0.5, i - 0.5],
                        color='white', linewidth=1)

    plt.show()

    cb = plt.colorbar(ticks=[0, 1, 2, 3, 4, 5])
    cb.set_ticklabels(['Sin explorar', 'Obstáculo', 'Explorado', 'Inicio', 'Objetivo', 'Camino'])
    cb.set_label('Estados')
    plt.pause(.05)
    plt.clf()

    if (done):
        plt.close('all')

def A_star(node, goalParentId):
    """
    Función que implementa el algoritmo A* para encontrar el camino más corto a
    un objetivo.

    Args:
    - node: El nodo actual en el que estamos buscando.
    - goalParentId: El identificador del nodo objetivo al que estamos buscando.

    Returns:
    - Un par de valores booleanos:
        - True si se ha alcanzado el objetivo.
        - False si no se ha alcanzado el objetivo.

    Esta función utiliza el algoritmo A* para encontrar el camino más corto 
    desde el nodo actual hasta el objetivo. El algoritmo evalúa las direcciones
    'arriba', 'abajo', 'derecha' y 'izquierda' desde el nodo actual, calcula 
    las distancias heurísticas a través de la función de distancia de Manhattan
    y elige la dirección con la distancia más corta. Luego, verifica si esa 
    dirección es transitable en el mapa (marcada como '0' o '4') y realiza un 
    movimiento en esa dirección si es posible. El proceso se repite hasta que 
    se alcanza el objetivo o el agente se queda atascado en un callejón sin 
    salida. La función devuelve True si se ha alcanzado el objetivo y False en
    otros casos.

    El algoritmo A* es una técnica de búsqueda informada que utiliza una 
    combinación de costo real y estimado para seleccionar la próxima dirección 
    a explorar, lo que tiende a encontrar un camino más corto hacia el 
    objetivo.
    """

    atascado = True  # Indica si el agente está atascado
    done = False     # Indica si se ha alcanzado el objetivo

    # Calcula las distancias heurísticas a través de la función de distancia de Manhattan
    distances = {
        'up': (abs(node.x - 1 - END_X) + abs(node.y - END_Y)),
        'down': (abs(node.x + 1 - END_X) + abs(node.y - END_Y)),
        'right': (abs(node.x - END_X) + abs(node.y + 1 - END_Y)),
        'left': (abs(node.x - END_X) + abs(node.y - 1 - END_Y))
    }
    
    sortedPaths = sorted(distances, key=distances.get) # Ordena las direcciones por distancia

    for distance in sortedPaths:
        if (distance == 'up' and (charMap[node.x - 1][node.y] == '0' or charMap[node.x - 1][node.y] == '4')):
            print("UP")
            done, goalParentId = move('up', node, goalParentId)
            atascado = False
            break
        elif (distance == 'down' and (charMap[node.x + 1][node.y] == '0' or charMap[node.x + 1][node.y] == '4')):
            print("DOWN")
            done, goalParentId = move('down', node, goalParentId)
            atascado = False
            break
        elif (distance == 'right' and (charMap[node.x][node.y + 1] == '0' or charMap[node.x][node.y + 1] == '4')):
            print("RIGHT")
            done, goalParentId = move('right', node, goalParentId)
            atascado = False
            break
        elif (distance == 'left' and (charMap[node.x][node.y - 1] == '0' or charMap[node.x][node.y - 1] == '4')):
            print("LEFT")
            done, goalParentId = move('left', node, goalParentId)
            atascado = False  
            break

    return done, goalParentId, atascado

# ## Creamos unna función que te diga si hay un obstáculo
def obstacles(node, goal_x, goal_y):

    direction_to_obstacle = []
    
    if (charMap[node.x][node.y + 1] == '1'): 
        obstacle = True 
        direction_to_obstacle.append('right')
    elif (charMap[node.x][node.y - 1] == '1'): 
        obstacle = True 
        direction_to_obstacle.append('left')
    elif (charMap[node.x + 1][node.y] == '1'): 
        obstacle = True 
        direction_to_obstacle.append('down')
    elif (charMap[node.x - 1][node.y] == '1'): 
        obstacle = True 
        direction_to_obstacle.append('up')
    else:
        return False, "free"
    
    return obstacle, direction_to_obstacle

# ## Creamos un algoritmo de tipo BUG
'''
def bug_algorithm(node, goal_x, goal_y, goalParentId, charMap):

    obstacle = False
    directions = ['up', 'down', 'right', 'left']
    obstacle, direction_to_obstacle = obstacles(node, goal_x, goal_y)

    if(obstacle):
        for direction in directions:
            print("ENTRO")
            node_aux = node

            match direction:
                case 'up':
                    node_aux.x = node_aux.x - 1
                    obstacle_aux, direction_to_obstacle_aux = obstacles(node_aux, goal_x, goal_y)
                    if(obstacle_aux and charMap[node_aux.x][node_aux.y] == '0'):
                        print(node.x, node.y)
                        done, goalParentId = move('up', node, goalParentId)
                        break
                case 'down':
                    node_aux.x = node_aux.x + 1
                    obstacle_aux, direction_to_obstacle_aux = obstacles(node_aux, goal_x, goal_y)
                    if(obstacle_aux and charMap[node.x + 1][node.y] == '0'):
                        done, goalParentId = move('down', node, goalParentId)
                        break
                case 'right':
                    node_aux.y = node_aux.y + 1
                    obstacle_aux, direction_to_obstacle_aux = obstacles(node_aux, goal_x, goal_y)
                    if(obstacle_aux and charMap[node.x][node.y + 1] == '0'):
                        done, goalParentId = move('right', node, goalParentId)
                        break
                case 'left':
                    node_aux.y = node_aux.y - 1
                    obstacle_aux, direction_to_obstacle_aux = obstacles(node_aux, goal_x, goal_y)
                    if(obstacle_aux and charMap[node.x][node.y - 1] == '0'):
                        done, goalParentId = move('left', node, goalParentId)
                        break
    else:
        print("FUERA")
        if (node.x < goal_x):
            done, goalParentId = move('right', node, goalParentId)
        elif (node.x > goal_x):
            done, goalParentId = move('left', node, goalParentId)
        elif (node.y < goal_y):
            done, goalParentId = move('down', node, goalParentId)
        elif (node.y > goal_y):
            done, goalParentId = move('up', node, goalParentId)
            
    #breakpoint()

    return done, goalParentId
'''

# ## Creamos una función que imprime por el camino y cambia el valor de los nodos que pertencen a la solución
def solutionPrint(goalParentId):
    print("%%%%%%%%%%%%%%%%%%%")
    ok = False
    while not ok:
        for node in nodes:
            if( node.myId == goalParentId):
                if (node.myId != 0):
                    charMap[node.x][node.y] = 6
                node.dump()
                goalParentId = node.parentId

                if( goalParentId == -2):
                    print("%%%%%%%%%%%%%%%%%2")
                    ok = True

# ## Empieza algoritmo

done = False  # clásica condición de parada del bucle `while`
goalParentId = -1  # -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto
atascado = False
wall = False
directions = ['up', 'down', 'right', 'left']

visitedNodes = []

path = []

while not done:
    print("--------------------- number of nodes: "+str(len(nodes)))
    for node in nodes:

        directions = ['up', 'down', 'right', 'left']

        # Si el nodo ya ha sido visitado se lo salta
        if (node.myId in visitedNodes):
            continue

        node.dump()

        visitedNodes.append(node.myId)

        #done, goalParentId = BFS(done, node, goalParentId)
        #done, goalParentId, atascado = greedy(node, goalParentId)
        #done, goalParentId = bug_algorithm(node, END_X, END_Y, goalParentId, charMap)
        done, goalParentId, atascado = A_star(node, goalParentId)

        while (atascado):
            nodes.pop()
            visitedNodes.pop()
            nodes[-1].dump()
            done, goalParentId, atascado = greedy(nodes[-1], goalParentId)


        dumpMap()
        drawMap(False)

        if (done):
            solutionPrint(goalParentId)
            drawMap(done)
            sleep(5)
            break