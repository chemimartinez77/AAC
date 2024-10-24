import pygame
import sys
from jugador import Jugador
from mercado import Mercado
from region import Region
from config import REGIONES_DISPONIBLES
from acciones import jugar_turno_bots, realizar_accion_jugador, mostrar_resultados_finales

# Inicializar Pygame
pygame.init()

# Actualizar dimensiones de la ventana
ANCHO = 1000  # Ancho aumentado para incluir el área del log
ALTO = 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("All About Coffee - Pygame")

# Configurar el reloj para controlar los FPS
clock = pygame.time.Clock()

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (34, 177, 76)
AZUL = (63, 72, 204)
ROJO = (237, 28, 36)
GRIS_CLARO = (200, 200, 200)

# Fuente
fuente = pygame.font.SysFont(None, 30)

# Clase Botón
class Boton:
    def __init__(self, x, y, ancho, alto, color, texto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color
        self.texto = texto
        self.fuente = pygame.font.SysFont(None, 30)

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
        superficie_texto = self.fuente.render(self.texto, True, BLANCO)
        text_rect = superficie_texto.get_rect(center=self.rect.center)
        pantalla.blit(superficie_texto, text_rect)

    def es_presionado(self, posicion):
        return self.rect.collidepoint(posicion)

# Función para mostrar texto en pantalla
def mostrar_texto(pantalla, texto, x, y, color=NEGRO, tamano_fuente=30):
    fuente = pygame.font.SysFont(None, tamano_fuente)
    superficie_texto = fuente.render(texto, True, color)
    pantalla.blit(superficie_texto, (x, y))

# Función para mostrar información de los jugadores
def mostrar_informacion_jugadores(pantalla, jugadores, mercado, turno):
    # Definir posiciones iniciales
    x_offset = 50
    y_offset = 20

    # Mostrar turno y precio del café
    mostrar_texto(pantalla, f"Turno: {turno}", x_offset, y_offset)
    y_offset += 30
    mostrar_texto(pantalla, f"Precio del café: {mercado.precio} $/unidad", x_offset, y_offset)
    y_offset += 40

    # Títulos de columnas
    mostrar_texto(pantalla, "Jugador", x_offset, y_offset)
    mostrar_texto(pantalla, "Dinero", x_offset + 150, y_offset)
    mostrar_texto(pantalla, "Producción", x_offset + 250, y_offset)
    mostrar_texto(pantalla, "Café Disponible", x_offset + 400, y_offset)
    y_offset += 25

    # Línea de separación
    pygame.draw.line(pantalla, NEGRO, (x_offset, y_offset), (x_offset + 550, y_offset), 2)
    y_offset += 10

    # Mostrar información de cada jugador
    for jugador in jugadores:
        # Destacar al jugador humano
        if jugador == jugadores[0]:
            color_texto = AZUL  # Color diferente para el jugador humano
        else:
            color_texto = NEGRO

        mostrar_texto(pantalla, jugador.nombre, x_offset, y_offset, color=color_texto)
        mostrar_texto(pantalla, str(jugador.dinero), x_offset + 150, y_offset, color=color_texto)
        mostrar_texto(pantalla, str(jugador.produccion), x_offset + 250, y_offset, color=color_texto)
        mostrar_texto(pantalla, str(jugador.cafe_disponible), x_offset + 400, y_offset, color=color_texto)
        y_offset += 30  # Espacio entre jugadores

# Función para mostrar la selección de región en una ventana emergente
def mostrar_seleccion_region(pantalla, regiones):
    # Crear una superposición semitransparente
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(128)  # Ajusta la transparencia
    overlay.fill((0, 0, 0))  # Color negro
    pantalla.blit(overlay, (0, 0))
    
    # Definir el rectángulo de la ventana emergente
    popup_rect = pygame.Rect(150, 100, 700, 400)
    pygame.draw.rect(pantalla, BLANCO, popup_rect)
    pygame.draw.rect(pantalla, NEGRO, popup_rect, 2)  # Borde negro
    
    # Título de la ventana
    mostrar_texto(pantalla, "Selecciona una región para plantar", popup_rect.x + 20, popup_rect.y + 20, color=NEGRO)
    
    # Dibujar botones de regiones
    botones_regiones = []
    y_offset = popup_rect.y + 60
    for region in regiones:
        boton_region = Boton(popup_rect.x + 50, y_offset, 600, 40, GRIS_CLARO, f"{region.nombre} - Coste: {region.coste_plantacion}")
        boton_region.dibujar(pantalla)
        botones_regiones.append((boton_region, region))
        y_offset += 50
    return botones_regiones

# Función para mostrar logs
logs = []

def agregar_log(mensaje):
    logs.append(mensaje)
    if len(logs) > 15:  # Aumentamos el límite para acomodar más mensajes
        logs.pop(0)

def mostrar_logs(pantalla):
    x_offset = 810  # Comienza después de los 800 píxeles
    y_offset = 20   # Margen superior
    for log in logs:
        mostrar_texto(pantalla, log, x_offset, y_offset, tamano_fuente=16)
        y_offset += 30  # Espacio entre líneas

# Inicializar el juego
def inicializar_juego():
    jugador = Jugador("Chemi")
    bot1 = Jugador("Bot 1")
    bot2 = Jugador("Bot 2")
    mercado = Mercado()
    juego = Juego([jugador, bot1, bot2], mercado)
    return juego

# Clase Juego
class Juego:
    def __init__(self, jugadores, mercado):
        self.jugadores = jugadores
        self.mercado = mercado
        self.turno = 1  # Iniciamos en el turno 1
        self.estado = 'jugando'  # Estados: 'jugando', 'seleccionando_region', 'mostrar_resultados'

# Crear instancias de botones
boton_plantar = Boton(50, 500, 200, 50, VERDE, 'Plantar')
boton_producir = Boton(300, 500, 200, 50, AZUL, 'Producir')
boton_vender = Boton(550, 500, 200, 50, ROJO, 'Vender')

# Inicializar el juego
juego = inicializar_juego()
jugador = juego.jugadores[0]  # El jugador humano
bots = juego.jugadores[1:]    # Los bots

# Variable para controlar si el jugador ya ha actuado en el turno
jugador_ha_actuado = False

# Bucle principal del juego
running = True
botones_regiones = []  # Inicializar lista de botones de regiones

while running:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            posicion_mouse = pygame.mouse.get_pos()

            if juego.estado == 'jugando':
                if boton_plantar.es_presionado(posicion_mouse):
                    juego.estado = 'seleccionando_region'
                elif boton_producir.es_presionado(posicion_mouse):
                    if not jugador_ha_actuado:
                        realizar_accion_jugador(juego, 'producir', agregar_log)
                        jugador_ha_actuado = True
                    else:
                        agregar_log("Ya has realizado una acción en este turno")
                elif boton_vender.es_presionado(posicion_mouse):
                    if not jugador_ha_actuado:
                        # Por simplicidad, venderemos todas las unidades disponibles
                        unidades_vender = jugador.cafe_disponible
                        if unidades_vender > 0:
                            realizar_accion_jugador(juego, 'vender', agregar_log, unidades_vender=unidades_vender)
                            jugador_ha_actuado = True
                        else:
                            agregar_log("No tienes café para vender")
                    else:
                        agregar_log("Ya has realizado una acción en este turno")

            elif juego.estado == 'seleccionando_region':
                # Manejar selección de región
                for boton, region in botones_regiones:
                    if boton.es_presionado(posicion_mouse):
                        if not jugador_ha_actuado:
                            realizar_accion_jugador(juego, 'plantar', agregar_log, selected_region=region)
                            jugador_ha_actuado = True
                            juego.estado = 'jugando'
                        else:
                            agregar_log("Ya has realizado una acción en este turno")
                # Si se hace clic fuera de la ventana emergente, volver al estado 'jugando'
                if not pygame.Rect(150, 100, 700, 400).collidepoint(posicion_mouse):
                    juego.estado = 'jugando'

        # Manejar clic en el botón salir en el estado 'mostrar_resultados'
        if juego.estado == 'mostrar_resultados':
            if event.type == pygame.MOUSEBUTTONDOWN:
                posicion_mouse = pygame.mouse.get_pos()
                if boton_salir.es_presionado(posicion_mouse):
                    running = False

    # Actualizar lógica del juego
    if jugador_ha_actuado:
        jugar_turno_bots(juego, agregar_log)
        jugador_ha_actuado = False

        # Verificar si el juego ha terminado
        if juego.turno > 20:
            resultados = mostrar_resultados_finales(juego)
            juego.estado = 'mostrar_resultados'

    # Dibujar en la pantalla
    screen.fill(BLANCO)

    if juego.estado == 'jugando':
        # Mostrar información de todos los jugadores
        mostrar_informacion_jugadores(screen, juego.jugadores, juego.mercado, juego.turno)
        # Dibujar botones de acciones
        boton_plantar.dibujar(screen)
        boton_producir.dibujar(screen)
        boton_vender.dibujar(screen)
    elif juego.estado == 'seleccionando_region':
        # Mostrar información de todos los jugadores
        mostrar_informacion_jugadores(screen, juego.jugadores, juego.mercado, juego.turno)
        # Dibujar la ventana de selección de región
        botones_regiones = mostrar_seleccion_region(screen, REGIONES_DISPONIBLES)
    elif juego.estado == 'mostrar_resultados':
        # Mostrar los resultados finales
        y_offset = 150
        for linea in resultados:
            mostrar_texto(screen, linea, 50, y_offset, color=NEGRO)
            y_offset += 40

        # Botón para salir del juego o reiniciar
        boton_salir = Boton(400, y_offset + 50, 200, 50, ROJO, 'Salir')
        boton_salir.dibujar(screen)

    # Dibujar el fondo del área del log y mostrar los logs
    pygame.draw.rect(screen, (230, 230, 230), (800, 0, 200, ALTO))
    mostrar_logs(screen)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del bucle
    clock.tick(60)

# Salir de Pygame
pygame.quit()
sys.exit()
