
# Práctica Introducción a la Planificación de Robots

README de la práctica



## Authors

- [Jaime Mas Santillán](https://www.github.com/TheArmega)




## BFS y Greedy
He deshecho el algoritmo BFS y lo he encapsulado en funciones:

- Función que encapsula el movimiento de un nodo a otro dada la posición a la que nos querermos desplzar:
```python 
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
```
- Función que encapsula el funcionamiento del algoritmo BFS
```python
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
```

- Para la realización de un algoritmo Greedy he utilizado la distancia euclídea (d = √((x2 - x1)² + (y2 - y1)²)):

```python
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
    - atascado: Un indicador de si el agente se encuentra en un mínimo local
      salida.

    Este algoritmo utiliza una estrategia "greedy" para buscar el camino más
    corto hacia el objetivo. Calcula las distancias desde el nodo actual a las
    posibles direcciones (arriba, abajo, derecha y izquierda) y elige la 
    dirección con la distancia más corta al objetivo. Luego, verifica si esa 
    dirección es transitable en el mapa (marcada como '0' o '4') y realiza un 
    movimiento en esa dirección si es posible. El proceso se repite hasta que 
    se alcanza el objetivo o el agente se queda atascado en un mínimo local
    salida.
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
```

## Extras

- Interfaz gráfica para los mapas y el recorrido:
```python
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
```
- Algoritmo A*
```python
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
```
- Nuevo mapa
<img width="354" alt="Screenshot 2023-10-24 at 18 18 23" src="https://github.com/TheArmega/Path-Planning/assets/38068010/7914f513-b22e-4391-88c3-d3ce1832a241">

- YouTube
BFS Map 3
<iframe width="560" height="315" src="https://www.youtube.com/embed/Eo3DOSZbhMQ?si=4bdtifxZV5j5fwxY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

