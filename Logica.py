import time

class Partida:
    def __init__(self, jugador: Jugador, repositorio: RepositorioPalabras):
        self.jugador = jugador
        self.repositorio = repositorio
        self.numero_nivel = 1
        self.nivel_actual = Nivel(self.numero_nivel, 60.0, 80.0, self.repositorio)
        self.puntaje_total = 0
        self.en_curso = False

    def iniciar(self):
        print(f"\nIniciando partida para {self.jugador.nombre}...")
        self.en_curso = True
        self.nivel_actual.generar_palabras()  # ← CORREGIDO
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
            print("Repite el nivel con mejor precisión.")



def jugar(self):
    print("=== BIENVENIDO A TYPEFAST ===")
    nombre = input("Ingrese su nombre: ")
    partida = self.iniciar_partida(nombre)

    velocidades = []  # guardamos velocidad de cada palabra
    precisiones = []  # guardamos precisión de cada palabra

    while partida.en_curso:
        palabra_obj = partida.nivel_actual.obtener_palabra()
        if not palabra_obj:
            partida.finalizar()
            break  # este break está BIEN aquí (solo sale si ya no hay más palabras)

        print(f"\nEscriba la palabra: {palabra_obj.texto}")

        # Medir tiempo de escritura
        inicio_palabra = time.time()
        entrada = input("👉 ")
        fin_palabra = time.time()

        tiempo_segundos = fin_palabra - inicio_palabra
        tiempo_min = tiempo_segundos / 60

        # Calcular precisión
        precision = partida.registrar_entrada(entrada)
        precisiones.append(precision)

        # Calcular velocidad (1 palabra / tiempo en minutos)
        velocidad = 1 / tiempo_min if tiempo_min > 0 else 0
        velocidades.append(velocidad)

        print(f"⏱ Tiempo: {tiempo_segundos:.2f}s | 🚀 Velocidad: {velocidad:.2f} WPM | 🎯 Precisión: {precision:.2f}%")

        # Asignar puntaje y evaluar progreso
        partida.asignar_puntaje(precision, velocidad)
        partida.evaluar_nivel(precision, velocidad)

    # Calcular promedios al final de la partida
    vel_prom = sum(velocidades) / len(velocidades) if velocidades else 0
    prec_prom = sum(precisiones) / len(precisiones) if precisiones else 0

    # Registrar resultado en el jugador
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














