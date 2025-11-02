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
        tiempo_min = (self.tiempo_fin - self.tiempo_inicio) / 40
        velocidad = palabras_correctas / tiempo_min if tiempo_min > 0 else 0
        return velocidad

    def asignar_puntaje(self, precision: float, velocidad: float):
        puntaje = int((precision * velocidad) / 10)
        self.puntaje_total += puntaje
        print(f"Puntaje del nivel: {puntaje} | Total: {self.puntaje_total}")
        return puntaje


    def evaluar_nivel(self, precision: float, velocidad: float):
        if self.nivel_actual.puede_pasar(precision):
            self.aumentar_nivel()
        else:
            print("Repite el nivel con mejor precisión.")

    def aumentar_nivel(self):
        self.numero_nivel += 1
        if self.numero_nivel <= 3:
            print(f"Pasando al nivel {self.numero_nivel}...")
            self.nivel_actual = Nivel(self.numero_nivel, 50.0, 85.0, self.repositorio)
            self.nivel_actual.generar_palabra()
        else:
            self.finalizar()

    def finalizar(self):
        print(f"\nPartida finalizada. Puntaje total: {self.puntaje_total}")
        self.jugador.registrar_resultado(
            self.puntaje_total,
            self.nivel_actual.precision_requerida,
            0,
            self.numero_nivel
        )
        self.en_curso = False

class Juego:
    def __init__(self):
        print("Inicializando Typefast...")
        self.repositorio = RepositorioPalabras()
        self.repositorio.cargar_palabras()
        self.partidas = []
        self.jugadores = []
        self.partida_actual = None
        self.activo = True
        print("Repositorio de palabras cargado correctamente.\n")

    def registrar_jugador(self, nombre: str) -> Jugador:
        jugador = Jugador(nombre)
        self.jugadores.append(jugador)
        print(f"Jugador registrado: {nombre}")
        return jugador

    def iniciar_partida(self, nombre_jugador: str):
        jugador = next((j for j in self.jugadores if j.nombre == nombre_jugador), None)
        if not jugador:
            jugador = self.registrar_jugador(nombre_jugador)

        partida = Partida(jugador, self.repositorio)
        self.partidas.append(partida)
        self.partida_actual = partida
        partida.iniciar()
        return partida

    def jugar(self):
        print("=== BIENVENIDO A TYPEFAST ===")
        nombre = input("Ingrese su nombre: ")
        partida = self.iniciar_partida(nombre)

        while partida.en_curso:
            palabra_obj = partida.nivel_actual.obtener_palabra()
            if not palabra_obj:
                partida.finalizar()
                break

            print(f"\nEscriba la palabra: {palabra_obj.texto}")
            inicio_palabra = time.time()  # ⏱ Empieza a medir
            entrada = input("👉 ")
            fin_palabra = time.time()  # ⏱ Termina de medir

            precision = partida.registrar_entrada(entrada)

            tiempo_total = (fin_palabra - inicio_palabra) / 60
            palabras_correctas = 1 if precision >= 80 else 0
            velocidad = palabras_correctas / tiempo_total if tiempo_total > 0 else 0

            partida.asignar_puntaje(precision, velocidad)
            partida.evaluar_nivel(precision, velocidad)

    def mostrar_resultados(self, jugador: Jugador):
        print("\n=== RESULTADOS FINALES ===")
        print(jugador)

    def reiniciar_partida(self):
        if self.partida_actual:
            self.partida_actual = Partida(self.partida_actual.jugador, self.repositorio)
            print("Partida reiniciada.")
            self.partida_actual.iniciar()

    def salir(self):
        print("\nCerrando Typefast... ¡Hasta pronto!")
        self.activo = False














