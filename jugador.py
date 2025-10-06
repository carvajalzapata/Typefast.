class Jugador:

    def __init__(self,nombre: str):
        self.nombre: str = nombre
        self.puntaje_total = 0
        self.velocidad_promedio = 0.0
        self.precsion_promedio = 0.0
        self.niveles_superados = 0
        self.partidas_jugadas = 0
        self.historial = []