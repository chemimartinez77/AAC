#region.py
class Region:
    def __init__(self, nombre, coste_plantacion, produccion_por_turno):
        self.nombre = nombre
        self.coste_plantacion = coste_plantacion
        self.produccion_por_turno = produccion_por_turno
    
    def producir(self):
        return self.produccion_por_turno
