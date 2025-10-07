import time
import random

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

        if nivel_alcanzado is not None and nivel_alcanzado > self.niveles_superados:
            self.niveles_superados = nivel_alcanzado

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
    def __init__(self, texto: str):
        self.texto = texto
        self.errores = 0
        self.precision = 0.0

    def comparar_con(self, entrada: str):
        errores = sum(1 for i in range(min(len(self.texto), len(entrada))) if self.texto[i] != entrada[i])
        errores += abs(len(self.texto) - len(entrada))
        self.errores = errores
        total = len(self.texto)
        self.precision = max(0, ((total - errores) / total) * 100)
        return self.precision


class RepositorioPalabras:
    def __init__(self):
        self.palabras = []

    def cargar_palabras(self):
        self.palabras = [
            "gato", "perro", "python", "computador", "teclado",
            "raton", "pantalla", "inteligencia", "programacion", "universidad"
        ]

    def obtener_por_nivel(self, nivel: int, cantidad: int):
        if nivel == 1:
            lista = [p for p in self.palabras if len(p) <= 5]
        elif nivel == 2:
            lista = [p for p in self.palabras if 6 <= len(p) <= 8]
        else:
            lista = [p for p in self.palabras if len(p) > 8]

        random.shuffle(lista)
        return lista[:cantidad]


class Nivel:
    def __init__(self, numero: int, tiempo_limite: float, precision_requerida: float, repositorio: RepositorioPalabras):
        self.numero = numero
        self.tiempo_limite = tiempo_limite
        self.precision_requerida = precision_requerida
        self.repositorio = repositorio
        self.palabras = repositorio.obtener_por_nivel(numero, 5)

    def puede_pasar(self, precision_media: float):
        return precision_media >= self.precision_requerida


class Partida:
    def __init__(self, jugador: Jugador, repositorio: RepositorioPalabras):
        self.jugador = jugador
        self.repositorio = repositorio
        self.nivel_actual = 1
        self.estado = "inactiva"

    def jugar_nivel(self, nivel: Nivel):
        print(f"\n🕹️ Nivel {nivel.numero} — Tiempo límite: {nivel.tiempo_limite} segundos")
        print("Escribe correctamente las siguientes palabras:")

        correctas = 0
        total_precision = 0
        inicio = time.time()

        for palabra in nivel.palabras:
            print(f"\n➡️  {palabra}")
            entrada = input("Tu palabra: ").strip()
            palabra_obj = PalabraJuego(palabra)
            precision = palabra_obj.comparar_con(entrada)
            total_precision += precision

            if precision == 100:
                correctas += 1
                print("✅ Correcto!")
            else:
                print(f"❌ Errores: {palabra_obj.errores} | Precisión: {precision:.2f}%")

        fin = time.time()
        duracion = fin - inicio

        precision_media = total_precision / len(nivel.palabras)
        velocidad = (correctas / (duracion / 60))
        puntaje = (precision_media * 0.7) + (velocidad * 0.3)

        print(f"\n📊 Resultados del nivel {nivel.numero}:")
        print(f"Precisión promedio: {precision_media:.2f}%")
        print(f"Velocidad: {velocidad:.2f} palabras/min")
        print(f"Puntaje: {puntaje:.2f}")

        self.jugador.registrar_resultado(puntaje, precision_media, velocidad, nivel.numero)

        if nivel.puede_pasar(precision_media):
            print("🎉 ¡Nivel superado!")
            return True
        else:
            print("😕 No alcanzaste la precisión requerida. Inténtalo de nuevo.")
            return False

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
