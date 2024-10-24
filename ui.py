#ui.py
import tkinter as tk
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import ttk, messagebox
from config import REGIONES_DISPONIBLES
from acciones import realizar_accion, jugar_turno
from utilidades import actualizar_tabla

def crear_imagen_con_texto(icon_path, texto, font_path="arial.ttf", font_size=16):
    # Cargar el icono y redimensionarlo a un tamaño mayor
    icono = Image.open(icon_path).resize((48, 48), Image.LANCZOS)
    
    # Cargar la fuente TrueType, para que admita tildes
    if font_path:
        fuente = ImageFont.truetype(font_path, font_size)
    else:
        fuente = ImageFont.load_default()
    
    # Calcular el tamaño del texto utilizando getbbox
    ancho_texto, alto_texto = fuente.getbbox(texto)[2:4]  # getbbox devuelve (x_min, y_min, x_max, y_max)
    ancho_total = icono.width + 10 + ancho_texto  # Aumentar el espacio entre el icono y el texto
    alto_total = max(icono.height, alto_texto)

    # Crear una nueva imagen combinada
    imagen_combinada = Image.new("RGBA", (ancho_total, alto_total), (255, 255, 255, 0))
    draw = ImageDraw.Draw(imagen_combinada)
    
    # Pegar el icono en la imagen combinada
    imagen_combinada.paste(icono, (0, (alto_total - icono.height) // 2))

    # Dibujar el texto al lado del icono
    draw.text((icono.width + 10, (alto_total - alto_texto) // 2), texto, font=fuente, fill="black")
    
    # Convertir la imagen a un formato que tkinter pueda utilizar
    return ImageTk.PhotoImage(imagen_combinada)

def mostrar_popup_plantar(juego, tree, root):
    popup = tk.Toplevel()
    popup.title("Selecciona una región para plantar")
    popup.geometry("500x400")
    tk.Label(popup, text="Elige una región:").pack(pady=10)

    ruta_imagenes = os.path.join(os.path.dirname(__file__), "static")
    imagenes_regiones = {
        "Bolivia": "Flag-map_of_Bolivia.svg.png",
        "Brasil": "Flag-map_of_Brazil.svg.png",
        "Colombia": "Flag-map_of_Colombia.svg.png",
        "México": "Mexico_Flag_Map.svg.png"
    }

    regiones_frame = tk.Frame(popup)
    regiones_frame.pack(pady=10)

    for region in REGIONES_DISPONIBLES:
        imagen_path = os.path.join(ruta_imagenes, imagenes_regiones.get(region.nombre, ""))
        if os.path.exists(imagen_path):
            try:
                imagen = Image.open(imagen_path)
                imagen.thumbnail((80, 80), Image.LANCZOS)
                imagen_tk = ImageTk.PhotoImage(imagen)

                marco_region = tk.Frame(regiones_frame)
                marco_region.pack(side=tk.LEFT, padx=5, pady=5)

                btn_region = tk.Button(
                    marco_region,
                    image=imagen_tk,
                    width=80,
                    height=80,
                    command=lambda r=region: [ejecutar_plantar(juego, tree, r, popup)]
                )
                btn_region.image = imagen_tk
                btn_region.pack()

                etiqueta_info = tk.Label(
                    marco_region,
                    text=f"{region.nombre}\nCoste: {region.coste_plantacion}, Prod: {region.produccion_por_turno}",
                    font=("Helvetica", 10)
                )
                etiqueta_info.pack()
            except Exception as e:
                print(f"Error al cargar la imagen {imagen_path}: {e}")
                btn_region = tk.Button(
                    regiones_frame,
                    text=f"{region.nombre} (Coste: {region.coste_plantacion}, Producción: {region.produccion_por_turno})",
                    command=lambda r=region: [ejecutar_plantar(juego, tree, r, popup)]
                )
                btn_region.pack(pady=5)
        else:
            btn_region = tk.Button(
                regiones_frame,
                text=f"{region.nombre} (Coste: {region.coste_plantacion}, Producción: {region.produccion_por_turno})",
                command=lambda r=region: [ejecutar_plantar(juego, tree, r, popup)]
            )
            btn_region.pack(pady=5)

    popup.transient(root)
    popup.grab_set()
    root.wait_window(popup)

def realizar_accion_si_posible(juego, tree, accion, unidades_vender=None):
    jugador = juego.jugadores[0]
    accion_valida = False

    if accion == "producir" and jugador.produccion > 0:
        realizar_accion(juego, tree, accion, None, actualizar_log)
        accion_valida = True
    elif accion == "vender":
        # Aquí pasamos las unidades desde el campo de entrada
        if unidades_vender is not None and jugador.cafe_disponible > 0:
            realizar_accion(juego, tree, accion, None, actualizar_log, unidades_vender)
            accion_valida = True
        else:
            messagebox.showerror("Acción no válida", "No puedes realizar esta acción debido a la falta de recursos.")
    else:
        messagebox.showerror("Acción no válida", "No puedes realizar esta acción debido a la falta de recursos.")

    if accion_valida:
        jugador_ha_actuado.set(True)
        habilitar_boton_turno()

def ejecutar_plantar(juego, tree, region, popup):
    realizar_accion(juego, tree, "plantar", region, actualizar_log)
    popup.destroy()
    jugador_ha_actuado.set(True)
    habilitar_boton_turno()

def habilitar_boton_turno():
    if jugador_ha_actuado.get():
        btn_turno.config(state="normal")

def actualizar_log(_, mensaje):
    log_text.config(state="normal")
    log_text.insert("end", mensaje + "\n")
    log_text.config(state="disabled")
    log_text.yview("end")

def siguiente_turno(juego, tree, turno_actual, turno_label, price_label):
    jugar_turno(juego, tree, log_text, price_label, actualizar_log, btn_turno, jugador_ha_actuado)
    turno_actual.set(turno_actual.get() + 1)
    turno_label.config(text=f"Turno actual: {turno_actual.get()}")
    habilitar_boton_turno()

def crear_interfaz(juego):
    global log_text, btn_turno, jugador_ha_actuado

    root = tk.Tk()
    root.title("Juego de Café")
    root.geometry("1600x900")

    jugador_ha_actuado = tk.BooleanVar(value=False)

    ruta_imagenes = os.path.join(os.path.dirname(__file__), "static")
    imagen_jugador = crear_imagen_con_texto(os.path.join(ruta_imagenes, "icoplayer.png"), "Jugador")
    imagen_dinero = crear_imagen_con_texto(os.path.join(ruta_imagenes, "icomoney.png"), "Dinero")
    imagen_produccion = crear_imagen_con_texto(os.path.join(ruta_imagenes, "icofactory.png"), "Producción")
    imagen_cafe = crear_imagen_con_texto(os.path.join(ruta_imagenes, "icocoffee.png"), "Café disponible")
    imagen_puntos = crear_imagen_con_texto(os.path.join(ruta_imagenes, "icoscore.png"), "Puntos")

    main_frame = tk.Frame(root)
    main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Mostrar el precio actual del café
    price_label = tk.Label(main_frame, text=f"Precio del café: {juego.mercado.precio} dólares por unidad", font=("Helvetica", 12))
    price_label.pack(pady=5)

    # Etiqueta para mostrar el turno actual
    turno_actual = tk.IntVar(value=1)  # Variable para el número de turno
    turno_label = tk.Label(main_frame, text=f"Turno actual: {turno_actual.get()}", font=("Helvetica", 12))
    turno_label.pack(pady=5)

    # Crear una tabla para mostrar los datos de los jugadores
    tree = ttk.Treeview(main_frame, columns=("Jugador", "Dinero", "Producción", "Café disponible", "Puntos"), show="headings", height=12)
    tree.heading("Jugador", image=imagen_jugador, anchor="center")
    tree.heading("Dinero", image=imagen_dinero, anchor="center")
    tree.heading("Producción", image=imagen_produccion, anchor="center")
    tree.heading("Café disponible", image=imagen_cafe, anchor="center")
    tree.heading("Puntos", image=imagen_puntos, anchor="center")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), padding=[10, 5, 10, 35])
    style.configure("Treeview", rowheight=25)

    tree.column("Jugador", anchor="center", width=200)
    tree.column("Dinero", anchor="center", width=130, minwidth=100)
    tree.column("Producción", anchor="center", width=130, minwidth=100)
    tree.column("Café disponible", anchor="center", width=160, minwidth=120)
    tree.column("Puntos", anchor="center", width=100, minwidth=80)

    tree.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
    actualizar_tabla(tree, juego.jugadores)

    action_frame = tk.Frame(main_frame)
    action_frame.pack(pady=10)

    # Entrada para ingresar la cantidad de café a vender
    label_vender = tk.Label(action_frame, text="Unidades de café a vender:")
    label_vender.grid(row=0, column=0, padx=10)
    unidades_entry = tk.Entry(action_frame, width=5)  # Entrada de texto para unidades a vender
    unidades_entry.grid(row=0, column=1, padx=10)

    # Botones de acción
    btn_plantar = tk.Button(action_frame, text="Plantar", command=lambda: mostrar_popup_plantar(juego, tree, root))
    btn_producir = tk.Button(action_frame, text="Producir", command=lambda: realizar_accion_si_posible(juego, tree, "producir"))
    btn_vender = tk.Button(action_frame, text="Vender", command=lambda: realizar_accion_si_posible(juego, tree, "vender", int(unidades_entry.get())))

    btn_plantar.grid(row=1, column=1, padx=10)
    btn_producir.grid(row=1, column=2, padx=10)
    btn_vender.grid(row=1, column=3, padx=10)

    # Botón para pasar al siguiente turno
    btn_turno = tk.Button(main_frame, text="Siguiente Turno", state="disabled", command=lambda: siguiente_turno(juego, tree, turno_actual, turno_label, price_label))
    btn_turno.pack(pady=20)

    log_text = tk.Text(main_frame, height=8, wrap="word", state="disabled", font=("Helvetica", 10))
    log_text.pack(expand=True, fill=tk.BOTH, side=tk.BOTTOM)

    root.mainloop()
