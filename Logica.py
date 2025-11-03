import time

class Partida:
    def __init__(self, jugador: Jugador, repositorio: RepositorioPalabras):
        self.jugador = jugador
        self.repositorio = repositorio
        self.numero_nivel = 1
        self.nivel_actual = Nivel(self.numero_nivel, self.repositorio)
        self.en_curso = False

    def iniciar(self):
        print(f"\n=== Iniciando partida para {self.jugador.nombre} ===")
        self.en_curso = True
        self.nivel_actual.generar_palabras()

    def registrar_entrada(self, entrada: str) -> float:
        palabra = self.nivel_actual.obtener_palabra()
        if not palabra:
            return 0.0
        precision = palabra.comparar_con(entrada)
        return precision

    def asignar_puntaje(self, precision: float, velocidad: float):
        self.nivel_actual.registrar_intento(precision, velocidad)
        self.jugador.puntaje_total += int((precision * velocidad) / 10)

    def aumentar_nivel(self):
        self.numero_nivel += 1
        if self.numero_nivel > 3:
            print("\n¡Has completado todos los niveles!")
            self.en_curso = False
            return
        print(f"\n--- Pasando al NIVEL {self.numero_nivel} ---")
        self.nivel_actual = Nivel(self.numero_nivel, self.repositorio)
        self.nivel_actual.generar_palabras()

    def finalizar(self):
        print("\n=== FIN DE LA PARTIDA ===")
        self.en_curso = False


def jugar():
    print("=== BIENVENIDO A TYPEFAST ===")
    nombre = input("Ingrese su nombre: ")
    jugador = Jugador(nombre)
    repo = RepositorioPalabras()
    repo.cargar_palabras()
    partida = Partida(jugador, repo)
    partida.iniciar()

    while partida.en_curso:
        nivel = partida.nivel_actual
        print(f"\n NIVEL {nivel.numero} | Palabras: {len(nivel.palabras)}")
        for palabra_obj in nivel.palabras:
            print(f"\nEscriba la palabra: {palabra_obj.texto}")
            inicio_palabra = time.time()
            entrada = input(" Ingrese la palabra: ")
            fin_palabra = time.time()

            tiempo_segundos = fin_palabra - inicio_palabra
            tiempo_min = tiempo_segundos / 60
            velocidad = 1 / tiempo_min if tiempo_min > 0 else 0

            precision = partida.registrar_entrada(entrada)
            partida.asignar_puntaje(precision, velocidad)
            print(f" {tiempo_segundos:.2f}s |  {velocidad:.2f} WPM |  {precision:.2f}%")

            nivel.siguiente_palabra()

        prom_p, prom_v = nivel.prom_totales()
        print("\n=== RESULTADOS DEL NIVEL ===")
        print(f" Precisión promedio: {prom_p:.2f}%")
        print(f" Velocidad promedio: {prom_v:.2f} WPM")
        print(f" Puntaje total acumulado: {jugador.puntaje_total}")

        if nivel.puede_pasar():
            print("\n Cumples con los requisitos para avanzar al siguiente nivel.")
            decision = input("¿Deseas pasar al siguiente nivel? (S/N): ").strip().lower()
            if decision == "s":
                partida.aumentar_nivel()
            else:
                print("\nTe has retirado voluntariamente. Fin del juego.")
                partida.finalizar()
        else:
            print("\n No cumples los requisitos para pasar. Debes repetir el nivel.")
            repetir = input("¿Deseas intentarlo de nuevo? (S/N): ").strip().lower()
            if repetir == "s":
                nivel.generar_palabras()
            else:
                print("\nTe has retirado del juego.")
                partida.finalizar()

    print("\n=== RESULTADOS FINALES ===")
    print(f"Jugador: {jugador.nombre}")
    print(f"Puntaje total: {jugador.puntaje_total}")
    print("¡Gracias por jugar TYPEFAST!")


if __name__ == "__main__":
    jugar()
