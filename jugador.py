class Jugador:
    def __init__(self, nombre: str):
        self.nombre: str = nombre
        self.puntaje_total = 0
        self.promedios_por_nivel = {}
        self.puntaje_por_nivel = {}

