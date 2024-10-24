#utilidades.py
import json
from region import Region

def actualizar_tabla(tree, jugadores):
    """
    Actualiza la tabla de la interfaz con la información de los jugadores.
    """
    # Limpiar el contenido existente en la tabla
    for item in tree.get_children():
        tree.delete(item)

    # Insertar la información actualizada de los jugadores
    for jugador in jugadores:
        tree.insert("", "end", values=(
            jugador.nombre, 
            jugador.dinero, 
            jugador.produccion, 
            jugador.cafe_disponible, 
            jugador.puntos
        ))

def guardar_juego(juego, archivo="partida_guardada.json"):
    """Guarda el estado actual del juego en un archivo JSON."""
    estado_juego = {
        "jugadores": [
            {
                "nombre": jugador.nombre,
                "dinero": jugador.dinero,
                "plantaciones": [(region.nombre, region.coste_plantacion, region.produccion_por_turno) for region in jugador.plantaciones],
                "produccion": jugador.produccion,
                "cafe_disponible": jugador.cafe_disponible,
                "puntos": jugador.puntos
            } for jugador in juego.jugadores
        ],
        "mercado": {"precio": juego.mercado.precio},
        "turno": juego.turno
    }

    with open(archivo, "w") as f:
        json.dump(estado_juego, f)
    print(f"Juego guardado en {archivo}")

def cargar_juego(juego, archivo="partida_guardada.json"):
    """Carga el estado del juego desde un archivo JSON."""
    with open(archivo, "r") as f:
        estado_juego = json.load(f)

    # Restaurar jugadores
    for i, jugador_data in enumerate(estado_juego["jugadores"]):
        jugador = juego.jugadores[i]
        jugador.nombre = jugador_data["nombre"]
        jugador.dinero = jugador_data["dinero"]
        jugador.plantaciones = [
            Region(nombre, coste, produccion) for nombre, coste, produccion in jugador_data["plantaciones"]
        ]
        jugador.produccion = jugador_data["produccion"]
        jugador.cafe_disponible = jugador_data["cafe_disponible"]
        jugador.puntos = jugador_data["puntos"]

    # Restaurar mercado y turno
    juego.mercado.precio = estado_juego["mercado"]["precio"]
    juego.turno = estado_juego["turno"]
    print(f"Juego cargado desde {archivo}")
