import time
class Partida:

    def __init__(self, jugador: Jugador):
        self.jugador = jugador
        self.nivel_actual = Nivel(numero = 1)
        self.historial_niveles = []
        self.estado = "inactiva"self.tiempo_inicio = None

    def iniciar_partida(self):
        print(f"¡Bienvenido {self.jugador.nombre}! Comenzando el nivel 1...")
        self.estado = "activa"
        self.tiempo_inicio = time.time()

    def verificar_palabra(self, palabra_original: str, palabra_usuario: str):
        palabra  = PalabraJuego(palabra_original)
        errores = palabra.contar_errores(palabra_usuario)
        precision = palabra.calcular_precision(palabra_usuario)
        return errores, precision

    def calcular_precision_y_velocidad(self, palabras_correctas: int, tiempo_transcurrido: float)
        pass
