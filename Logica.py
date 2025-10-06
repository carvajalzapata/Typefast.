class Partida:

    def __init__(self, jugador: Jugador):
        self.jugador = jugador
        self.nivel_actual = Nivel(numero = 1)
        self.historial_niveles = []
        self.estado = "inactiva"self.tiempo_inicio = None

