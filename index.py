import networkx as nx
import random
import py5
import time

# 1. Generación del laberinto
def generar_laberinto(n):
    G = nx.grid_2d_graph(n, n)
    edges = list(G.edges())
    random.shuffle(edges)
    maze = nx.Graph()
    maze.add_edges_from(edges[:n * n - 1])  # Limitar a (n * n - 1) aristas para crear el laberinto
    return maze

# Configuración inicial
n = 5  # Tamaño del laberinto
jugador_pos = (0, 0)  # Posición inicial del jugador
laberinto = generar_laberinto(n)
inicio = (0, 0)
salida = (n - 1, n - 1)
tiempo_inicio = time.time()
tiempo_limite = 30  # Tiempo límite de 30 segundos
juego_ganado = False  # Para controlar cuando se gana el juego

# 2. Configuración de py5
def setup():
    py5.size(400, 400)
    py5.background(255)
    py5.stroke(0)

def draw():
    global juego_ganado
    py5.background(255)
    
    if not juego_ganado:
        dibujar_laberinto(laberinto)
        dibujar_jugador(jugador_pos)
        marcar_salida(salida)
        
        # Verificar si el jugador llegó a la salida
        if jugador_pos == salida:
            juego_ganado = True
            mostrar_mensaje_ganaste()
            
        # Verificar el tiempo límite
        tiempo_actual = time.time()
        if tiempo_actual - tiempo_inicio > tiempo_limite:
            mostrar_solucion()  # Mostrar solución si se vence el tiempo
    else:
        mostrar_mensaje_ganaste()  # Mantener el mensaje de "Ganaste" visible

# 3. Dibujar el laberinto
def dibujar_laberinto(grafo):
    for (nodo1, nodo2) in grafo.edges():
        x1, y1 = nodo1
        x2, y2 = nodo2
        py5.line(x1 * 80 + 40, y1 * 80 + 40, x2 * 80 + 40, y2 * 80 + 40)

# 4. Dibujar la posición del jugador
def dibujar_jugador(pos):
    x, y = pos
    py5.fill(0, 0, 255)
    py5.ellipse(x * 80 + 40, y * 80 + 40, 20, 20)

# 5. Mostrar solución automática cuando se acaba el tiempo
def mostrar_solucion():
    py5.stroke(255, 0, 0)
    camino = nx.shortest_path(laberinto, source=inicio, target=salida)
    for i in range(len(camino) - 1):
        x1, y1 = camino[i]
        x2, y2 = camino[i + 1]
        py5.line(x1 * 80 + 40, y1 * 80 + 40, x2 * 80 + 40, y2 * 80 + 40)

# 6. Movimiento del jugador
def key_pressed():
    global jugador_pos
    x, y = jugador_pos
    if py5.key == py5.CODED:
        if py5.key_code == py5.UP and (x, y - 1) in laberinto.neighbors((x, y)):
            jugador_pos = (x, y - 1)
        elif py5.key_code == py5.DOWN and (x, y + 1) in laberinto.neighbors((x, y)):
            jugador_pos = (x, y + 1)
        elif py5.key_code == py5.LEFT and (x - 1, y) in laberinto.neighbors((x, y)):
            jugador_pos = (x - 1, y)
        elif py5.key_code == py5.RIGHT and (x + 1, y) in laberinto.neighbors((x, y)):
            jugador_pos = (x + 1, y)

# 7. Salida del juego
def marcar_salida(pos):
    x, y = pos
    py5.fill(255, 0, 0)  
    py5.rect(x * 80 + 30, y * 80 + 30, 20, 20)

# 8. Mostrar mensaje de "Ganaste"
def mostrar_mensaje_ganaste():
    py5.fill(0)
    py5.text_size(32)
    py5.text_align(py5.CENTER, py5.CENTER)
    py5.text("¡Ganaste!", py5.width / 2, py5.height / 2)

# Ejecutar el juego
py5.run_sketch()
