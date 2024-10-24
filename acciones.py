# acciones.py
import tkinter as tk
from tkinter import messagebox
from config import REGIONES_DISPONIBLES
from utilidades import actualizar_tabla

def realizar_accion(juego, tree, accion, selected_region, log_func=None, unidades_vender=None):
    jugador = juego.jugadores[0]  # Suponiendo que el jugador 1 es el jugador principal
    if accion == "plantar":
        if selected_region is not None and jugador.dinero >= selected_region.coste_plantacion:
            jugador.plantar(selected_region, log_func)
        else:
            messagebox.showerror("Error", f"No tienes suficiente dinero para plantar en {selected_region.nombre}" if jugador.dinero < selected_region.coste_plantacion else "Por favor selecciona una región válida para plantar.")
    elif accion == "producir":
        if jugador.produccion > 0:
            jugador.producir(log_func)
        else:
            messagebox.showerror("Acción no válida", "No puedes producir porque no tienes café plantado.")
    elif accion == "vender":
        if unidades_vender is not None and jugador.cafe_disponible >= unidades_vender:
            # Pasamos la lista de jugadores también
            jugador.vender(juego.mercado, log_func, unidades_vender, juego.jugadores)
        else:
            messagebox.showerror("Acción no válida", "No tienes suficiente café para vender.")

    actualizar_tabla(tree, juego.jugadores)

def jugar_turno(juego, tree, log_text, price_label, log_func, btn_turno, jugador_ha_actuado):
    # Verificar si el juego ha alcanzado los 20 turnos
    if juego.turno >= 20:
        mostrar_resultados_finales(juego)
        return  # Salir de la función si el juego ha terminado

    # Registrar el precio anterior antes de la fluctuación
    precio_anterior = juego.mercado.precio

    # Permitir que los bots realicen sus acciones (considerando las condiciones)
    for jugador in juego.jugadores[1:]:  # Omitir el primer jugador (humano)
        import random
        acciones_posibles = ["plantar"]
        if jugador.cafe_disponible > 0:  # Agregar "vender" solo si el bot tiene café para vender
            acciones_posibles.append("vender")
        if jugador.produccion > 0:
            acciones_posibles.append("producir")
        accion = random.choice(acciones_posibles)

        if accion == "plantar" and jugador.dinero >= 30:
            region = random.choice(REGIONES_DISPONIBLES)
            jugador.plantar(region, log_func)
        elif accion == "producir":
            jugador.producir(log_func)
        elif accion == "vender":
            # Pasar la lista de jugadores al vender, igual que para el jugador principal
            jugador.vender(juego.mercado, log_func, 10, juego.jugadores)  # Asumiendo que los bots venden 10 unidades

    # Avanzar al siguiente turno en el juego
    juego.turno += 1

    # Actualizar la etiqueta del precio y registrar el cambio en el precio
    nuevo_precio = juego.mercado.precio
    price_label.config(text=f"Precio del café: {nuevo_precio} dólares por unidad")
    log_func("end", f"El precio del café ha cambiado de {precio_anterior} a {nuevo_precio} dólares por unidad\n")

    # Actualizar la tabla con el nuevo estado del juego
    actualizar_tabla(tree, juego.jugadores)

    # Deshabilitar el botón "Siguiente Turno"
    btn_turno.config(state="disabled")
    # Restablecer el estado de "jugador_ha_actuado" para el siguiente turno
    jugador_ha_actuado.set(False)

    # Verificar nuevamente si el juego ha alcanzado los 20 turnos para mostrar los resultados finales
    if juego.turno >= 20:
        mostrar_resultados_finales(juego)

def mostrar_resultados_finales(juego):
    # Ordenar los jugadores por la cantidad de dinero, de mayor a menor
    jugadores_ordenados = sorted(juego.jugadores, key=lambda j: j.dinero, reverse=True)
    ganador = jugadores_ordenados[0]

    # Crear una ventana para mostrar los resultados
    resultado_popup = tk.Toplevel()
    resultado_popup.title("Resultados Finales")
    resultado_popup.geometry("400x300")

    # Mostrar los resultados de todos los jugadores
    tk.Label(resultado_popup, text="Resultados del Juego", font=("Helvetica", 14, "bold")).pack(pady=10)
    for jugador in jugadores_ordenados:
        tk.Label(resultado_popup, text=f"{jugador.nombre}: {jugador.dinero} dólares").pack()

    # Mostrar el ganador en una fuente más grande y negrita
    tk.Label(resultado_popup, text=f"\nGanador: {ganador.nombre}", font=("Helvetica", 18, "bold")).pack(pady=10)
    tk.Label(resultado_popup, text=f"Con {ganador.dinero} dólares").pack()
