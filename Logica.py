import time

class Partida:
    def __init__(self, jugador: Jugador, repositorio: RepositorioPalabras):
        self.jugador = jugador
        self.repositorio = repositorio
        self.numero_nivel = 1
        self.nivel_actual = Nivel(self.numero_nivel, 60.0, 80.0, self.repositorio)
        self.puntaje_total = 0
        self.en_curso = False
        self.resultados = []

    def iniciar(self):
        print(f"\nIniciando partida para {self.jugador.nombre}...")
        self.en_curso = True
        self.nivel_actual.generar_palabra()
        self.tiempo_inicio = time.time()

    def registrar_entrada(self, entrada: str):
        palabra = self.nivel_actual.obtener_palabra()
        if not palabra:
            print("No hay palabra actual disponible.")
            return

        precision = palabra.comparar_con(entrada)
        print(palabra)

        self.nivel_actual.siguiente_palabra()
        return precision

    def calcular_velocidad(self, palabras_correctas: int):
        self.tiempo_fin = time.time()
        tiempo_min = (self.tiempo_fin - self.tiempo_inicio) / 60
        velocidad = palabras_correctas / tiempo_min if tiempo_min > 0 else 0
        return velocidad

    def asignar_puntaje(self, precision: float, velocidad: float):
        puntaje = int((precision * velocidad) / 10)
        self.puntaje_total += puntaje
        print(f"Puntaje del nivel: {puntaje} | Total: {self.puntaje_total}")
        return puntaje















