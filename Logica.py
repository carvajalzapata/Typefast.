import time
import random

class Partida:
    def __init__(self, jugador: Jugador, repositorio: RepositorioPalabras):
        self.jugador = jugador
        self.repositorio = repositorio
        self.nivel_actual = 1
        self.estado = "inactiva"

    def jugar_nivel(self, nivel: Nivel):
        print(f"\n Estas en el nivel {nivel.numero} — tienes un tiempo de: {nivel.tiempo_limite} segundos")
        print("Copia perro!:")

        correctas = 0
        total_precision = 0
        inicio = time.time()

        for palabra in nivel.palabras:
            print(f"\n Palabra: {palabra.texto}")
            entrada = input("Tu palabra: ").strip()
            palabra_obj = PalabraJuego(palabra.texto)
            precision = palabra_obj.comparar_con(entrada)
            total_precision += precision

            if precision == 1.0:
                correctas += 1
                print("No esta mal!")
            else:
                print(f"Pesimo: {palabra_obj.errores} | Precisión: {precision * 100:.2f}%")

        fin = time.time()
        duracion = fin - inicio

        precision_media = (total_precision / len(nivel.palabras)) * 100
        velocidad = (correctas / (duracion / 60))
        puntaje = (precision_media * 0.7) + (velocidad * 0.3)

        print(f"\n Resultados del nivel {nivel.numero}:")
        print(f"Precisión promedio: {precision_media:.2f}%")
        print(f"Velocidad: {velocidad:.2f} palabras/min")
        print(f"Puntaje: {puntaje:.2f}")

        self.jugador.registrar_resultado(puntaje, precision_media, velocidad, nivel.numero)

        if nivel.puede_pasar(precision_media):
            print("¡Tuviste suerte!")
            return True
        else:
            print("Dedicate a tiktoker mejor.")
            return False

    def iniciar(self):
        self.estado = "activa"
        print(f"\n ¡Esto es TypeFast MadaFakar, {self.jugador.nombre}!")

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
                    print("\n ¡pasaste!")
                    break
            else:
                repetir = input("¿Deseas intentar el nivel otra vez? (s/n): ").strip().lower()
                if repetir != 's':
                    break

        self.finalizar_partida()

    def finalizar_partida(self):
        print("\n PARTIDA FINALIZADA ")
        print(self.jugador)
        print("----------------------------")

if __name__ == "__main__":
    print("Bienvenido a TYPEFAST — Juego de mecanografía 🖋️")
    nombre = input("Ingresa tu nombre: ")
    jugador = Jugador(nombre)
    repositorio = RepositorioPalabras()
    repositorio.cargar_palabras()

    partida = Partida(jugador, repositorio)
    partida.iniciar()





