class Jugador:

    def __init__(self,nombre: str):
        self.nombre: str = nombre
        self.puntaje_total = 0
        self.velocidad_promedio = 0.0
        self.precision_promedio = 0.0
        self.niveles_superados = 0
        self.partidas_jugadas = 0
        self.historial = []

    def registrar_resultado(self, puntaje : int, precision: float, velocidad: float, nivel_alcanzado = None):
        if not isinstance(puntaje, int) or puntaje < 0:
            raise ValueError("el puntaje debe ser un numero mayor igual a 0 ")
        if not (isinstance(precision, (int, float)) and 0 <= precision <= 100):
            raise ValueError("la precision debe estar en un rango de 0 a 100")
        if not (isinstance(velocidad, (int, float)) and velocidad >= 0):
            raise ValueError("la velocidad deb de ser mayor que 0")

        self.partidas_jugadas += 1
        self.puntaje_total += int(puntaje)

        if nivel_alcanzado is not None:
            try:
                nivel = int(nivel_alcanzado)
                if nivel > self.niveles_superados:
                    self.niveles_superados = nivel
            except Exception:
                pass

        n_prev = self.partidas_jugadas - 1
        n_new = self.partidas_jugadas
        self.velocidad_promedio = (self.velocidad_promedio * n_prev + float(velocidad)) / n_new
        self.precision_promedio = (self.precision_promedio * n_prev + float(precision)) / n_new

        self.historial.append({
            'puntaje': puntaje,
            'precision': precision,
            'velocidad': velocidad,
            'nivel_alcanzado': nivel_alcanzado if nivel_alcanzado is not None else None

        })

    def actualizar_estadisticas(self):
        if not self.historial:
            self.puntaje_total = 0
            self.velocidad_promedio = 0.0
            self.precision_promedio = 0.0
            self.niveles_superados = 0
            self.partidas_jugadas = 0
            return
        self.partidas_jugadas = len(self.historial)
        self.puntaje_total = sum((e['puntaje ']) for e in self.historial) / len(self.historial)
        self.velocidad_promedio = sum(e['velocidad'] for e in self.historial) / len(self.historial)
        self.precision_promedio = sum(e['precision'] for e in self.historial) / len(self.historial)
        niveles = [e['nivel_alcanzado'] for e in self.historial if e.get('nivel_alcanzado')is not None]
        self.niveles_superados = max(niveles) if niveles else 0

    def reiniciar_datos(self):
        pass