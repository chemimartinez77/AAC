#config.py
from region import Region
from jugador import Jugador
from mercado import Mercado

# List of available regions with example values
REGIONES_DISPONIBLES = [
    Region("Colombia", 30, 5),
    Region("Brasil", 40, 7),
    Region("Bolivia", 25, 4),
    Region("México", 35, 6)
]

# Definición de la clase Juego
class Juego:
    def __init__(self, jugadores, mercado):
        self.jugadores = jugadores
        self.mercado = mercado
        self.turno = 0

# Función para inicializar el juego
def inicializar_juego():
    """Inicializa el juego con los jugadores y el mercado."""
    jugador1 = Jugador("Chemi")
    bot1 = Jugador("Bot 1")
    bot2 = Jugador("Bot 2")
    mercado = Mercado()

    # Inicializamos el juego con 3 jugadores y el mercado
    juego = Juego([jugador1, bot1, bot2], mercado)

    return juego
