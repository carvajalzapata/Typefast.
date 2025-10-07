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
        self.puntaje_total = 0
        self.velocidad_promedio = 0.0
        self.precision_promedio = 0.0
        self.niveles_superados = 0
        self.partidas_jugadas = 0
        self.historial = []

    def __str__(self):
        return (f"Jugador: {self.nombre}\n"
                f"Puntaje total: {self.puntaje_total}\n"
                f"Velocidad promedio : {self.velocidad_promedio:.2f}\n"
                f"Precisión promedio : {self.precision_promedio:.2f}\n"
                f"Niveles superados: {self.niveles_superados}")

class PalabraJuego:
        def __init__(self, texto: str, usada: bool = False) -> None:
            self.texto: str = texto
            self.precision: float = 0.0
            self.errores: int = 0
            self.usada: bool = usada

        def calcular_errores(self, entrada: str) -> int:
            error = 0
            i = 0

            while i < len(self.texto) and i < len(entrada):
                if self.texto[i] != entrada[i]:
                    error += 1
                i = i + 1

            if len(self.texto) > len(entrada):
                error += (len(self.texto) - len(entrada))
            elif len(entrada) > len(self.texto):
                error += (len(entrada) - len(self.texto))

            self.errores = error
            return error

        def comparar_con(self, entrada: str):
            errores = self.calcular_errores(entrada)
            total = len(entrada)

            if total > 0:
                aciertos = total - errores
                self.precision = aciertos / total
            else:
                self.precision = 0.0

            return self.precision

        def palabra_correcta(self, palabra_correcta: str) -> bool:
            if self.texto.lower().strip() == palabra_correcta.lower().strip():
                return True
            else:
                return False

        def es_correcta(self):
            return self.usada

        def __str__(self) -> str:
            return f"Palabra escrita: {self.texto}, Errores: {self.errores}, Precisión: {round(self.precision * 100, 2)}%"

    class RepositorioPalabras:

        def __init__(self) -> None:
            self.palabras: list = []

        def cargar_palabras(self):
            self.palabras = [
                PalabraJuego("gato"),
                PalabraJuego("perro"),
                PalabraJuego("python"),
                PalabraJuego("computador"),
                PalabraJuego("teclado"),
                PalabraJuego("ratón"),
                PalabraJuego("pantalla"),
                PalabraJuego("inteligencia"),
                PalabraJuego("programacion"),
                PalabraJuego("universidad"),
            ]

        def obtener_por_nivel(self, nivel: int, cantidad: int):
            palabras_nivel = []

            for palabra in self.palabras:
                longitud = len(palabra.texto)

                if nivel == 1 and longitud <= 5:
                    palabras_nivel.append(palabra)
                elif nivel == 2 and 6 <= longitud <= 8:
                    palabras_nivel.append(palabra)
                elif nivel == 3 and longitud > 8:
                    palabras_nivel.append(palabra)

            return palabras_nivel

        def __str__(self):
            print("Palabras en el repositorio")
            for palabra in self.palabras:
                print(f"- {palabra.texto}")

    class Nivel:
        def __init__(self, numero: int, tiempo_limite: float, precision_requerida: float,
                     repositorio: 'RepositorioPalabras') -> None:
            self.numero: int = numero
            self.tiempo_limite: float = tiempo_limite
            self.precision_requerida: float = precision_requerida
            self.palabras: list = []
            self.indice_actual: int = 0
            self.repositorio: RepositorioPalabras = repositorio

        def generar_palabra(self, repositorio):
            self.palabras = repositorio.obtener_por_nivel(self.numero, 5)

            if len(self.palabras) > 0:
                print("Palabras cargadas para el nivel", self.numero)
                for palabra in self.palabras:
                    print("-", palabra.texto)
            else:
                print("No hay palabras disponibles para este nivel.")

        def obtener_palabra(self) -> None:
            if self.indice_actual < len(self.palabras):
                return self.palabras[self.indice_actual]
            else:
                return None

        def siguiente_palabra(self):
            if self.indice_actual < len(self.palabras) - 1:
                self.indice_actual = self.indice_actual + 1
            else:
                print("Ya completaste todas las palabras de este nivel.")

        def puede_pasar(self, precision_jugador: float):
            if precision_jugador >= self.precision_requerida:
                print("¡Nivel superado!")
                return True
            else:
                print("No alcanzaste la precisión requerida.")
                return False

        def reducir_tiempo(self, reduccion: int):
            pass

        def pasar_nivel(self):
            pass

        def mostrar_informacion(self):
            pass

        def reiniciar(self):
            self.indice_actual = 0
            print("Nivel reiniciado.")


class Partida:

    def __init__(self, jugador: Jugador, repositorio: RepositorioPalabras):
        self.jugador = jugador
        self.repositorio = repositorio
        self.nivel_actual = Nivel(
            numero=1,
            tiempo_limite=30,
            precision_requerida=80,
            repositorio=repositorio
        )
        self.historial_niveles = []
        self.estado = "inactiva"
        self.tiempo_inicio = None

    def iniciar_partida(self):
        print(f"¡Bienvenido {self.jugador.nombre}! Comenzando el nivel 1...")
        self.estado = "activa"
        self.tiempo_inicio = time.time()
        self.nivel_actual.generar_palabra()

    def verificar_palabra(self, palabra_original: str, palabra_usuario: str):
        palabra = PalabraJuego(palabra_original)
        errores = palabra.calcular_errores(palabra_usuario)
        precision = palabra.comparar_con(palabra_usuario)
        return errores, precision

    def calcular_precision_y_velocidad(self, palabras_correctas: int, tiempo_transcurrido: float):
        if tiempo_transcurrido <= 0:
            raise ValueError("El tiempo transcurrido debe ser mayor que 0.")
        precision = (palabras_correctas / max(1, self.nivel_actual.indice_actual + 1)) * 100
        velocidad = (palabras_correctas / (tiempo_transcurrido / 60))
        return precision, velocidad

    def asignar_puntaje(self, precision: float, velocidad: float):
        puntaje = (precision * 0.7) + (velocidad * 0.3)
        self.jugador.registrar_resultado(puntaje, precision, velocidad, self.nivel_actual.numero)
        print(f"Puntaje obtenido en nivel {self.nivel_actual.numero}: {puntaje:.2f}")
        return puntaje

    def avanzar_nivel(self):
        if self.nivel_actual.puede_pasar(self.jugador.precision_promedio):
            self.historial_niveles.append(self.nivel_actual)
            nuevo_numero = self.nivel_actual.numero + 1
            nuevo_tiempo = max(10, self.nivel_actual.tiempo_limite - 5)
            nueva_precision = min(100, self.nivel_actual.precision_requerida + 5)
            self.nivel_actual = Nivel(
                numero=nuevo_numero,
                tiempo_limite=nuevo_tiempo,
                precision_requerida=nueva_precision,
                repositorio=self.repositorio
            )
            print(f"\n--- Avanzas al nivel {nuevo_numero} ---\n")
        else:
            print("Debes repetir el nivel actual para mejorar tu precisión.")

    def finalizar_partida(self):
        self.estado = "finalizada"
        print("\n--- PARTIDA FINALIZADA ---")
        print(self.jugador)
        print(f"Niveles completados: {len(self.historial_niveles)}")
        print("----------------------------")

