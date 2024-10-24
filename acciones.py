# acciones.py

import random
from config import REGIONES_DISPONIBLES

def realizar_accion_jugador(juego, accion, log_func, selected_region=None, unidades_vender=None):
    jugador = juego.jugadores[0]  # Suponiendo que el jugador principal es el primer jugador
    if accion == "plantar":
        if selected_region is not None:
            if jugador.dinero >= selected_region.coste_plantacion:
                if selected_region not in jugador.plantaciones:
                    jugador.plantar(selected_region, log_func)
                    # No es necesario llamar a log_func aquí, ya se registra en jugador.plantar
                else:
                    log_func(f"Ya has plantado en {selected_region.nombre}")
            else:
                log_func(f"No tienes suficiente dinero para plantar en {selected_region.nombre}")
        else:
            log_func("Por favor, selecciona una región válida para plantar.")
    elif accion == "producir":
        if jugador.produccion > 0:
            jugador.producir(log_func)
            # No es necesario llamar a log_func aquí, ya se registra en jugador.producir
        else:
            log_func("No puedes producir porque no tienes café plantado.")
    elif accion == "vender":
        if unidades_vender is not None:
            if jugador.cafe_disponible >= unidades_vender:
                jugador.vender(juego.mercado, log_func, unidades_vender, juego.jugadores)
                # No es necesario llamar a log_func aquí, ya se registra en jugador.vender
            else:
                log_func(f"No tienes suficiente café para vender {unidades_vender} unidades.")
        else:
            log_func("Por favor, ingresa la cantidad de café que deseas vender.")

def jugar_turno_bots(juego, log_func):
    for bot in juego.jugadores[1:]:  # Omitir el primer jugador (humano)
        acciones_posibles = []
        if bot.dinero >= 30:
            acciones_posibles.append("plantar")
        if bot.produccion > 0:
            acciones_posibles.append("producir")
        if bot.cafe_disponible > 0:
            acciones_posibles.append("vender")
        if acciones_posibles:
            accion = random.choice(acciones_posibles)
            if accion == "plantar":
                region = random.choice(REGIONES_DISPONIBLES)
                if bot.dinero >= region.coste_plantacion and region not in bot.plantaciones:
                    bot.plantar(region, log_func)
                    # Eliminamos la llamada adicional a log_func para evitar duplicados
            elif accion == "producir":
                bot.producir(log_func)
                # Eliminamos la llamada adicional a log_func para evitar duplicados
            elif accion == "vender":
                unidades_vender = min(bot.cafe_disponible, 10)  # Los bots venden hasta 10 unidades
                bot.vender(juego.mercado, log_func, unidades_vender, juego.jugadores)
                # Eliminamos la llamada adicional a log_func para evitar duplicados

    # Avanzar al siguiente turno
    juego.turno += 1

    # Verificar si el juego ha alcanzado los 20 turnos
    if juego.turno >= 20:
        juego.estado = 'finalizado'
        log_func("El juego ha terminado.")

    # Actualizar el precio del mercado
    precio_anterior = juego.mercado.precio
    # Asumimos que el precio se ajusta dentro de las funciones de venta
    nuevo_precio = juego.mercado.precio
    if nuevo_precio != precio_anterior:
        log_func(f"El precio del café ha cambiado de {precio_anterior} a {nuevo_precio} dólares por unidad.")

def mostrar_resultados_finales(juego):
    # Ordenar los jugadores por la cantidad de dinero, de mayor a menor
    jugadores_ordenados = sorted(juego.jugadores, key=lambda j: j.dinero, reverse=True)
    ganador = jugadores_ordenados[0]

    # Crear una lista de resultados para mostrar en pantalla
    resultados = []
    resultados.append("Resultados del Juego:")
    for jugador in jugadores_ordenados:
        resultados.append(f"{jugador.nombre}: {jugador.dinero} dólares")
    resultados.append(f"\nGanador: {ganador.nombre} con {ganador.dinero} dólares")

    return resultados
