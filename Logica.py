import time

class Partida:
    def __init__(self, jugador: Jugador, repositorio: RepositorioPalabras):
        self.jugador = jugador
        self.repositorio = repositorio
        self.numero_nivel = 1
        self.nivel_actual = Nivel(self.numero_nivel, 60.0, 0.5, self.repositorio)
        self.puntaje_total = 0
        self.en_curso = False

    def iniciar(self):
        print(f"\nIniciando partida para {self.jugador.nombre}...")
        self.en_curso = True
        self.nivel_actual.generar_palabras()  # CORREGIDO
        self.tiempo_inicio = time.time()

    def registrar_entrada(self, entrada: str):
        palabra = self.nivel_actual.obtener_palabra()
        if not palabra:
            print("No hay palabra actual disponible.")
            return 0.0

        precision = palabra.comparar_con(entrada)
        print(palabra)
        self.nivel_actual.siguiente_palabra()
        return precision

    def asignar_puntaje(self, precision: float, velocidad: float):
        puntaje = int((precision * velocidad) / 10)
        self.puntaje_total += puntaje
        print(f"Puntaje del nivel: {puntaje} | Total acumulado: {self.puntaje_total}")
        return puntaje

    def evaluar_nivel(self, precision: float, velocidad: float):
        if self.nivel_actual.puede_pasar(precision, velocidad):
            self.aumentar_nivel()
        else:
            print("❌ No alcanzaste la precisión o velocidad requerida. Intenta de nuevo.")

    def aumentar_nivel(self):
        self.numero_nivel += 1
        if self.numero_nivel <= 3:
            print(f"\nAvanzando al nivel {self.numero_nivel}...")
            self.nivel_actual = Nivel(self.numero_nivel, 70.0, 0.6, self.repositorio)
            self.nivel_actual.generar_palabras()
        else:
            self.finalizar()

    def finalizar(self):
        print(f"\n✅ Partida finalizada. Puntaje total: {self.puntaje_total}")
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

        velocidades = []
        precisiones = []

        while partida.en_curso:
            palabra_obj = partida.nivel_actual.obtener_palabra()
            if not palabra_obj:
                partida.finalizar()
                break

            print(f"\nEscriba la palabra: {palabra_obj.texto}")

            # Medir tiempo
            inicio_palabra = time.time()
            entrada = input("👉 ")
            fin_palabra = time.time()

            tiempo_segundos = fin_palabra - inicio_palabra
            velocidad = 1 / tiempo_segundos if tiempo_segundos > 0 else 0

            # Calcular precisión
            precision = partida.registrar_entrada(entrada)
            precisiones.append(precision)
            velocidades.append(velocidad)

            print(f"⏱ Tiempo: {tiempo_segundos:.2f}s | 🚀 Velocidad: {velocidad:.2f} palabras/segundo | 🎯 Precisión: {precision:.2f}%")

            # Asignar puntaje y evaluar progreso
            partida.asignar_puntaje(precision, velocidad)
            partida.evaluar_nivel(precision, velocidad)

        # Promedios finales
        vel_prom = sum(velocidades) / len(velocidades) if velocidades else 0
        prec_prom = sum(precisiones) / len(precisiones) if precisiones else 0

        partida.jugador.registrar_resultado(
            partida.puntaje_total,
            prec_prom,
            vel_prom,
            partida.numero_nivel
        )

        self.mostrar_resultados(partida.jugador)

    def mostrar_resultados(self, jugador: Jugador):
        print("\n=== RESULTADOS FINALES ===")
        print(jugador)

    def salir(self):
        print("\nCerrando Typefast... ¡Hasta pronto!")
        self.activo = False















