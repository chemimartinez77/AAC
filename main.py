#main.py
from config import inicializar_juego
from utilidades import guardar_juego, cargar_juego
from ui import crear_interfaz

if __name__ == "__main__":
    # # Inicializar el juego o cargar una partida guardada
    # if input("¿Deseas cargar una partida guardada? (s/n): ").lower() == "s":
    #     juego = inicializar_juego()
    #     cargar_juego(juego)
    # else:
    #     juego = inicializar_juego()
    
    juego = inicializar_juego()

    # Crear la interfaz gráfica
    crear_interfaz(juego)

    # Guardar el juego al final de cada turno o cuando el jugador lo decida
    guardar_juego(juego)
