import time


class Jugador:
    def __init__(self, nombre: str):
        self.nombre: str = nombre
        self.puntaje_total = 0
        self.velocidad_promedio = 0.0
        self.precision_promedio = 0.0
        self.niveles_superados = 0
        self.partidas_jugadas = 0
        self.historial = []

    def registrar_resultado(self, puntaje: float, precision: float, velocidad: float, nivel_alcanzado=None):
        if not (isinstance(puntaje, (int, float)) and puntaje >= 0):
            raise ValueError("El puntaje debe ser un número mayor o igual a 0.")
        if not (isinstance(precision, (int, float)) and 0 <= precision <= 100):
            raise ValueError("La precisión debe estar en un rango de 0 a 100.")
        if not (isinstance(velocidad, (int, float)) and velocidad >= 0):
            raise ValueError("La velocidad debe ser mayor o igual a 0.")

        self.partidas_jugadas += 1
        self.puntaje_total += puntaje

        if nivel_alcanzado is not None:
            try:
                nivel = int(nivel_alcanzado)
                if nivel > self.niveles_superados:
                    self.niveles_superados = nivel
            except Exception:
                pass

        n_prev = self.partidas_jugadas - 1
        n_new = self.partidas_jugadas
        self.velocidad_promedio = (self.velocidad_promedio * n_prev + velocidad) / n_new
        self.precision_promedio = (self.precision_promedio * n_prev + precision) / n_new

        self.historial.append({
            'puntaje': puntaje,
            'precision': precision,
            'velocidad': velocidad,
            'nivel_alcanzado': nivel_alcanzado
        })

    def __str__(self):
        return (f"\nJugador: {self.nombre}\n"
                f"Puntaje total: {self.puntaje_total:.2f}\n"
                f"Velocidad promedio: {self.velocidad_promedio:.2f} palabras/min\n"
                f"Precisión promedio: {self.precision_promedio:.2f}%\n"
                f"Niveles superados: {self.niveles_superados}")


class PalabraJuego:
    def __init__(self, texto: str, usada: bool = False) -> None:
        self.texto: str = texto
        self.precision: float = 0.0
        self.errores: int = 0
        self.usada: bool = usada

    def calcular_errores(self, entrada: str) -> int:
        errores = sum(1 for i in range(min(len(self.texto), len(entrada))) if self.texto[i] != entrada[i])
        errores += abs(len(self.texto) - len(entrada))
        self.errores = errores
        return errores

    def comparar_con(self, entrada: str):
        errores = self.calcular_errores(entrada)
        total = len(entrada)
        self.precision = ((total - errores) / total) if total > 0 else 0.0
        return self.precision

    def __str__(self) -> str:
        return (f"Palabra: {self.texto} | Errores: {self.errores} | "
                f"Precisión: {round(self.precision * 100, 2)}%")


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
            PalabraJuego("raton"),
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
        return palabras_nivel[:cantidad]


class Nivel:
    def __init__(self, numero: int, tiempo_limite: float, precision_requerida: float,
                 repositorio: 'RepositorioPalabras') -> None:
        self.numero: int = numero
        self.tiempo_limite: float = tiempo_limite
        self.precision_requerida: float = precision_requerida
        self.palabras: list = []
        self.indice_actual: int = 0
        self.repositorio: RepositorioPalabras = repositorio

    def generar_palabra(self):
        self.palabras = self.repositorio.obtener_por_nivel(self.numero, 5)
        if self.palabras:
            print(f"\nPalabras cargadas para el nivel {self.numero}:")
            for palabra in self.palabras:
                print(" -", palabra.texto)
        else:
            print("No hay palabras disponibles para este nivel.")

    def puede_pasar(self, precision_jugador: float):
        if precision_jugador >= self.precision_requerida:
            print(" ¡Nivel superado!")
            return True
        else:
            print(" No alcanzaste la precisión requerida.")
            return False


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
        print(f"\n🎮 ¡Bienvenido {self.jugador.nombre}! Comenzando el nivel 1...")
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
        precision = (palabras_correctas / max(1, len(self.nivel_actual.palabras))) * 100
        velocidad = (palabras_correctas / (tiempo_transcurrido / 60))
        return precision, velocidad

    def asignar_puntaje(self, precision: float, velocidad: float):
        puntaje = (precision * 0.7) + (velocidad * 0.3)
        self.jugador.registrar_resultado(puntaje, precision, velocidad, self.nivel_actual.numero)
        print(f"Puntaje obtenido en nivel {self.nivel_actual.numero}: {puntaje:.2f}")
        return puntaje

    def avanzar_nivel(self):
        print("\n Evaluando si puedes avanzar de nivel.")
        if self.nivel_actual.puede_pasar(self.jugador.precision_promedio):
            self.historial_niveles.append(self.nivel_actual)
            nuevo_numero = self.nivel_actual.numero + 1
            nuevo_tiempo = max(10, self.nivel_actual.tiempo_limite - 5)
            nueva_precision = min(100, self.nivel_actual.precision_requerida + 5)

            # Crear el nuevo nivel y generar sus palabras
            self.nivel_actual = Nivel(
                numero=nuevo_numero,
                tiempo_limite=nuevo_tiempo,
                precision_requerida=nueva_precision,
                repositorio=self.repositorio
            )
            self.nivel_actual.generar_palabra()
            print(f"\n Avanzas al nivel {nuevo_numero} \n")
        else:
            print(" Muy malo perdiste.")

    def finalizar_partida(self):
        self.estado = "finalizada"
        print("\n-PARTIDA FINALIZADA-")
        print(self.jugador)
        print(f"Niveles completados: {len(self.historial_niveles)}")
        print("----------------------------")


    def iniciar(self):
        self.estado = "activa"
        print(f"\n🎮 ¡Bienvenido a TypeFast, {self.jugador.nombre}!")

        while True:
            nivel = Nivel(
                numero=self.nivel_actual,
                tiempo_limite=max(10, 30 - (self.nivel_actual - 1) * 5),
                precision_requerida=min(95, 80 + (self.nivel_actual - 1) * 5),
                repositorio=self.repositorio
            )

            superado = self.jugar_nivel(nivel)

            if superado:
                self.nivel_actual += 1
                if self.nivel_actual > 3:
                    print("\n🏆 ¡Has completado todos los niveles!")
                    break
            else:
                repetir = input("¿Deseas intentar el nivel otra vez? (s/n): ").strip().lower()
                if repetir != 's':
                    break

        self.finalizar_partida()

    def finalizar_partida(self):
        print("\n🏁 --- PARTIDA FINALIZADA ---")
        print(self.jugador)
        print("----------------------------")


# ---------------------------------------------
# BLOQUE PRINCIPAL
# ---------------------------------------------
if __name__ == "__main__":
    print("🧠 Bienvenido a TYPEFAST — Juego de mecanografía")
    nombre = input("Ingresa tu nombre: ")
    jugador = Jugador(nombre)
    repositorio = RepositorioPalabras()
    repositorio.cargar_palabras()

    partida = Partida(jugador, repositorio)
    partida.iniciar()
