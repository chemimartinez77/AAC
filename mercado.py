#mercado.py
class Mercado:
    def __init__(self):
        self.precio = 10  # Precio inicial del café
        self.stock_inicial = 10  # Stock total inicial (10 unidades por 3 jugadores)

    def ajustar_precio_por_venta(self, unidades_vendidas, total_cafe_disponible):
        """
        Ajusta el precio del café basado en la cantidad vendida y el stock total disponible.
        - Por cada unidad vendida, el precio baja.
        - Si el stock total es menor al stock inicial, el precio sube.
        """
        # Reducción de precio por la venta
        self.precio -= 2 * unidades_vendidas  # Cada unidad vendida reduce el precio en 2 dólares (ajustable)

        # Aumento del precio si el stock total es menor que el stock inicial
        print(f"Café disponible {total_cafe_disponible} - Stock inicial {self.stock_inicial}")
        if total_cafe_disponible < self.stock_inicial:
            print(f"´Café disponible {total_cafe_disponible} - Stock inicial {self.stock_inicial}")
            diferencia_stock = self.stock_inicial - total_cafe_disponible
            self.precio += diferencia_stock / 3  # Ajuste proporcional basado en la falta de stock

        # Limitar el precio mínimo a 1 para evitar precios negativos o cero
        if self.precio < 1:
            self.precio = 1

        print(f"El precio del café ahora es {self.precio} dólares por unidad")
