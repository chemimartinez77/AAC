#jugador.py
class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.dinero = 50
        self.plantaciones = []  # Lista de plantaciones que posee
        self.produccion = 0  # Capacidad de producción total
        self.cafe_disponible = 10
        self.puntos = 0  # Puntos de victoria acumulados

    def plantar(self, region, log_func=None):
        # Verificar si la región ya ha sido plantada para no aumentar la producción dos veces
        if region not in self.plantaciones:  # Comprobar si la región ya fue plantada
            if self.dinero >= region.coste_plantacion:
                self.dinero -= region.coste_plantacion
                self.plantaciones.append(region)
                self.produccion += region.produccion_por_turno  # Aumentar la capacidad de producción
                if log_func:
                    log_func("end", f"{self.nombre} ha plantado en {region.nombre}\n")
            else:
                if log_func:
                    log_func("end", f"{self.nombre} no tiene suficiente dinero para plantar en {region.nombre}\n")
        else:
            # Mensaje si la región ya fue plantada
            if log_func:
                log_func("end", f"{self.nombre} ya ha plantado en {region.nombre}, no se aumentará la producción\n")

    def producir(self, log_func=None):
        # Incrementar el café disponible en función de la capacidad de producción
        if self.produccion > 0:
            self.cafe_disponible += self.produccion
            if log_func:
                log_func("end", f"{self.nombre} ha producido {self.produccion} unidades de café\n")
        else:
            if log_func:
                log_func("end", f"{self.nombre} no tiene capacidad de producción para producir café\n")

    def vender(self, mercado, log_func=None, unidades_vender=0, jugadores=None):
        if unidades_vender <= self.cafe_disponible:
            ganancia = unidades_vender * mercado.precio
            self.dinero += ganancia
            self.cafe_disponible -= unidades_vender
            if log_func:
                log_func("end", f"{self.nombre} ha vendido {unidades_vender} unidades de café por {ganancia} dólares\n")

            # Ajustar el precio del café basado en las ventas y el stock disponible
            total_cafe_disponible = sum(j.cafe_disponible for j in jugadores)  # Usamos 'jugadores' del objeto juego
            mercado.ajustar_precio_por_venta(unidades_vender, total_cafe_disponible)
        else:
            if log_func:
                log_func("end", f"{self.nombre} no tiene suficiente café para vender {unidades_vender} unidades\n")

    def obtener_puntos(self):
        self.puntos = self.dinero // 10
